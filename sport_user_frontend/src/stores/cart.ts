import { defineStore } from 'pinia'

interface CartState {
  cartCount: number
}

export const useCartStore = defineStore('cart', {
  state: (): CartState => ({
    cartCount: 0,
  }),

  getters: {
    hasItems: (state) => state.cartCount > 0,
  },

  actions: {
    setCartCount(count: number) {
      this.cartCount = Math.max(0, count)
    },

    increaseCartCount(step = 1) {
      this.cartCount += step
    },

    decreaseCartCount(step = 1) {
      this.cartCount = Math.max(0, this.cartCount - step)
    },

    clearCartCount() {
      this.cartCount = 0
    },
  },
})