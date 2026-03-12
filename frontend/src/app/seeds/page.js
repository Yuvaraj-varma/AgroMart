"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useCart } from "../../context/CartContext";

// utility - normalize simple strings same way as backend (close match)
const normalize = (s = "") =>
  String(s)
    .toLowerCase()
    .replace(/\(.*?\)/g, "") // remove parentheses content
    .replace(/[-,_]/g, " ")
    .replace(/[^a-z0-9\s]/g, "")
    .replace(/\s+/g, "")
    .replace(/s$/, "");

export default function SeedsPage() {
  const { addToCart } = useCart();

  const [allSeeds, setAllSeeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [type, setType] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [quantities, setQuantities] = useState({});
  const [liveRates, setLiveRates] = useState([]);

  // Fetch seeds from PostgreSQL
  useEffect(() => {
    const fetchSeeds = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/seeds/");
        if (!res.ok) throw new Error("Failed to fetch seeds");
        const data = await res.json();

        const backendSeeds = data.map((p) => ({
          name: p.name,
          type: p.type || "Seed",
          price: Number(p.price) || 0,
          unit: p.unit || (p.price > 500 ? "quintal" : "kg"),
          description: p.description || "High-quality certified seeds.",
          image_url: p.image_url?.startsWith("http")
            ? p.image_url
            : `http://127.0.0.1:8000${p.image_url || "/uploads/default.jpg"}`,
        }));

        setAllSeeds(backendSeeds);
      } catch (err) {
        console.error("❌ Seeds fetch failed:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSeeds();
  }, []);

  // Fetch live seed rates from backend
  useEffect(() => {
    const fetchLiveRates = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/live-rates/latest");
        const data = await res.json();
        const rates = data.seeds || [];

        // Build map keyed by normalized commodity_norm (prefer commodity_norm field)
        const map = {};
        rates.forEach((r) => {
          const norm = (r.commodity_norm || r.commodity || "").toString().toLowerCase().replace(/\s+/g, "");
          // parse max_price safely
          const raw = r.max_price ?? r.modal_price ?? r.min_price ?? 0;
          const parsed = Number(String(raw).replace(/,/g, ""));
          // keep highest
          if (!map[norm] || (parsed && parsed > Number(map[norm].max_price || 0))) {
            map[norm] = { ...r, max_price: parsed };
          }
        });

        // Convert map to array for any UI needs
        const uniqueRates = Object.values(map);

        setLiveRates(uniqueRates);
      } catch (err) {
        console.warn("⚠️ Live seed rates fetch failed:", err);
      }
    };

    fetchLiveRates();
    const interval = setInterval(fetchLiveRates, 1000 * 60 * 30); // every 30 min
    return () => clearInterval(interval);
  }, []);

  // Filters
  const filteredSeeds = allSeeds.filter((seed) => {
    const matchesName = seed.name.toLowerCase().includes(search.toLowerCase());
    const matchesType = type ? seed.type === type : true;
    const matchesPrice = maxPrice ? seed.price <= Number(maxPrice) : true;
    return matchesName && matchesType && matchesPrice;
  });

  const handleQuantityChange = (index, value) => {
    setQuantities((prev) => ({ ...prev, [index]: value }));
  };

  const getQuantityMultiplier = (label) => {
    if (label.includes("5kg")) return 5;
    if (label.includes("10kg")) return 10;
    if (label.includes("5 quintal")) return 5;
    return 1;
  };

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 text-lg">Loading seeds...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 text-gray-800 p-8">
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-green-700">🌱 Seeds Marketplace</h1>
        <Link href="/" className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
          ← Back to Home
        </Link>
      </nav>

      <section className="text-center mb-6">
        <h2 className="text-3xl font-semibold mb-2 text-green-800">Buy Certified Seeds Directly from Farmers 🌾</h2>
        <p className="text-gray-600">Browse and buy at real mandi-linked live prices.</p>
      </section>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
        <input type="text" placeholder="Search seed..." value={search} onChange={(e) => setSearch(e.target.value)} className="border border-green-200 rounded-md p-2 w-64" />
        <select value={type} onChange={(e) => setType(e.target.value)} className="border border-green-200 rounded-md p-2 w-48">
          <option value="">All Types</option>
          <option value="Cereal">Cereal</option>
          <option value="Oilseed">Oilseed</option>
          <option value="Pulses">Pulses</option>
          <option value="Fiber Crop">Fiber Crop</option>
        </select>
        <input type="number" placeholder="Max Price (₹)" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} className="border border-green-200 rounded-md p-2 w-40" />
      </div>

      {/* Seeds Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredSeeds.length > 0 ? (
          filteredSeeds.map((item, index) => {
            const quantityLabel = quantities[index] || `1 ${item.unit}`;
            const multiplier = getQuantityMultiplier(quantityLabel);

            // find live rate using normalized matching (commodity_norm preferred)
            const seedNorm = normalize(item.name);
            const linkedRate = liveRates.find((r) => {
              const rNorm = normalize(r.commodity_norm || r.commodity);
              return rNorm === seedNorm || rNorm.includes(seedNorm) || seedNorm.includes(rNorm);
            });

            // compute final price (use live rate if present, otherwise DB price)
            let livePriceNum = null;
            if (linkedRate && (linkedRate.max_price !== undefined && linkedRate.max_price !== null)) {
              // ensure numeric
              livePriceNum = Number(linkedRate.max_price) || Number(linkedRate.modal_price) || Number(linkedRate.min_price) || null;
              // convert per backend convention (divide by 100)
              if (livePriceNum !== null) {
                livePriceNum = Number((livePriceNum / 100).toFixed(2));
              }
            }

            const finalUnitPrice = livePriceNum !== null ? livePriceNum : Number(item.price || 0);
            const totalPrice = Number((finalUnitPrice * multiplier).toFixed(2));

            return (
              <div key={index} className="bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-md transition transform hover:-translate-y-1 p-3 flex flex-col">
                <img src={item.image_url} alt={item.name} className="w-full h-48 object-cover rounded-xl" />
                <div className="flex-1 mt-3 text-center">
                  <h3 className="text-lg font-semibold text-green-700 flex items-center justify-center gap-1">
                    {item.name}
                    {linkedRate && (
                      <span title={`Live rate linked (₹${finalUnitPrice} / ${item.unit})`} className="text-green-600 text-base animate-pulse">✅</span>
                    )}
                  </h3>
                  <p className="text-gray-600 text-sm mt-1">{item.description}</p>

                  <select value={quantityLabel} onChange={(e) => handleQuantityChange(index, e.target.value)} className="mt-3 border border-gray-300 rounded-md px-2 py-1 text-sm w-full">
                    <option>{`1 ${item.unit}`}</option>
                    {item.unit === "kg" && (
                      <>
                        <option>5kg</option>
                        <option>10kg</option>
                      </>
                    )}
                    {item.unit === "quintal" && <option>5 quintal</option>}
                  </select>

                  <p className="mt-2 text-green-800 font-semibold">₹{finalUnitPrice} / {item.unit}</p>
                </div>

                <button onClick={() => addToCart({ name: item.name, image: item.image_url, unitPrice: finalUnitPrice, quantity: quantityLabel, totalPrice })} className="mt-3 border border-green-600 text-green-600 font-semibold py-2 rounded-lg hover:bg-green-600 hover:text-white transition">
                  🛒 Add to Cart
                </button>
              </div>
            );
          })
        ) : (
          <p className="text-center text-gray-600 col-span-full">No seeds found for the selected filters.</p>
        )}
      </div>
    </main>
  );
}
