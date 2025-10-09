import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Team1 from '../views/Team1.vue'
import Team2 from '../views/Team2.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/team1',
    name: 'Team1',
    component: Team1
  },
  {
    path: '/team2',
    name: 'Team2',
    component: Team2
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
