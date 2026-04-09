"use client";
import { createContext, useContext, useState, useEffect } from "react";

const CartContext = createContext();

export function CartProvider({ children }) {
  // ✅ Load cart from localStorage on first render
  const [cartItems, setCartItems] = useState(() => {
    if (typeof window === "undefined") return [];
    try {
      const stored = localStorage.getItem("cartItems");
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  // ✅ Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem("cartItems", JSON.stringify(cartItems));
  }, [cartItems]);

  // 🛒 Add to Cart
  const addToCart = (item) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find(
        (i) => i.name === item.name && i.quantity === item.quantity
      );
      if (existingItem) {
        return prevItems.map((i) =>
          i.name === item.name && i.quantity === item.quantity
            ? { ...i, totalPrice: i.totalPrice + item.totalPrice }
            : i
        );
      }
      return [...prevItems, item];
    });
  };

  // ❌ Remove item by index
  const removeFromCart = (index) => {
    setCartItems((prevItems) => prevItems.filter((_, i) => i !== index));
  };

  // 🧹 Clear all items
  const clearCart = () => {
    setCartItems([]);
    localStorage.removeItem("cartItems");
  };

  // 💰 Calculate total amount
  const totalAmount = cartItems.reduce(
    (sum, item) => sum + (item.totalPrice || item.price || 0),
    0
  );

  return (
    <CartContext.Provider
      value={{ cartItems, addToCart, removeFromCart, clearCart, totalAmount }}
    >
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => useContext(CartContext);
