import { createRouter, createWebHistory } from "vue-router";
import GameView from "../views/GameView.vue";
import TeamDashboard from "../components/TeamDashboard.vue";

const routes = [
  { path: "/", component: GameView },
  { path: "/team/:id", component: TeamDashboard },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
