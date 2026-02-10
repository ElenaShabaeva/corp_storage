import { defineStore } from "pinia";
import { ref } from "vue";
import api from "../services/api";

export const useProjectsStore = defineStore("projects", () => {
  const projects = ref(null);

  const showCreateModal = ref(false);
  const initialLoading = ref(false);
  const createLoading = ref(false);
  const serverError = ref("");

  const savedProjects = () => {
    try {
      const save = localStorage.getItem("projects");
      if (save) {
        projects.value = JSON.parse(save);
        return true;
      }
    } catch (e) {
      localStorage.removeItem("projects");
    }
    return false;
  };

  async function getProjects() {
    try {
      initialLoading.value = true;

      if (savedProjects()) {
        return projects.value;
      }
      const data = await api.request("/project/all");

      projects.value = data.projects;
      localStorage.setItem("projects", JSON.stringify(data.projects));
    } catch (e) {
      projects.value = null;
    } finally {
      initialLoading.value = false;
    }
  }

  async function createProject(project) {
    try {
      showCreateModal.value = false
      createLoading.value = true;
      serverError.value = "";

      const newProject = await api.request("/project", {
        method: "POST",
        body: JSON.stringify(project),
      });
      
      if (projects.value) {
        projects.value.unshift(newProject);
      } else {
        projects.value = [newProject];
      }

      localStorage.setItem("projects", JSON.stringify(projects.value));

    } catch (e) {
      serverError.value = "Не удалось создать проект";

      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      createLoading.value = false;
    }
  }

  function openCreateModal() {
    showCreateModal.value = true;
  }
  function closeCreateModal() {
    showCreateModal.value = false;
  }

  return {
    projects,
    showCreateModal,
    initialLoading,
    createLoading,
    serverError,
    getProjects,
    createProject,
    openCreateModal,
    closeCreateModal,
  };
});
