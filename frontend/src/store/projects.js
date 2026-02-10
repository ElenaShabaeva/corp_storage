import { defineStore } from "pinia";
import { ref } from "vue";

export const useProjectsStore = defineStore("projects", () => {
  const projects = ref(null);

  const showCreateModal = ref(false);

  function openCreateModal() {
    showCreateModal.value = true;
  }
  function closeCreateModal() {
    showCreateModal.value = false;
  }

  return {
    projects,
    showCreateModal,
    openCreateModal,
    closeCreateModal
  };
});
