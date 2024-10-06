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
  {
    path: "/metrics/screen-time",
    name: "screen-time",
    component: () => import("@/views/metrics/screenTime.vue"),
  },
  {
    path: "/metrics/hire-quality",
    name: "hire-quality",
    component: () => import("@/views/metrics/hireQuality.vue"),
  },
  {
    path: "/metrics/average-hire-time",
    name: "average-hire-time",
    component: () => import("@/views/metrics/averageHire.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
