import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import GiftsView from './views/GiftsView.vue'
import SurveyView from './views/SurveyView.vue'
import ResultsView from './views/ResultsView.vue'
import AdminView from './views/AdminView.vue'
import LoginView from './views/LoginView.vue'
import { useAuth } from './store/auth'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: GiftsView },
    { path: '/survey', component: SurveyView },
    { path: '/results/:id', component: ResultsView, props: true },
    { path: '/login', component: LoginView },
    { 
      path: '/admin-reports', 
      component: AdminView,
      meta: { requiresAuth: true }
    }
  ]
})

// Initialize auth on app start
const { initAuth, state } = useAuth()
initAuth()

// Navigation guard to protect admin route
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !state.isAdmin) {
    next('/login')
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.mount('#app')
