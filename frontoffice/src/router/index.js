import { createRouter, createWebHistory } from 'vue-router';
import PageA from '../PageA.vue';
import PageB from '../PageB.vue';

const routes = [
  { path: '/', component: PageA },
  { path: '/page-b', component: PageB }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
