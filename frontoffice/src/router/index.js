import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import User1 from '../views/User1.vue'
import User2 from '../views/User2.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/user1',
    name: 'User1',
    component: User1
  },
  {
    path: '/user2',
    name: 'User2',
    component: User2
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router