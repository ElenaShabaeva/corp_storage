import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../store/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/registration",
      name: "registration",
      component: () => import("@/pages/RegistrationPage.vue"),
      meta: { requiresAuth: false },
    },
    {
      path: "/",
      name: "login",
      component: () => import("@/pages/AuthorizationPage.vue"),
      meta: { requiresAuth: false },
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("@/pages/ProfilePage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/projects",
      name: "projects",
      component: () => import("@/pages/ProjectsPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/project/:id",
      name: "project",
      component: () => import("@/pages/project/ProjectPage.vue"),
      meta: { requiresAuth: true },
      children: [
        {
          path: "",
          redirect: { name: "members" },
        },
        {
          path: "members",
          name: "members",
          component: () => import("@/pages/project/MembersPage.vue"),
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const store = useAuthStore();

  if (to.meta.requiresAuth && !store.token) {
    next({
      name: "login",
      query: { redirect: to.fullPath },
    });
    return;
  }

  if (store.token && (to.name === "login" || to.name === "registration")) {
    next({ name: "projects" });
    return;
  }

  next();
});

export default router;
