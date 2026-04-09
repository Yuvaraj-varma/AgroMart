from fastapi import APIRouter
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import re

from app.core.config import settings
from app.db.mongo_session import rates_collection as collection

router = APIRouter()
IST = pytz.timezone("Asia/Kolkata")


# -------------------------------------------------------------
# 🧹 Helper: normalize commodity/crop names
# -------------------------------------------------------------
def normalize_name(s: str) -> str:
    """Normalize commodity/crop names for consistent matching."""
    if not s:
        return ""
    s_norm = s.strip().lower()

    # Remove parentheses and their contents, punctuation, and hyphens
    s_norm = re.sub(r"\(.*?\)", "", s_norm)     # remove "(Unginned)" etc.
    s_norm = s_norm.replace("-", " ")
    s_norm = re.sub(r"[^\w\s]", "", s_norm)     # remove punctuation

    # Remove unwanted descriptive words
    for word in ["unginned", "ginned", "seed", "faq", "other", "common", "fresh"]:
        s_norm = s_norm.replace(word, "")

    # Collapse and remove all spaces
    s_norm = re.sub(r"\s+", "", s_norm)

    # Remove trailing plural 's'
    if s_norm.endswith("s") and len(s_norm) > 2:
        s_norm = s_norm[:-1]

    return s_norm


# -------------------------------------------------------------
# 🧠 Helper — Find last known rate for a commodity from history
# -------------------------------------------------------------
def get_last_known_rate(commodity_name: str):
    """
    Return the most recent record for a commodity (crop or seed) from history.
    Returns the item dict or None.
    """
    try:
        target_norm = normalize_name(commodity_name)
        # iterate documents newest first (sort by fetched_at desc then date desc)
        records = collection.find({}, {"_id": 0}).sort([("fetched_at", -1), ("date", -1)])
        for rec in records:
            # check crops first
            for c in rec.get("crops", []):
                if normalize_name(c.get("commodity", "")) == target_norm:
                    return c
            # then seeds
            for s in rec.get("seeds", []):
                if normalize_name(s.get("commodity", "")) == target_norm:
                    return s
        return None
    except Exception as e:
        print(f"⚠️ Error in get_last_known_rate for {commodity_name}: {e}")
        return None


# -------------------------------------------------------------
# 🟢 MAIN FUNCTION — Fetch & Store Crops + Seeds Data
# -------------------------------------------------------------
def fetch_and_store_agmarknet_data():
    """Fetch daily Agmarknet data and store both crop and seed live rates."""
    try:
        params = {
            "api-key": settings.AGMARKNET_API_KEY,
            "format": "json",
            "limit": 1000,
        }

        print("🌾 Fetching latest Agmarknet data...")
        response = requests.get(settings.AGMARKNET_URL, params=params, timeout=25)

        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text[:200]}")
            return

        data = response.json()
        if "records" not in data:
            print("❌ Unexpected API response structure")
            return

        records = data["records"]

        seeds_data = []
        crops_data = []

        for item in records:
            commodity_raw = item.get("commodity", "")
            commodity_norm = normalize_name(commodity_raw)
            if not commodity_raw:
                continue

            item["commodity_norm"] = commodity_norm

            if "seed" in commodity_raw.lower():
                seeds_data.append(item)
            else:
                crops_data.append(item)

        # ✅ Deduplicate by normalized name (keep highest max_price)
        def get_unique_max(items):
            unique = {}
            for i in items:
                name_raw = i.get("commodity") or ""
                name_norm = i.get("commodity_norm") or normalize_name(name_raw)
                try:
                    max_price = float(i.get("max_price", 0) or 0)
                except (ValueError, TypeError):
                    max_price = 0.0
                if not name_norm:
                    continue
                if name_norm not in unique or max_price > float(unique[name_norm].get("max_price", 0) or 0):
                    i["commodity_norm"] = name_norm
                    unique[name_norm] = i
            return sorted(unique.values(), key=lambda x: float(x.get("max_price", 0) or 0), reverse=True)

        unique_seeds = get_unique_max(seeds_data)
        unique_crops = get_unique_max(crops_data)

        today = datetime.now(IST).strftime("%Y-%m-%d")

        record = {
            "date": today,
            "fetched_at": datetime.now(IST),
            "count": len(unique_crops) + len(unique_seeds),
            "crops": unique_crops[:500],
            "seeds": unique_seeds[:500],
        }

        collection.update_one({"date": today}, {"$set": record}, upsert=True)
        print(f"✅ Stored {len(unique_crops)} crops and {len(unique_seeds)} seeds for {today}")

    except Exception as e:
        print(f"❌ Error updating live rates: {e}")


# -------------------------------------------------------------
# 🟢 FASTAPI ROUTES
# -------------------------------------------------------------
@router.get("/", tags=["Live Rates"])
def fetch_agmarknet_data():
    """Manually trigger Agmarknet data fetch (Crops + Seeds)."""
    fetch_and_store_agmarknet_data()
    latest = collection.find_one(sort=[("date", -1)], projection={"_id": 0})
    return latest or {"message": "❌ No data found"}


@router.get("/latest", tags=["Live Rates"])
def get_latest_live_rates():
    """✅ Get the most recent live rate record (Crops + Seeds)."""
    latest = collection.find_one(sort=[("fetched_at", -1)], projection={"_id": 0})
    if not latest:
        return {"message": "❌ No live rates found", "crops": [], "seeds": []}

    # Ensure normalization on-the-fly
    def ensure_norm(items):
        out = []
        for it in items:
            it = dict(it)
            raw = it.get("commodity", "")
            if not it.get("commodity_norm"):
                it["commodity_norm"] = normalize_name(raw)
            out.append(it)
        return out

    crops = ensure_norm(
        sorted(latest.get("crops", []), key=lambda x: float(x.get("max_price", 0) or 0), reverse=True)
    )
    seeds = ensure_norm(
        sorted(latest.get("seeds", []), key=lambda x: float(x.get("max_price", 0) or 0), reverse=True)
    )

    # -----------------------------
    # Fallback: fill missing important commodities from history
    # -----------------------------
    # you can adjust this list as needed
    important_commodities = [
        "sugarcane",
        "cotton",
        "rice",
        "wheat",
        # add any other commodities you want guaranteed
    ]

    existing_norms = set([normalize_name(c.get("commodity", "")) for c in crops + seeds])

    for name in important_commodities:
        if name not in existing_norms:
            last = get_last_known_rate(name)
            if last:
                # ensure commodity_norm exists on the historical record
                last = dict(last)
                if not last.get("commodity_norm"):
                    last["commodity_norm"] = normalize_name(last.get("commodity", ""))
                crops.append(last)
                existing_norms.add(name)

    # update count to reflect fallback additions
    total_count = len(crops) + len(seeds)

    return {
        "message": "✅ Latest live rates fetched successfully (with history fallback)",
        "date": latest.get("date"),
        "count": total_count,
        "crops": crops,
        "seeds": seeds,
    }


@router.get("/history", tags=["Live Rates"])
def get_all_live_rates():
    """Get all stored live rate data from MongoDB."""
    try:
        records = list(collection.find({}, {"_id": 0}).sort("date", -1))
        for rec in records:
            rec["crops"] = [
                {**c, "commodity_norm": c.get("commodity_norm") or normalize_name(c.get("commodity", ""))}
                for c in rec.get("crops", [])
            ]
            rec["seeds"] = [
                {**s, "commodity_norm": s.get("commodity_norm") or normalize_name(s.get("commodity", ""))}
                for s in rec.get("seeds", [])
            ]
        return {"count": len(records), "data": records}
    except Exception as e:
        return {"error": str(e)}


# -------------------------------------------------------------
# 🕕 SCHEDULER — Auto-fetch every day at 6 AM IST
# -------------------------------------------------------------
scheduler_started = False

def start_scheduler():
    global scheduler_started
    if scheduler_started:
        return
    scheduler = BackgroundScheduler(timezone=IST)
    scheduler.add_job(fetch_and_store_agmarknet_data, "cron", hour=6, minute=0)
    scheduler.start()
    scheduler_started = True
    print("🕕 Scheduler started — auto-fetches live rates daily at 6 AM IST.")

# ✅ Start scheduler automatically once when module loads
start_scheduler()
