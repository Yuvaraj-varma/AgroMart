"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  async function handleLogin(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/auth/login", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        alert(err.detail || "Invalid credentials");
        return;
      }

      const data = await res.json();

      // ✅ Save login details to localStorage
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);

      // ✅ Try fetching user info (to get name)
      try {
        const userRes = await fetch("http://127.0.0.1:8000/api/auth/me", {
          headers: {
            Authorization: `Bearer ${data.access_token}`,
          },
        });

        if (userRes.ok) {
          const userData = await userRes.json();
          if (userData && userData.name) {
            localStorage.setItem("userName", userData.name);
          } else {
            localStorage.setItem("userName", "Unknown");
          }
        } else {
          localStorage.setItem("userName", "Unknown");
        }
      } catch (err) {
        console.error("⚠️ Failed to fetch user info:", err);
        localStorage.setItem("userName", "Unknown");
      }

      // ✅ Greet based on role
      alert(`✅ Welcome ${data.role === "vendor" ? "Vendor" : "Buyer"}!`);
      router.push("/");

    } catch (error) {
      console.error("❌ Login failed:", error);
      alert("Something went wrong while logging in. Please try again.");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-green-50">
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-green-200 relative"
      >
        {/* 🔙 Back Button */}
        <Link
          href="/"
          className="absolute top-4 left-4 text-green-700 hover:text-green-800 font-semibold flex items-center space-x-1"
        >
          <span>←</span>
          <span>Back</span>
        </Link>

        <h2 className="text-2xl font-bold text-center text-green-700 mb-6 mt-2">
          🔐 Login to AgroMart
        </h2>

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-6 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          required
        />

        <button
          type="submit"
          className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition"
        >
          Login
        </button>

        <p className="text-center text-gray-600 mt-4">
          Don’t have an account?{" "}
          <span
            onClick={() => router.push("/signup")}
            className="text-green-700 font-semibold cursor-pointer hover:underline"
          >
            Sign up
          </span>
        </p>
      </form>
    </main>
  );
}
