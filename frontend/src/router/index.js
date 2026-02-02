import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "registration",
      component: () => import("@/pages/RegistrationPage.vue"),
      meta: { requiresAuth: false },
    },
  ],
});

export default router;
