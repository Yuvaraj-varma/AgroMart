"use client";
import Link from "next/link";

export default function LiveRatesHome() {
  return (
    <main className="min-h-screen bg-green-50 text-gray-800 flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold text-green-700 mb-4">🌾 View Live Market Rates</h1>
      <p className="text-gray-600 mb-10 text-center max-w-lg">
        Check the latest mandi prices for crops and seeds updated daily from Agmarknet.
      </p>

      <div className="flex flex-col sm:flex-row gap-6">
        <Link
          href="/live-rates/crop"
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-md text-lg font-semibold transition"
        >
          🌿 View Crop Rates
        </Link>

        <Link
          href="/live-rates/seed"
          className="bg-yellow-600 hover:bg-yellow-700 text-white px-6 py-3 rounded-xl shadow-md text-lg font-semibold transition"
        >
          🌱 View Seed Rates
        </Link>
      </div>

      <Link
        href="/"
        className="mt-10 text-green-700 hover:underline font-medium"
      >
        ← Back to Home
      </Link>
    </main>
  );
}
