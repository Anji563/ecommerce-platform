"use client";

import { useState } from "react";
import axios from "axios";
import { useCartStore } from "@/store/useCartStore";

export default function ShoppingCart() {
  const cart = useCartStore((state: any) => state.cart);
  const clearCart = useCartStore((state: any) => state.clearCart);

  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("");

  const total = cart.reduce((sum: number, item: any) => sum + item.price * item.quantity, 0);

  const handleCheckout = async () => {
    if (!email) return alert("Please enter email");
    setStatus("Processing order...");
    try {
      const items = cart.map((i: any) => ({ product_id: i.id, quantity: i.quantity }));
      const res = await axios.post("http://localhost:8000/api/checkout", { user_email: email, items });
      setStatus(`Order placed! Order ID: ${res.data.order_id}`);
      clearCart();
    } catch (err) {
      setStatus("Checkout failed.");
    }
  };

  return (
    <div style={{ padding: "20px 0", borderTop: "2px solid #eee", marginTop: "20px" }}>
      <h2>Cart</h2>
      {cart.map((item: any) => (
        <div key={item.id}>
          {item.name} x {item.quantity} - ${(item.price * item.quantity).toFixed(2)}
        </div>
      ))}
      <h3>Total: ${total.toFixed(2)}</h3>
      <input
        type="email"
        placeholder="Enter email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ padding: "8px", marginRight: "10px" }}
      />
      <button onClick={handleCheckout} style={{ padding: "8px 16px", cursor: "pointer" }}>
        Checkout
      </button>
      {status && <p style={{ marginTop: "10px", fontWeight: "bold" }}>{status}</p>}
    </div>
  );
}
