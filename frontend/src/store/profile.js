import { defineStore } from "pinia";
import api from "../services/api";
import { ref } from "vue";
import { useAuthStore } from "./auth";

export const useProfileStore = defineStore("profile", () => {
  const user = ref(null);

  const initialLoading = ref(false);
  const updateLoading = ref(false);
  const deleteLoading = ref(false);
  const showDeleteModal = ref(false);
  const serverError = ref("");
  const success = ref("");

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

  async function updateProfile(userData) {
    try {
      updateLoading.value = true;
      serverError.value = "";
      success.value = "";

      const updatedUser = await api.request("/user/update", {
        method: "PATCH",
        body: JSON.stringify(userData),
      });
      
      user.value = updatedUser;
      
      success.value = "Данные успешно обновлены";

      setTimeout(() => (success.value = ""), 4000);
    } catch (e) {
      serverError.value = "Не удалось обновить данные";
      user.value = null;

      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      updateLoading.value = false;
    }
  }

  async function deleteProfile() {
    try {
      showDeleteModal.value = false
      deleteLoading.value = true;
      serverError.value = "";

      await api.request("/user/delete", {
        method: "DELETE",
        credentials: 'include'
      });

      const store = useAuthStore()
      store.deleteAccount()

    } catch (e) {
      serverError.value = "Не удалось удалить аккаунт";
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      deleteLoading.value = false;
    }
  }

  function openModal() {
    showDeleteModal.value = true
  }
  function closeModal() {
    showDeleteModal.value = false
  }

  return {
    user,
    initialLoading,
    updateLoading,
    deleteLoading,
    showDeleteModal,
    serverError,
    success,
    getProfile,
    updateProfile,
    deleteProfile,
    openModal, 
    closeModal
  };
});
