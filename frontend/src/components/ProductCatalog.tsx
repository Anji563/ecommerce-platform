"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { useCartStore } from "@/store/useCartStore";

interface Product {
  id: number;
  name: string;
  price: number;
}

export default function ProductCatalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const addItem = useCartStore((state: any) => state.addItem);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/products")
      .then((res) => {
        const data = Array.isArray(res.data) ? res.data : res.data?.products || [];
        setProducts(data);
      })
      .catch((err) => {
        console.error("Failed to fetch products:", err);
        setProducts([]);
      });
  }, []);

  return (
    <div style={{ padding: "20px 0" }}>
      <h2>Products</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px" }}>
        {Array.isArray(products) &&
          products.map((p) => (
            <div key={p.id} style={{ border: "1px solid #ccc", padding: "15px", borderRadius: "8px" }}>
              <h3>{p.name}</h3>
              <p>${p.price?.toFixed(2)}</p>
              <button onClick={() => addItem(p)} style={{ padding: "8px 16px", cursor: "pointer" }}>
                Add to Cart
              </button>
            </div>
          ))}
      </div>
    </div>
  );
}
