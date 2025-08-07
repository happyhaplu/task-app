import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/login.vue'
import Signup from '../views/signup.vue'
import Tasks from '../views/tasks.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/tasks', component: Tasks },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
