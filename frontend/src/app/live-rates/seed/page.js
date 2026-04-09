"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { API_URL } from "../../../lib/api";

export default function LiveSeedsPage() {
  const [rates, setRates] = useState([]);
  const [loading, setLoading] = useState(true);

  // ✅ Fetch latest SEED live rates from backend
  const fetchLiveRates = async () => {
    try {
      const res = await fetch(`${API_URL}/api/live-rates/latest`);
      const data = await res.json();

      // ✅ Only use seeds data
      const items = Array.isArray(data.seeds) ? data.seeds : [];
      const processed = items.map((item) => {
        const maxPrice = parseFloat(item.max_price || 0);
        return {
          ...item,
          price_per_kg: (maxPrice / 100).toFixed(2),
          price_per_100kg: maxPrice.toFixed(2),
        };
      });

      setRates(processed);
    } catch (err) {
      console.error("❌ Failed to fetch live seed rates:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLiveRates();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-lg text-gray-600">
          Fetching today's live seed prices...
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-yellow-50 text-gray-800 p-8">
      {/* 🔹 Navbar */}
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-yellow-700">
          🌱 Daily Seed Market Rates
        </h1>
        <Link
          href="/live-rates"
          className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg transition"
        >
          ← Back
        </Link>
      </nav>

      {/* 🔹 Header */}
      <section className="text-center mb-6">
        <h2 className="text-3xl font-semibold mb-2 text-yellow-800">
          Live Seed Rates (Updated daily at 6 AM)
        </h2>
        <p className="text-gray-600">
          Showing top {rates.length} seed commodities with maximum mandi prices.
        </p>
      </section>

      {/* 🔹 Data Table */}
      <div className="overflow-x-auto bg-white rounded-xl shadow-md p-4">
        <table className="min-w-full border-collapse">
          <thead>
            <tr className="border-b bg-yellow-100">
              <th className="p-3 text-left">Commodity</th>
              <th className="p-3 text-left">Market</th>
              <th className="p-3 text-left">Price (₹/kg)</th>
              <th className="p-3 text-left">Price (₹/100 kg)</th>
            </tr>
          </thead>
          <tbody>
            {rates.length > 0 ? (
              rates.slice(0, 100).map((item, idx) => (
                <tr key={idx} className="border-b hover:bg-yellow-50 transition">
                  <td className="p-3 font-semibold text-yellow-700">
                    {item.commodity}
                  </td>
                  <td className="p-3">{item.market}</td>
                  <td className="p-3 text-yellow-700 font-medium">
                    ₹{item.price_per_kg}
                  </td>
                  <td className="p-3 text-yellow-700 font-medium">
                    ₹{item.price_per_100kg}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan="4"
                  className="p-4 text-center text-gray-500"
                >
                  No seed data available.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* 🔹 Footer */}
      <p className="text-sm text-gray-500 mt-6 text-center">
        Last updated: {new Date().toLocaleString()}
      </p>
    </main>
  );
}
