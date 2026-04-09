"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { API_URL } from "../../lib/api";

export default function SignupPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("buyer");
  const [errors, setErrors] = useState({});
  const router = useRouter();

  function validate() {
    const errs = {};
    if (name.trim().length < 2)   errs.name     = "Name must be at least 2 characters";
    if (!email.includes("@"))     errs.email    = "Enter a valid email address";
    if (password.length < 6)      errs.password = "Password must be at least 6 characters";
    return errs;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) { setErrors(errs); return; }
    setErrors({});

    try {
      const res = await fetch(`${API_URL}/api/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, role }),
      });

      if (!res.ok) {
        const err = await res.json();
        alert(err.detail || "Signup failed. Try again!");
        return;
      }

      // ✅ If signup succeeded, auto-login the user
      const loginForm = new FormData();
      loginForm.append("username", email);
      loginForm.append("password", password);

      const loginRes = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        body: loginForm,
      });

      if (!loginRes.ok) {
        alert("✅ Registered successfully! Please login manually.");
        router.push("/login");
        return;
      }

      const loginData = await loginRes.json();

      // ✅ Save user data in localStorage
      localStorage.setItem("token", loginData.access_token);
      localStorage.setItem("role", role);
      localStorage.setItem("userName", name);

      alert(`🎉 Welcome to AgroMart, ${name}! (${role})`);
      router.push("/"); // Redirect to homepage

    } catch (error) {
      console.error("❌ Signup error:", error);
      alert("Something went wrong during signup.");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-green-50">
      <form
        onSubmit={handleSubmit}
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
          📝 Sign up for AgroMart
        </h2>

        <input
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full mb-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          required
        />
        {errors.name && <p className="text-red-500 text-sm mb-3">{errors.name}</p>}

        <input
          placeholder="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          required
        />
        {errors.email && <p className="text-red-500 text-sm mb-3">{errors.email}</p>}

        <input
          placeholder="Password (min 6 characters)"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          required
        />
        {errors.password && <p className="text-red-500 text-sm mb-3">{errors.password}</p>}

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full mb-6 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
        >
          <option value="buyer">Buyer</option>
          <option value="vendor">Vendor</option>
        </select>

        <button
          type="submit"
          className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition"
        >
          Sign Up
        </button>

        <p className="text-center text-gray-600 mt-4">
          Already have an account?{" "}
          <span
            onClick={() => router.push("/login")}
            className="text-green-700 font-semibold cursor-pointer hover:underline"
          >
            Login
          </span>
        </p>
      </form>
    </main>
  );
}
