"use client";
import { createContext, useContext, useState } from "react";

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cartItems, setCartItems] = useState([]);

  // 🛒 Add to Cart with quantity and totalPrice support
  const addToCart = (item) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find(
        (i) => i.name === item.name && i.quantity === item.quantity
      );

      if (existingItem) {
        // If same item + same quantity exists → increase total
        return prevItems.map((i) =>
          i.name === item.name && i.quantity === item.quantity
            ? { ...i, totalPrice: i.totalPrice + item.totalPrice }
            : i
        );
      } else {
        // Else add as new item
        return [...prevItems, item];
      }
    });
  };

  // ❌ Remove item by index
  const removeFromCart = (index) => {
    setCartItems((prevItems) => prevItems.filter((_, i) => i !== index));
  };

  // 🧹 Clear all items
  const clearCart = () => setCartItems([]);

  // 💰 Calculate total amount (sum of totalPrice)
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
