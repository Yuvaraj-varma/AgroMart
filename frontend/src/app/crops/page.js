"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useCart } from "../../context/CartContext";

export default function CropsPage() {
  const { addToCart } = useCart();

  const [allCrops, setAllCrops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [type, setType] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [quantities, setQuantities] = useState({});
  const [liveRates, setLiveRates] = useState([]);

  // ✅ Fetch crops from PostgreSQL
  useEffect(() => {
    const fetchCrops = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/crops/");
        if (!res.ok) throw new Error("Failed to fetch crops");
        const data = await res.json();

        const backendCrops = data.map((p) => ({
          name: p.name,
          type: p.type || "Crop",
          price: Number(p.price) || 0,
          unit: p.unit || (p.price > 500 ? "quintal" : "kg"),
          description: p.description || "High-quality crop from farms.",
          image_url: p.image_url?.startsWith("http")
            ? p.image_url
            : `http://127.0.0.1:8000${p.image_url || "/uploads/default.jpg"}`,
        }));

        setAllCrops(backendCrops);
      } catch (err) {
        console.error("❌ Crops fetch failed:", err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCrops();
  }, []);

  // ✅ Fetch Live Rates (MongoDB)
  useEffect(() => {
    const fetchLiveRates = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/live-rates/");
        const data = await res.json();
        const rates = data.rates || [];

        // Deduplicate live commodities by highest price
        const uniqueRates = Object.values(
          rates.reduce((acc, curr) => {
            const name = curr.commodity.toLowerCase();
            if (!acc[name] || curr.max_price > acc[name].max_price) {
              acc[name] = curr;
            }
            return acc;
          }, {})
        );

        setLiveRates(uniqueRates);

        // ✅ Update crop prices dynamically if live rate found
        setAllCrops((prevCrops) =>
          prevCrops.map((crop) => {
            const cropName = crop.name.toLowerCase().replace(/s$/, "");
            const rate = uniqueRates.find((r) => {
              const commodity = r.commodity.toLowerCase();
              return (
                commodity.includes(cropName) ||
                cropName.includes(commodity)
              );
            });

            if (rate?.max_price) {
              const pricePerKg = (rate.max_price / 100).toFixed(2);
              return { ...crop, price: Number(pricePerKg), unit: "kg" };
            }
            return crop;
          })
        );
      } catch (error) {
        console.warn("⚠️ Live rates fetch failed:", error);
      }
    };

    fetchLiveRates();
  }, []);

  // ✅ Filters
  const filteredCrops = allCrops.filter((crop) => {
    const matchesName = crop.name.toLowerCase().includes(search.toLowerCase());
    const matchesType = type ? crop.type === type : true;
    const matchesPrice = maxPrice ? crop.price <= Number(maxPrice) : true;
    return matchesName && matchesType && matchesPrice;
  });

  const handleQuantityChange = (index, value) => {
    setQuantities((prev) => ({ ...prev, [index]: value }));
  };

  const getQuantityMultiplier = (label) => {
    if (label.includes("5kg")) return 5;
    if (label.includes("10kg")) return 10;
    return 1;
  };

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 text-lg">Loading crops...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 text-gray-800 p-8">
      {/* Navbar */}
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-green-700">🌾 Crops Marketplace</h1>
        <Link
          href="/"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </Link>
      </nav>

      <section className="text-center mb-6">
        <h2 className="text-3xl font-semibold mb-2 text-green-800">
          Fresh Crops from Indian Farms 🧺
        </h2>
        <p className="text-gray-600">
          Browse, filter, and buy at real mandi-linked prices.
        </p>
      </section>

      {/* Search + Filter */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
        <input
          type="text"
          placeholder="Search crop..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-green-200 rounded-md p-2 w-64"
        />
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="border border-green-200 rounded-md p-2 w-48"
        >
          <option value="">All Types</option>
          <option value="Cereal">Cereal</option>
          <option value="Vegetable">Vegetable</option>
          <option value="Fruit">Fruit</option>
          <option value="Cash Crop">Cash Crop</option>
          <option value="Oilseed">Oilseed</option>
          <option value="Organic">Organic</option>
        </select>
        <input
          type="number"
          placeholder="Max Price (₹)"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          className="border border-green-200 rounded-md p-2 w-40"
        />
      </div>

      {/* ✅ Crop Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredCrops.map((item, index) => {
          const quantityLabel = quantities[index] || `1 ${item.unit}`;
          const multiplier = getQuantityMultiplier(quantityLabel);
          const totalPrice = item.price * multiplier;

          const linkedRate = liveRates.find((r) =>
            r.commodity.toLowerCase().includes(item.name.toLowerCase())
          );

          return (
            <div
              key={index}
              className="bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-md transition transform hover:-translate-y-1 p-3 flex flex-col"
            >
              <img
                src={item.image_url}
                alt={item.name}
                className="w-full h-48 object-cover rounded-xl"
              />
              <div className="flex-1 mt-3 text-center">
                <h3 className="text-lg font-semibold text-green-700 flex items-center justify-center gap-1">
                  {item.name}
                  {linkedRate && (
                    <span
                      title={`Live rate linked (₹${(linkedRate.max_price / 100).toFixed(2)} / kg)`}
                      className="text-green-600 text-base animate-pulse"
                    >
                      ✅
                    </span>
                  )}
                </h3>
                <p className="text-gray-600 text-sm mt-1">{item.description}</p>
                <select
                  value={quantityLabel}
                  onChange={(e) => handleQuantityChange(index, e.target.value)}
                  className="mt-3 border border-gray-300 rounded-md px-2 py-1 text-sm w-full"
                >
                  <option>1 {item.unit}</option>
                  {item.unit === "kg" && (
                    <>
                      <option>5kg</option>
                      <option>10kg</option>
                    </>
                  )}
                </select>
                <p className="mt-2 text-green-800 font-semibold">
                  ₹{totalPrice} / {quantityLabel}
                </p>
              </div>
              <button
                onClick={() =>
                  addToCart({
                    name: item.name,
                    image: item.image_url,
                    unitPrice: item.price,
                    quantity: quantityLabel,
                    totalPrice,
                  })
                }
                className="mt-3 border border-green-600 text-green-600 font-semibold py-2 rounded-lg hover:bg-green-600 hover:text-white transition"
              >
                🛒 Add to Cart
              </button>
            </div>
          );
        })}
      </div>
    </main>
  );
}
