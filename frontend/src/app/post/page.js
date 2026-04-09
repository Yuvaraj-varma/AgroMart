"use client";
import { useState } from "react";
import Link from "next/link";
import { API_URL } from "../../lib/api";

export default function PostProductPage() {
  const [formData, setFormData] = useState({
    name: "",
    category: "", // ✅ seeds / fertilizers / crops
    type: "",
    price: "",
    description: "",
    image: null,
    farmer_name: "",
    location: "",
  });

  const [preview, setPreview] = useState(null);

  // ✅ Handle input changes
  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (files && files[0]) {
      setFormData({ ...formData, [name]: files[0] });
      setPreview(URL.createObjectURL(files[0])); // 👀 Preview image
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  // ✅ Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = new FormData();
      data.append("name", formData.name);
      data.append("type", formData.type);
      data.append("price", formData.price);
      data.append("description", formData.description);
      data.append("farmer_name", formData.farmer_name);
      data.append("location", formData.location);
      if (formData.image) data.append("image", formData.image);

      const endpoint = formData.category || "crops";

      const response = await fetch(`${API_URL}/api/${endpoint}/`, {
        method: "POST",
        body: data,
      });

      if (response.ok) {
        alert(`✅ ${formData.category} uploaded successfully!`);
        setFormData({
          name: "",
          category: "",
          type: "",
          price: "",
          description: "",
          image: null,
          farmer_name: "",
          location: "",
        });
        setPreview(null);
      } else {
        alert("❌ Upload failed! Check backend logs.");
      }
    } catch (err) {
      console.error("Error uploading:", err);
      alert("⚠️ Something went wrong. Check console or backend logs.");
    }
  };

  return (
    <main className="min-h-screen bg-green-50 p-8 text-gray-800">
      {/* ✅ Navigation */}
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-green-700">🧑‍🌾 Post New Product</h1>
        <Link
          href="/"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
        >
          ← Back to Home
        </Link>
      </nav>

      {/* ✅ Form */}
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md max-w-lg mx-auto"
      >
        {/* Product Name */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Product Name</span>
          <input
            name="name"
            type="text"
            required
            value={formData.name}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
            placeholder="Enter product name"
          />
        </label>

        {/* Category Dropdown */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Category</span>
          <select
            name="category"
            required
            value={formData.category}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
          >
            <option value="">Select Category</option>
            <option value="crops">Crop</option>
            <option value="seeds">Seed</option>
            <option value="fertilizers">Fertilizer</option>
          </select>
        </label>

        {/* Type */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Type</span>
          <input
            name="type"
            type="text"
            value={formData.type}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
            placeholder="e.g., Organic / Hybrid / Nitrogen-based"
          />
        </label>

        {/* Price */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Price (₹)</span>
          <input
            name="price"
            type="number"
            required
            value={formData.price}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
            placeholder="e.g., 250"
          />
        </label>

        {/* Description */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Description</span>
          <textarea
            name="description"
            required
            value={formData.description}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
            placeholder="Write a short description"
          />
        </label>

        {/* ✅ Farmer Name */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Farmer Name</span>
          <input
            name="farmer_name"
            type="text"
            required
            value={formData.farmer_name}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
            placeholder="Enter your name"
          />
        </label>

        {/* ✅ Location */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Location</span>
          <input
            name="location"
            type="text"
            required
            value={formData.location}
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
            placeholder="Enter your location (e.g., Chennai, TN)"
          />
        </label>

        {/* Upload Image */}
        <label className="block mb-3">
          <span className="text-green-700 font-medium">Upload Image</span>
          <input
            name="image"
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="w-full mt-1 p-2 border rounded-md"
          />
        </label>

        {/* 👀 Image Preview */}
        {preview && (
          <div className="mt-3 mb-4">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-48 object-cover rounded-lg border"
            />
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg mt-4 font-semibold"
        >
          📤 Upload Product
        </button>
      </form>
    </main>
  );
}
