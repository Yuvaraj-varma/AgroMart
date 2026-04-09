"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useCart } from "../../context/CartContext";
import { API_URL } from "../../lib/api";

export default function CartPage() {
  const { cartItems, removeFromCart, clearCart } = useCart();
  const [showPaymentOptions, setShowPaymentOptions] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState("");
  const [loading, setLoading] = useState(false);
  const [buyerName, setBuyerName] = useState("Guest Buyer");

  // ✅ Get buyer name from localStorage (if logged in)
  useEffect(() => {
    const storedName =
      localStorage.getItem("buyerName") || localStorage.getItem("userName");
    if (storedName) setBuyerName(storedName);
  }, []);

  // ---------- Helpers ----------
  // Parse first numeric value from a string (handles "₹18 / 1 kg", "18", "18.5", "1,200")
  function extractFirstNumber(raw) {
    if (raw === undefined || raw === null) return null;
    if (typeof raw === "number") return raw;
    const s = String(raw);
    // find first number (integer or float), allow commas and dots
    const m = s.match(/[-+]?\d{1,3}(?:[,\d{3}]*\d)?(?:[.,]\d+)?|[-+]?\d+([.,]\d+)?/);
    if (!m) return null;
    const numStr = m[0].replace(/,/g, "."); // change commas to dot for locales like 1,234 -> 1.234
    const num = parseFloat(numStr);
    return Number.isFinite(num) ? num : null;
  }

  // Quantity parsing: "1 kg", "2kg", "2 bags", "1.5", "500 g" -> numeric value (500 for "500 g")
  function parseQuantity(raw) {
    if (raw === undefined || raw === null) return 1;
    if (typeof raw === "number") return Number(raw);
    const n = extractFirstNumber(raw);
    if (n === null) return 1;
    return n;
  }

  // Price parsing: robust search across fields and fallback to regex
  function parsePriceFromItem(item) {
    // candidate fields to check (common conventions)
    const candidates = [
      item.price,
      item.totalPrice,
      item.unitPrice,
      item.pricePerUnit,
      item.price_text,
      item.priceText,
      item.meta && item.meta.price,
      item.raw && item.raw.price,
      item.raw && item.raw.priceText,
    ];

    // 1) try each candidate directly
    for (const c of candidates) {
      if (c === undefined || c === null) continue;
      const num = extractFirstNumber(c);
      if (num !== null) return num;
    }

    // 2) sometimes price is embedded in "₹18 / 1 kg" inside description
    if (item.description) {
      const num = extractFirstNumber(item.description);
      if (num !== null) return num;
    }

    // 3) fallback: check entire item object as string
    const asString = JSON.stringify(item);
    const num = extractFirstNumber(asString);
    if (num !== null) return num;

    // 4) last fallback: 0 (and we'll log)
    console.warn("CartPage: could not parse price for item:", item);
    return 0;
  }

  // Normalize items to safe numeric format
  function normalizeItems(items) {
    return items.map((item, index) => {
      const quantity = parseQuantity(item.quantity ?? item.qty ?? item.count ?? 1);
      const price = parsePriceFromItem(item);
      const itemTotal = +(price * quantity || 0);
      // If price is 0, log to help debugging (so you can fix add-to-cart)
      if (price === 0) {
        console.warn(`[Cart] parsed price 0 for item index=${index}, name=${item.name}`, item);
      }
      return {
        product_id: item.id || item._id || `product-${index + 1}`,
        name: item.name || "Unknown",
        quantity,
        price,
        itemTotal,
        raw: item,
      };
    });
  }

  const normalized = normalizeItems(cartItems || []);
  const total = normalized.reduce((s, it) => s + it.itemTotal, 0);

  // ---------- Send order to backend ----------
  const sendOrderToBackend = async () => {
    const orderPayload = {
      buyer_name: buyerName,
      items: normalized.map((it) => ({
        product_id: it.product_id,
        name: it.name,
        quantity: Number(it.quantity),
        price: Number(it.price),
      })),
      total_price: Number(total),
      currency: "INR",
      metadata: { payment_method: paymentMethod },
    };

    try {
      const res = await fetch(`${API_URL}/api/orders/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderPayload),
      });

      const data = await res.json();

      if (res.ok) {
        alert(`✅ Order placed successfully via ${paymentMethod}!`);
        clearCart();
      } else {
        const errMsg = data?.detail ?? data ?? "Server error";
        alert(`❌ Failed: ${JSON.stringify(errMsg)}`);
      }
    } catch (error) {
      console.error("Error sending order:", error);
      alert("⚠️ Something went wrong while placing your order!");
    }
  };

  const handlePlaceOrder = async () => {
    if (!paymentMethod) {
      alert("⚠️ Please select a payment method!");
      return;
    }
    if (cartItems.length === 0) {
      alert("🛒 Your cart is empty!");
      return;
    }
    setLoading(true);
    await sendOrderToBackend();
    setLoading(false);
  };

  // ---------- UI ----------
  return (
    <main className="min-h-screen bg-green-50 text-gray-800 p-8">
      {/* Continue Shopping button styled as green button */}
      <div className="mb-6">
        <Link
          href="/"
          className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg shadow-md transition font-semibold inline-flex items-center"
        >
          ← Continue Shopping
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-green-700 mb-6 flex items-center gap-2">
        🛒 Your Cart
      </h1>

      {cartItems.length === 0 ? (
        <div className="text-center mt-20">
          <p className="text-lg text-gray-600 mb-4">Your cart is empty. Go shopping!</p>
          <Link
            href="/"
            className="bg-green-600 hover:bg-green-700 text-white px-5 py-3 rounded-lg shadow-md transition font-semibold"
          >
            Go Shopping
          </Link>
        </div>
      ) : (
        <>
          {/* Cart Items */}
          <div className="space-y-4">
            {normalized.map((it, index) => (
              <div
                key={index}
                className="flex justify-between items-center bg-white shadow-sm border border-green-100 rounded-lg p-4"
              >
                <div>
                  <h3 className="font-semibold text-lg text-green-700">{it.name}</h3>

                  {/* price badge (white text on green) */}
                  <div className="mt-2 inline-flex items-center gap-3">
                    <span className="bg-green-600 text-white px-3 py-1 rounded-lg font-semibold text-sm">
                      ₹{it.itemTotal.toFixed(2)}
                    </span>
                    <span className="text-gray-600 text-sm">
                      {it.quantity} × ₹{it.price.toFixed(2)}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() => removeFromCart(index)}
                    className="bg-red-500 hover:bg-red-600 text-white px-4 py-1 rounded-lg font-semibold shadow-md transition"
                    aria-label={`Remove ${it.name}`}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Total + Payment */}
          <div className="mt-8 border-t pt-4">
            <p className="text-xl font-bold mb-3 text-right text-green-800">
              Total: <span className="text-green-700 font-extrabold">₹{total.toFixed(2)}</span>
            </p>

            <div className="flex flex-col sm:flex-row justify-end gap-4 items-center">
              <button
                onClick={() => setShowPaymentOptions(!showPaymentOptions)}
                className="border border-green-600 text-green-600 px-4 py-2 rounded-lg font-semibold hover:bg-green-600 hover:text-white transition"
              >
                {showPaymentOptions ? "Hide Options" : "Payment Options"}
              </button>

              <button
                onClick={handlePlaceOrder}
                disabled={loading}
                className={`${
                  loading ? "bg-gray-400" : "bg-green-600 hover:bg-green-700"
                } text-white px-4 py-2 rounded-lg font-semibold shadow-md transition`}
              >
                {loading ? "Processing..." : "Place Order"}
              </button>
            </div>

            {/* Payment Options */}
            {showPaymentOptions && (
              <div className="mt-4 bg-white shadow-md rounded-lg p-4 w-full sm:w-1/3 float-right border border-green-100">
                <h3 className="font-semibold text-green-700 mb-3 text-center">Select Payment Method</h3>
                <div className="space-y-2 text-green-700">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="payment"
                      value="Bank Transfer"
                      checked={paymentMethod === "Bank Transfer"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    🏦 Bank Transfer
                  </label>

                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="payment"
                      value="UPI"
                      checked={paymentMethod === "UPI"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    💸 UPI Payment
                  </label>

                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="payment"
                      value="Cash on Delivery"
                      checked={paymentMethod === "Cash on Delivery"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    🚚 Cash on Delivery
                  </label>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </main>
  );
}
