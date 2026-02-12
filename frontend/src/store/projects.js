import { defineStore } from "pinia";
import { ref } from "vue";
import api from "../services/api";

export const useProjectsStore = defineStore("projects", () => {
  const projects = ref(null);
  const projectInfo = ref(null);
  const projectMembers = ref(null);

  const showCreateModal = ref(false);
  const initialLoading = ref(false);
  const createLoading = ref(false);
  const infoLoading = ref(false);
  const membersLoading = ref(false);
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
      showCreateModal.value = false;
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

  async function getProjectInfo(id) {
    try {
      infoLoading.value = true
      const data = await api.request(`/project?project_id=${id}`);
      
      projectInfo.value = data;
    } catch (e) {
      serverError.value = 'Не удалось загрузить данные проекта'
      setTimeout(() => (serverError.value = ""), 4000);
      projectInfo.value = null
    } finally {
      infoLoading.value = false
    }
  }

  async function getProjectMembers(id) {
    try {
      membersLoading.value = true
      const data = await api.request(`/project/members?project_id=${id}`);
      
      projectMembers.value = data;
    } catch (e) {
      serverError.value = 'Не удалось загрузить участников'
      setTimeout(() => (serverError.value = ""), 4000);
      projectMembers.value = null
    } finally {
      membersLoading.value = false
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
    projectInfo,
    projectMembers,
    showCreateModal,
    initialLoading,
    createLoading,
    infoLoading,
    membersLoading,
    serverError,
    getProjects,
    createProject,
    getProjectInfo,
    getProjectMembers,
    openCreateModal,
    closeCreateModal,
  };
});
