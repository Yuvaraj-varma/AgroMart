"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useCart } from "../../context/CartContext";
import { API_URL } from "../../lib/api";

export default function FertilizersPage() {
  const { addToCart } = useCart();
  const [fertilizers, setFertilizers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [type, setType] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  // ✅ Fetch fertilizers from PostgreSQL only
  useEffect(() => {
    const fetchFertilizers = async () => {
      try {
        const res = await fetch(`${API_URL}/api/fertilizers/`);
        if (!res.ok) throw new Error("Failed to fetch fertilizers");
        const data = await res.json();

        const backendFertilizers = data.map((f) => ({
          name: f.name,
          type: f.type || "Fertilizer",
          price: Number(f.price) || 0,
          description:
            f.description || "Certified fertilizer for healthy crop growth.",
          image_url: f.image_url?.startsWith("http")
            ? f.image_url
            : `${API_URL}${f.image_url || "/uploads/default.jpg"}`,
        }));

        setFertilizers(backendFertilizers);
      } catch (err) {
        console.error("❌ Fertilizers fetch failed:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchFertilizers();
  }, []);

  // ✅ Filters
  const filtered = fertilizers.filter((f) => {
    const matchesName = f.name.toLowerCase().includes(search.toLowerCase());
    const matchesType = type ? f.type === type : true;
    const matchesPrice = maxPrice ? f.price <= Number(maxPrice) : true;
    return matchesName && matchesType && matchesPrice;
  });

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 text-lg">Loading fertilizers...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 text-gray-800 p-8">
      {/* Navbar */}
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-green-700">
          🧪 Fertilizers Marketplace
        </h1>
        <Link
          href="/"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </Link>
      </nav>

      {/* Heading */}
      <section className="text-center mb-6">
        <h2 className="text-3xl font-semibold mb-2 text-green-800">
          Buy Certified Fertilizers for Better Yields 🌿
        </h2>
        <p className="text-gray-600">
          Browse and purchase fertilizers directly from verified sellers.
        </p>
      </section>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
        <input
          type="text"
          placeholder="Search fertilizer..."
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
          <option value="Nitrogen">Nitrogen</option>
          <option value="Phosphorus">Phosphorus</option>
          <option value="Potassium">Potassium</option>
          <option value="Organic">Organic</option>
          <option value="Balanced">Balanced</option>
          <option value="Natural-Organic">Natural-Organic</option>
        </select>
        <input
          type="number"
          placeholder="Max Price (₹)"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          className="border border-green-200 rounded-md p-2 w-40"
        />
      </div>

      {/* Fertilizer Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {filtered.length > 0 ? (
          filtered.map((item, index) => (
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
                <h3 className="text-lg font-semibold text-green-700">
                  {item.name}
                </h3>
                <p className="text-gray-600 text-sm mt-1">
                  {item.description}
                </p>
                <p className="mt-2 text-green-800 font-semibold">
                  ₹{item.price} / 25kg
                </p>
              </div>
              <button
                onClick={() =>
                  addToCart({
                    name: item.name,
                    image: item.image_url,
                    unitPrice: item.price,
                    quantity: "25kg",
                    totalPrice: item.price,
                  })
                }
                className="mt-3 border border-green-600 text-green-600 font-semibold py-2 rounded-lg hover:bg-green-600 hover:text-white transition"
              >
                🛒 Add to Cart
              </button>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-600 col-span-full">
            No fertilizers found for the selected filters.
          </p>
        )}
      </div>
    </main>
  );
}
