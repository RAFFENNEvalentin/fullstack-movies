import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000
})

// Interceptors simples (logs erreurs réseau en dev)
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (import.meta.env.DEV) {
      console.error('[API ERROR]', err?.response?.status, err?.response?.data || err.message)
    }
    return Promise.reject(err)
  }
)