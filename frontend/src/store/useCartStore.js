import { create } from "zustand";

export const useCartStore = create((set) => ({
  cart: [],
  addItem: (product) =>
    set((state) => {
      const existing = state.cart.find((i) => i.id === product.id);
      if (existing) {
        return {
          cart: state.cart.map((i) =>
            i.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
          ),
        };
      }
      return { cart: [...state.cart, { ...product, quantity: 1 }] };
    }),
  clearCart: () => set({ cart: [] }),
}));
