import { defineStore } from "pinia";
import api from "../services/api";
import { ref } from "vue";

export const useProfileStore = defineStore("profile", () => {
  const user = ref(null);

  const initialLoading = ref(false);

  async function getProfile() {
    try {
      initialLoading.value = true;

      user.value = await api.request("/user/profile");
    } catch (e) {
      user.value = null;
    } finally {
      initialLoading.value = false;
    }
  }

  return { user, initialLoading, getProfile };
});
