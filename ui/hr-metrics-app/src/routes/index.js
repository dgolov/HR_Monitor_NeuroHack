import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: "/",
    component: () => import("@/views/BarChart.vue"),
  },
  {
    path: "/candidates",
    name: "candidates",
    component: () => import("@/views/CandidatesPage.vue"),
  },
  {
    path: "/vacancies",
    name: "vacancies",
    component: () => import("@/views/VacanciesPage.vue"),
  },
  {
    path: "/interviews",
    name: "interviews",
    component: () => import("@/views/InterviewsPage.vue"),
  },
  {
    path: "/cabinet",
    name: "cabinet",
    component: () => import("@/views/CabinetPage.vue"),
  },
];

// Использование `createRouter` и `createWebHistory` для Vue 3
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
