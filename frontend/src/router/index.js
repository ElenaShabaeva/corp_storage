import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../store/auth";
import { useProfileStore } from "../store/profile";
import { useProjectsStore } from "../store/projects";

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
        {
          path: "documents",
          name: "documents",
          component: () => import("@/pages/project/DocumentsPage.vue"),
        },
      ],
    },
    {
      path: "/notification",
      name: "notification",
      component: () => import("@/pages/notifications/NotificationPage.vue"),
      meta: {requiresAuth: true},
      children: [
        {
          path: "",
          redirect: {name: 'messages'}
        },
        {
          path: "messages",
          name: "messages",
          component: () => import("@/pages/notifications/MessagesPage.vue")
        },
        {
          path: "invites",
          name: "invites",
          component: () => import("@/pages/notifications/InvitesPage.vue")
        }
      ]
    }
  ],
});

// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore();
//   const profileStore = useProfileStore()
//   const projectsStore = useProjectsStore()

//   authStore.serverError = ''
//   profileStore.serverError = ''
//   projectsStore.serverError = ''

//   profileStore.success = ''
//   projectsStore.success = ''

//   if (to.meta.requiresAuth && !authStore.token) {
//     next({
//       name: "login",
//       query: { redirect: to.fullPath },
//     });
//     return;
//   }

//   if (authStore.token && (to.name === "login" || to.name === "registration")) {
//     next({ name: "projects" });
//     return;
//   }

//   next();
// });

export default router;
