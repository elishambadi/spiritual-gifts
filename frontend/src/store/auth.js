import { reactive } from 'vue'

const state = reactive({
  isAdmin: false,
  adminPassword: null
})

export const useAuth = () => {
  const checkAdmin = (password) => {
    const ADMIN_PASSWORD = import.meta.env.VITE_ADMIN_PASSWORD || 'admin123' // Default password for development
    if (password === ADMIN_PASSWORD) {
      state.isAdmin = true
      state.adminPassword = password
      localStorage.setItem('adminAuth', password)
      return true
    }
    return false
  }

  const logout = () => {
    state.isAdmin = false
    state.adminPassword = null
    localStorage.removeItem('adminAuth')
  }

  const initAuth = () => {
    const savedAuth = localStorage.getItem('adminAuth')
    if (savedAuth) {
      checkAdmin(savedAuth)
    }
  }

  return {
    state,
    checkAdmin,
    logout,
    initAuth
  }
}
