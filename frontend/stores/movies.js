import { defineStore } from 'pinia'
import { api } from '@/lib/api'

export const useMoviesStore = defineStore('movies', {
  state: () => ({
    items: [],        // films de la page courante
    count: 0,         // total de films
    page: 1,          // page courante (1-based)
    selected: null,   // film détaillé (ou null)
    loading: false,
    error: null
  }),

  getters: {
    totalPages: (s) => Math.max(1, Math.ceil((s.count || 0) / 5)), // page size backend = 5
    hasError: (s) => !!s.error
  },

  actions: {
    _start()  { this.loading = true; this.error = null },
    _fail(e)  { this.error = e?.response?.data || e?.message || 'Unknown error' },
    _end()    { this.loading = false },

    async fetchMovies(page = 1) {
      this._start()
      try {
        const { data } = await api.get('/movies/', { params: { page } })
        this.items = data.results || []
        this.count = data.count ?? 0
        this.page  = page
      } catch (e) {
        this._fail(e)
      } finally {
        this._end()
      }
    },

    async fetchMovie(id) {
      this._start()
      try {
        const { data } = await api.get(`/movies/${id}/`)
        this.selected = data
        return data
      } catch (e) {
        this._fail(e)
        this.selected = null
        throw e
      } finally {
        this._end()
      }
    },

    async addReview(id, grade) {
      this._start()
      try {
        await api.post(`/movies/${id}/reviews/`, { grade })
        // Après création, on recharge le détail pour rafraîchir average_grade
        await this.fetchMovie(id)
      } catch (e) {
        this._fail(e)
        throw e
      } finally {
        this._end()
      }
    },

    /**
     * payload attendu: { description?: string, actor_ids?: number[] }
     */
    async updateMovie(id, payload) {
      this._start()
      try {
        const { data } = await api.patch(`/movies/${id}/`, payload)
        // met à jour selected si c'est le même film
        if (this.selected && this.selected.id === id) {
          this.selected = data
        }
        // refresh partiel de la liste si le film courant est dedans
        const idx = this.items.findIndex(m => m.id === id)
        if (idx !== -1) {
          // garde les champs déjà présents et met à jour les modifiés
          this.items[idx] = { ...this.items[idx], ...data }
        }
        return data
      } catch (e) {
        this._fail(e)
        throw e
      } finally {
        this._end()
      }
    }
  }
})