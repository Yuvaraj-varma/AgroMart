"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { API_URL } from "../../lib/api";

export default function VendorDashboard() {
  const [products, setProducts] = useState({ crops: [], seeds: [], fertilizers: [] });
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const role  = localStorage.getItem("role");
    const token = localStorage.getItem("token");
    if (!token || role !== "vendor") {
      alert("⚠️ Only vendors can access this page.");
      router.push("/login");
      return;
    }
    fetchMyProducts(token);
  }, []);

  async function fetchMyProducts(token) {
    try {
      const res = await fetch(`${API_URL}/api/vendor/my-products`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      setProducts(data);
    } catch (err) {
      console.error("❌ Failed to fetch products:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(category, id) {
    if (!confirm("Are you sure you want to delete this product?")) return;
    const token = localStorage.getItem("token");
    setDeleting(`${category}-${id}`);
    try {
      const res = await fetch(`${API_URL}/api/vendor/my-products/${category}/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        setProducts((prev) => ({
          ...prev,
          [category]: prev[category].filter((p) => p.id !== id),
        }));
      } else {
        alert("❌ Failed to delete product.");
      }
    } catch (err) {
      alert("⚠️ Something went wrong.");
    } finally {
      setDeleting(null);
    }
  }

  const allProducts = [
    ...products.crops.map((p) => ({ ...p, category: "crops" })),
    ...products.seeds.map((p) => ({ ...p, category: "seeds" })),
    ...products.fertilizers.map((p) => ({ ...p, category: "fertilizers" })),
  ];

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 text-lg">Loading your products...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 text-gray-800 p-8">
      {/* Navbar */}
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-green-700">🧑🌾 Vendor Dashboard</h1>
        <div className="flex gap-3">
          <Link href="/post" className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
            + Post New Product
          </Link>
          <Link href="/" className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg">
            ← Home
          </Link>
        </div>
      </nav>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label: "Crops", count: products.crops.length, color: "green" },
          { label: "Seeds", count: products.seeds.length, color: "yellow" },
          { label: "Fertilizers", count: products.fertilizers.length, color: "blue" },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-xl shadow-sm p-4 text-center border border-gray-100">
            <p className="text-3xl font-bold text-green-700">{s.count}</p>
            <p className="text-gray-600 mt-1">{s.label} Posted</p>
          </div>
        ))}
      </div>

      {/* Products Table */}
      {allProducts.length === 0 ? (
        <div className="text-center mt-20">
          <p className="text-gray-600 text-lg mb-4">You haven't posted any products yet.</p>
          <Link href="/post" className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold">
            Post Your First Product
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <table className="min-w-full">
            <thead className="bg-green-100">
              <tr>
                <th className="p-4 text-left">Image</th>
                <th className="p-4 text-left">Name</th>
                <th className="p-4 text-left">Category</th>
                <th className="p-4 text-left">Type</th>
                <th className="p-4 text-left">Price</th>
                <th className="p-4 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {allProducts.map((p) => (
                <tr key={`${p.category}-${p.id}`} className="border-b hover:bg-green-50 transition">
                  <td className="p-4">
                    <img
                      src={p.image_url ? `${API_URL}${p.image_url}` : "/product-placeholder.svg"}
                      alt={p.name}
                      className="w-14 h-14 object-cover rounded-lg"
                    />
                  </td>
                  <td className="p-4 font-semibold text-green-700">{p.name}</td>
                  <td className="p-4 capitalize">{p.category.slice(0, -1)}</td>
                  <td className="p-4 text-gray-600">{p.type || "-"}</td>
                  <td className="p-4 font-semibold">₹{p.price}</td>
                  <td className="p-4">
                    <button
                      onClick={() => handleDelete(p.category, p.id)}
                      disabled={deleting === `${p.category}-${p.id}`}
                      className="bg-red-500 hover:bg-red-600 text-white px-4 py-1 rounded-lg font-semibold transition disabled:bg-gray-400"
                    >
                      {deleting === `${p.category}-${p.id}` ? "Deleting..." : "Delete"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
