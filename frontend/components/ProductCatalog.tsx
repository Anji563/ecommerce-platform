'use client';

import { useState, useEffect } from 'react';
import { useCartStore, Product } from '@/store/useCartStore';

export default function ProductCatalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const addToCart = useCartStore((state) => state.addToCart);

  useEffect(() => {
    const fetchProducts = async () => {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (category) params.append('category', category);

      try {
        const res = await fetch(`http://localhost:8000/api/v1/products?${params.toString()}`);
        if (res.ok) {
          const data = await res.json();
          setProducts(data);
        }
      } catch (error) {
        console.error("Failed to load products", error);
      }
    };

    const timer = setTimeout(fetchProducts, 300);
    return () => clearTimeout(timer);
  }, [search, category]);

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          placeholder="Search products..."
          className="border p-2 rounded-md w-full text-black"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="border p-2 rounded-md text-black min-w-[200px]"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
        </select>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.id} className="border rounded-lg p-4 shadow-sm bg-white flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-gray-800">{product.title}</h3>
              <p className="text-gray-600">${product.price.toFixed(2)}</p>
              <p className="text-sm text-gray-400 mt-1">In Stock: {product.stock}</p>
            </div>
            <button
              onClick={() => addToCart(product)}
              className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-md transition"
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}