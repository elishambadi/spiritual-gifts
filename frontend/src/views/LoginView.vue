<template>
  <div class="login-container">
    <div class="card login-card">
      <h2>Admin Login</h2>
      <p style="color: var(--text-secondary); margin-bottom: 2rem;">
        Please enter the admin password to access the reports dashboard.
      </p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Enter admin password"
            :disabled="loading"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading || !password">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../store/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const { checkAdmin } = useAuth()
    const password = ref('')
    const error = ref(null)
    const loading = ref(false)

    const handleLogin = async () => {
      loading.value = true
      error.value = null

      // Small delay to show loading state
      await new Promise(resolve => setTimeout(resolve, 500))

      if (checkAdmin(password.value)) {
        router.push('/admin-reports')
      } else {
        error.value = 'Invalid password. Please try again.'
        loading.value = false
      }
    }

    return {
      password,
      error,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  max-width: 450px;
  width: 100%;
}

.error-message {
  color: var(--accent-color);
  background: rgba(245, 101, 101, 0.1);
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
</style>
