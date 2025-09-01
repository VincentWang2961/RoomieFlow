import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    initialized: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user
  },

  actions: {
    async initializeAuth() {
      if (this.token) {
        try {
          await this.fetchUser()
        } catch (error) {
          this.logout()
        }
      }
      this.initialized = true
    },

    async login(credentials) {
      try {
        const response = await api.post('/auth/login', credentials)
        const { user, access_token } = response.data

        this.user = user
        this.token = access_token
        
        localStorage.setItem('token', access_token)
        
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Login failed'
        return { success: false, error: message }
      }
    },

    async register(userData) {
      try {
        const response = await api.post('/auth/register', userData)
        const { user, access_token } = response.data

        this.user = user
        this.token = access_token
        
        localStorage.setItem('token', access_token)
        
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Registration failed'
        return { success: false, error: message }
      }
    },

    async fetchUser() {
      try {
        const response = await api.get('/auth/me')
        this.user = response.data.user
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to fetch user'
        return { success: false, error: message }
      }
    },

    async refreshToken() {
      try {
        const response = await api.post('/auth/refresh')
        const { user, access_token } = response.data

        this.user = user
        this.token = access_token
        
        localStorage.setItem('token', access_token)
        
        return { success: true }
      } catch (error) {
        this.logout()
        return { success: false }
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})