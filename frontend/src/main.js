import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import GiftsView from './views/GiftsView.vue'
import SurveyView from './views/SurveyView.vue'
import ResultsView from './views/ResultsView.vue'
import AdminView from './views/AdminView.vue'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: GiftsView },
    { path: '/survey', component: SurveyView },
    { path: '/results/:id', component: ResultsView, props: true },
    { path: '/admin-reports', component: AdminView }
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')
