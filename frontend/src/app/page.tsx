"use client";

import ProductCatalog from "@/components/ProductCatalog";
import ShoppingCart from "@/components/ShoppingCart";

export default function Home() {
  return (
    <main style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>E-Commerce Storefront</h1>
      <ProductCatalog />
      <ShoppingCart />
    </main>
  );
}
