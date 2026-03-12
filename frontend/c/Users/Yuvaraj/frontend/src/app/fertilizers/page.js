
import Link from "next/link";

export default function FertilizersPage() {
  return (
    <main className="min-h-screen bg-green-50 text-gray-800 p-8">
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-green-700">📦 Fertilizers Section</h1>
        <Link
          href="/"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </Link>
      </nav>

      <section className="text-center">
        <h2 className="text-3xl font-semibold mb-4">Available Fertilizers</h2>
        <p className="text-gray-600 mb-6">
          Browse or add fertilizers to enrich your soil.
        </p>
      </section>
    </main>
  );
}
