import { defineStore } from 'pinia'
import { api } from '@/lib/api'

export const useActorsStore = defineStore('actors', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),
  getters: {
    // liste prête pour un select : { id, fullName }
    selectItems: (s) => s.items.map(a => ({
      id: a.id,
      fullName: `${a.first_name} ${a.last_name}`.trim()
    }))
  },
  actions: {
    async fetchActors() {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get('/actors/')
        this.items = Array.isArray(data) ? data : []
      } catch (e) {
        this.error = e?.response?.data || e?.message || 'Error loading actors'
      } finally {
        this.loading = false
      }
    }
  }
})