"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";

export default function OrderSuccessPage() {
  const searchParams = useSearchParams();
  const orderId      = searchParams.get("order_id");
  const payment      = searchParams.get("payment");
  const total        = searchParams.get("total");
  const [time, setTime]   = useState("");

  useEffect(() => {
    setTime(new Date().toLocaleString());
  }, []);

  return (
    <main className="min-h-screen bg-green-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-lg p-10 max-w-md w-full text-center border border-green-100">

        {/* Success Icon */}
        <div className="text-6xl mb-4">✅</div>

        <h1 className="text-3xl font-bold text-green-700 mb-2">Order Placed!</h1>
        <p className="text-gray-600 mb-6">
          Thank you for shopping at <span className="font-semibold text-green-700">AgroMart</span>!
        </p>

        {/* Order Details */}
        <div className="bg-green-50 rounded-xl p-4 text-left space-y-3 mb-6 border border-green-100">
          {orderId && (
            <div className="flex justify-between">
              <span className="text-gray-500">Order ID</span>
              <span className="font-semibold text-gray-700 text-sm">{orderId.slice(0, 18)}...</span>
            </div>
          )}
          {payment && (
            <div className="flex justify-between">
              <span className="text-gray-500">Payment</span>
              <span className="font-semibold text-green-700">{payment}</span>
            </div>
          )}
          {total && (
            <div className="flex justify-between">
              <span className="text-gray-500">Total Paid</span>
              <span className="font-bold text-green-700 text-lg">₹{Number(total).toFixed(2)}</span>
            </div>
          )}
          {time && (
            <div className="flex justify-between">
              <span className="text-gray-500">Placed At</span>
              <span className="font-semibold text-gray-700 text-sm">{time}</span>
            </div>
          )}
        </div>

        {/* Payment Instructions */}
        {payment === "Bank Transfer" && (
          <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 text-left mb-6">
            <p className="font-semibold text-blue-700 mb-1">🏦 Bank Transfer Details</p>
            <p className="text-sm text-gray-600">Account: AgroMart Pvt Ltd</p>
            <p className="text-sm text-gray-600">Bank: State Bank of India</p>
            <p className="text-sm text-gray-600">IFSC: SBIN0001234</p>
            <p className="text-sm text-gray-600">Account No: 1234567890</p>
          </div>
        )}

        {payment === "UPI" && (
          <div className="bg-purple-50 border border-purple-100 rounded-xl p-4 text-left mb-6">
            <p className="font-semibold text-purple-700 mb-1">💸 UPI Payment</p>
            <p className="text-sm text-gray-600">UPI ID: agromart@upi</p>
            <p className="text-sm text-gray-600">Pay ₹{Number(total).toFixed(2)} to complete your order.</p>
          </div>
        )}

        {payment === "Cash on Delivery" && (
          <div className="bg-yellow-50 border border-yellow-100 rounded-xl p-4 text-left mb-6">
            <p className="font-semibold text-yellow-700 mb-1">🚚 Cash on Delivery</p>
            <p className="text-sm text-gray-600">Pay ₹{Number(total).toFixed(2)} when your order arrives.</p>
            <p className="text-sm text-gray-600">Expected delivery: 3-5 business days.</p>
          </div>
        )}

        {/* Buttons */}
        <div className="flex flex-col gap-3">
          <Link
            href="/"
            className="bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold transition"
          >
            🌾 Continue Shopping
          </Link>
          <Link
            href="/cart"
            className="border border-green-600 text-green-600 py-3 rounded-xl font-semibold hover:bg-green-50 transition"
          >
            🛒 View Cart
          </Link>
        </div>
      </div>
    </main>
  );
}
