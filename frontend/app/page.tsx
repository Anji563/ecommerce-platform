'use client';

import ProductCatalog from '@/components/ProductCatalog';
import { useCartStore } from '@/store/useCartStore';

export default function HomePage() {
  const cart = useCartStore((state) => state.cart);
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white border-b p-4 shadow-sm">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">Async E-Commerce</h1>
          <div className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full font-semibold">
            Cart Items: {totalItems}
          </div>
        </div>
      </header>
      <ProductCatalog />
    </main>
  );
}