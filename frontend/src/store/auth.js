import { defineStore } from "pinia";
import { computed, ref } from "vue";
import authService from "../services/auth.service";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || null)
  const isLoggedIn = computed(() => !!token.value)

  const loading = ref(false);
  const serverError = ref("");
  const fieldError = ref("");


  async function registration(user) {
    try {
      loading.value = true;
      serverError.value = "";
      fieldError.value = "";

      const data = await authService.registration(user);
      token.value = data.token_info.token
      localStorage.setItem("token", data.token_info.token)
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

  return { token, isLoggedIn, registration, loading, serverError, fieldError }
});
