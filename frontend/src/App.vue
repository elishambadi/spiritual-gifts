<template>
  <div id="app">
    <header>
      <h1>Spiritual Gifts Survey</h1>
      <p>Discover your spiritual gifts through this comprehensive assessment</p>
      
      <nav class="header-nav">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">About Spiritual Gifts</router-link>
        <router-link to="/survey" class="nav-link" :class="{ active: $route.path === '/survey' }">Take Survey</router-link>
        <router-link v-if="authState.isAdmin" to="/admin-reports" class="nav-link" :class="{ active: $route.path === '/admin-reports' }">Admin Reports</router-link>
        <button v-if="authState.isAdmin" @click="handleLogout" class="nav-link logout-btn">Logout</button>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { useAuth } from './store/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const { state: authState, logout } = useAuth()
    const router = useRouter()

    const handleLogout = () => {
      logout()
      router.push('/')
    }

    return {
      authState,
      handleLogout
    }
  }
}
</script>

<style>
.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
