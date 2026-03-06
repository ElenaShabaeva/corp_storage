import { defineStore } from "pinia";
import { computed, ref } from "vue";
import authService from "../services/auth.service";
import router from "../router";
import { useNotificationsStore } from "./notifications";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || null);
  const isLoggedIn = computed(() => !!token.value);

  const loading = ref(false);
  const serverError = ref("");
  const fieldError = ref("");

  const store = useNotificationsStore()

  async function registration(user) {
    try {
      loading.value = true;
      serverError.value = "";
      fieldError.value = "";

      const data = await authService.registration(user);
      token.value = data.token_info.token;
      localStorage.setItem("token", data.token_info.token);
      localStorage.setItem('username', user.login)

      router.push({ name: "profile" });
      await store.initialize();
    } catch (e) {
      if (e.message === 'Пользователь с таким "Логин" уже существует') {
        fieldError.value = e.message;
      } else {
        serverError.value = "Не удалось зарегистрироваться";
      }
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function authorization(user) {
    try {
      loading.value = true;
      serverError.value = "";
      fieldError.value = "";

      const data = await authService.authorization(user);
      token.value = data.token_info.token;
      localStorage.setItem("token", data.token_info.token);
      localStorage.setItem('username', user.login)

      router.push({ name: "projects" });
      await store.initialize();
    } catch (e) {
      if (e.message === "Неправильный логин или пароль") {
        fieldError.value = e.message;
      } else {
        serverError.value = "Не удалось войти в аккаунт";
      }
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    try {
      loading.value = true;
      serverError.value = "";

      await authService.logout();

      token.value = null;
      localStorage.removeItem("token");
      localStorage.removeItem('username')

      router.push({ name: "login" });
      
      store.disconnectSSE()
    } catch (e) {
      serverError.value = e.message;
    } finally {
      loading.value = false;
    }
  }

  async function refresh() {
    try {
      const data = await authService.refresh();

      const newToken = data.token_info.token;
      token.value = newToken;
      localStorage.setItem("token", newToken);

      return newToken;
    } catch (e) {
      token.value = null;
      localStorage.removeItem("token");

      router.push({ name: "login" });
    }
  }

  async function deleteAccount() {
    loading.value = false
    token.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem('username')

    router.push({ name: "login" });
  }

  return {
    token,
    isLoggedIn,
    registration,
    authorization,
    logout,
    refresh,
    deleteAccount,
    loading,
    serverError,
    fieldError,
  };
});
