"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { API_URL } from "../lib/api";

export default function HomePage() {
  const [userRole, setUserRole] = useState(null);
  const [userName, setUserName] = useState(null);

  // ✅ Fetch user info from backend if token exists
  useEffect(() => {
    async function fetchUser() {
      const token = localStorage.getItem("token");
      if (!token) return; // Not logged in

      try {
        const res = await fetch(`${API_URL}/api/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const data = await res.json();
          setUserRole(data.role);
          setUserName(data.name || "User");
        }
      } catch (err) {
        console.error("❌ Failed to fetch user info:", err);
      }
    }

    fetchUser();
  }, []);

  // ✅ Logout function
  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setUserRole(null);
    setUserName(null);
  }

  return (
    <main
      className="min-h-screen text-gray-800"
      style={{
        backgroundColor: "#f0fdf4",
        backgroundImage: `url('https://www.transparenttextures.com/patterns/paper-fibers.png')`,
      }}
    >
      {/* 🌿 Navbar */}
      <nav className="flex justify-between items-center px-8 py-4 bg-green-700 text-white shadow-md">
        <h1 className="text-2xl font-bold">🌾 AgroMart</h1>

        <div className="flex items-center space-x-6 text-lg">
          <Link href="/" className="hover:underline">
            Home
          </Link>
          <Link href="/seeds" className="hover:underline">
            Seeds
          </Link>
          <Link href="/fertilizers" className="hover:underline">
            Fertilizers
          </Link>
          <Link href="/crops" className="hover:underline">
            Crops
          </Link>

          {/* ✅ Only show Post Product if Vendor */}
          {userRole === "vendor" && (
            <Link href="/post" className="hover:underline">
              Post Product
            </Link>
          )}

          <Link
            href="/cart"
            className="ml-4 border border-white px-4 py-1 rounded-lg hover:bg-white hover:text-green-700 transition"
          >
            🛒 Cart
          </Link>

          {/* ✅ Conditional Login / Logout */}
          {userRole ? (
            <div className="flex items-center space-x-4">
              <span className="font-semibold">
                🌿 Welcome {userName} ({userRole === "vendor" ? "Vendor" : "Buyer"}) 👋
              </span>
              <button
                onClick={handleLogout}
                className="border border-white px-3 py-1 rounded-lg hover:bg-white hover:text-green-700 transition"
              >
                Logout
              </button>
            </div>
          ) : (
            <>
              <Link
                href="/login"
                className="border border-white px-3 py-1 rounded-lg hover:bg-white hover:text-green-700 transition"
              >
                Login
              </Link>
              <Link
                href="/signup"
                className="border border-white px-3 py-1 rounded-lg hover:bg-white hover:text-green-700 transition"
              >
                Signup
              </Link>
            </>
          )}
        </div>
      </nav>

      {/* 🌱 Hero Section */}
      <section className="flex flex-col items-center justify-center text-center py-24 px-4">
        {/* ✅ Show Login/Signup only if not logged in */}
        {!userRole && (
          <div className="flex space-x-6 mb-6">
            <Link
              href="/login"
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg shadow-md transition font-medium"
            >
              🔐 Login
            </Link>
            <Link
              href="/signup"
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg shadow-md transition font-medium"
            >
              📝 Signup
            </Link>
          </div>
        )}

        {/* 🧾 Title and Description */}
        <h2 className="text-4xl font-bold mb-4 text-green-800">
          Buy & Sell Agricultural Goods Easily
        </h2>
        <p className="text-lg text-gray-700 max-w-xl mb-8">
          Explore quality seeds, fertilizers, and fresh crops — all in one place.
        </p>

        {/* 🌿 Main Buttons */}
        <div className="flex flex-col items-center space-y-4">
          <Link
            href="/seeds"
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg shadow-md transition"
          >
            🌱 Browse Seeds
          </Link>
          <Link
            href="/fertilizers"
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg shadow-md transition"
          >
            📦 Browse Fertilizers
          </Link>
          <Link
            href="/crops"
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg shadow-md transition"
          >
            🌾 Browse Crops
          </Link>
          <Link
            href="/live-rates"
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg shadow-md transition"
          >
            📈 View Live Market Rates
          </Link>
        </div>
      </section>
    </main>
  );
}
