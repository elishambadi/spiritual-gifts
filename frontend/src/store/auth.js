import { reactive } from 'vue'

const state = reactive({
  isAdmin: false,
  adminPassword: null
})

export const useAuth = () => {
  const checkAdmin = (password) => {
    // Simple password check - in production, use proper authentication
    const ADMIN_PASSWORD = 'parklandsadmin2024'
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
