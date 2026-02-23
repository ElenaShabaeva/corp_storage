import { defineStore } from "pinia";
import { ref } from "vue";
import api from "../services/api";

export const useProjectsStore = defineStore("projects", () => {
  const projects = ref(null);
  const projectInfo = ref(null);
  const projectMembers = ref(null);
  const projectDocuments = ref([]);
  const projectOwner = ref(false);

  const showCreateModal = ref(false);
  const showInviteModal = ref(false);
  const showLeaveModal = ref(false);
  const showKickModal = ref(false);
  const showDeleteDocumentModal = ref(false);
  const showCreateDocumentModal = ref(false);
  const initialLoading = ref(false);
  const createLoading = ref(false);
  const infoLoading = ref(false);
  const membersLoading = ref(false);
  const inviteLoading = ref(false);
  const leaveLoading = ref(false);
  const kickLoading = ref(false);
  const createDocumentLoading =  ref(false);
  const documentsLoading = ref(false);
  const serverError = ref("");
  const success = ref("");

  const currentProject = ref(null);
  const currentMember = ref(null);
  const currentDocument = ref(null);

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
      infoLoading.value = true;
      const data = await api.request(`/project?project_id=${id}`);
      serverError.value = "";

      projectInfo.value = data;
      projectOwner.value = data.isOwner;
    } catch (e) {
      serverError.value = "Не удалось загрузить данные проекта";
      setTimeout(() => (serverError.value = ""), 4000);
      projectInfo.value = null;
    } finally {
      infoLoading.value = false;
    }
  }

  async function getProjectMembers(id) {
    try {
      membersLoading.value = true;
      const data = await api.request(`/project/members?project_id=${id}`);
      serverError.value = "";

      projectMembers.value = data;
    } catch (e) {
      serverError.value = "Не удалось загрузить участников";
      setTimeout(() => (serverError.value = ""), 4000);
      projectMembers.value = null;
    } finally {
      membersLoading.value = false;
    }
  }

  async function inviteMember(id, nickname) {
    try {
      showInviteModal.value = false;
      inviteLoading.value = true;
      serverError.value = "";

      const data = await api.request("/project/invite", {
        method: "POST",
        body: JSON.stringify({
          login: nickname,
          project_id: id,
        }),
      });

      success.value = `Отправлено приглашение '${nickname}'`;

      setTimeout(() => (success.value = ""), 4000);
    } catch (e) {
      if (e.message?.includes("409") || e.status === 409) {
        serverError.value = `Участник '${nickname}' уже добавлен в проект`;
      } else {
        serverError.value = `Не удалось добавить '${nickname}': ${e.message}`;
      }
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      inviteLoading.value = false;
    }
  }

  async function leaveProject() {
    try {
      showLeaveModal.value = false;
      leaveLoading.value = true;
      serverError.value = "";

      const data = await api.request(
        `/project/leave?project_id=${currentProject.value.id}`,
      );

      if (projects.value) {
        const projectIndex = projects.value.findIndex(
          (p) => p.id === currentProject.value.id,
        );

        if (projectIndex !== -1) {
          projects.value.splice(projectIndex, 1);
        }

        localStorage.setItem("projects", JSON.stringify(projects.value));
      } else {
        localStorage.removeItem("projects");
      }

      success.value = `Вы покинули проект '${currentProject.value.name}'`;
      setTimeout(() => (success.value = ""), 4000);
    } catch (e) {
      serverError.value = `Не удалось покинуть проект '${currentProject.value.name}'`;
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      leaveLoading.value = false;
      currentProject.value = null;
    }
  }

  async function kickProject(id) {
    try {
      showKickModal.value = false;
      kickLoading.value = true;
      serverError.value = "";

      const data = await api.request("/project/kick", {
        method: "POST",
        body: JSON.stringify({
          login: currentMember.value,
          project_id: id,
        }),
      });

      console.log(data);

      success.value = `'${currentMember.value}' исключен из проекта`;
      setTimeout(() => (success.value = ""), 4000);
    } catch (e) {
      serverError.value = `Не удалось исключить из проекта '${currentMember.value}'`;
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      kickLoading.value = false;
      currentMember.value = null;
    }
  }

  async function getDocuments(id) {
    try {
      documentsLoading.value = true;
      const data = await api.request(`/project/${id}/documents/all`);
      projectDocuments.value = data.documents;

    } catch (e) {
      serverError.value = "Не удалось загрузить документы"
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      documentsLoading.value = false;
    }
  }

  async function createDocument(id, name) {
    try {
      createDocumentLoading.value = true
      showCreateDocumentModal.value = false
      const data = await api.request(
        `/project/${id}/documents?file_name=${name}`,
        {
          method: "POST",
        },
      );

      projectDocuments.value = [
        data,
        ...projectDocuments.value
      ]

    } catch (e) {
      if (e.message?.includes("409") || e.status === 409) {
        serverError.value = 'Такой документ есть или с таким названием нельзя создать документ';
      } else {
        serverError.value = 'Не удалось создать документ';
      }
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      currentDocument.value = null;
      createDocumentLoading.value = false
    }
  }

  async function deleteDocument(id) {
    try {
      showDeleteDocumentModal.value = false;
      const data = await api.request(
        `/project/${id}/documents?document_id=${currentDocument.value}`,
        {
          method: "DELETE",
        },
      );

      projectDocuments.value = projectDocuments.value.filter(
        (d) => d.id !== currentDocument.value,
      );
    } catch (e) {
      if (e.message?.includes("403") || e.status === 403) {
        serverError.value = 'Вы не можете удалить документ';
      } else {
        serverError.value = 'Не удалось удалить документ';
      } 
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      currentDocument.value = null;
    }
  }

  function openCreateModal() {
    showCreateModal.value = true;
  }
  function closeCreateModal() {
    showCreateModal.value = false;
  }

  function openInviteModal() {
    showInviteModal.value = true;
  }
  function closeInviteModal() {
    showInviteModal.value = false;
  }

  function openLeaveModal(project) {
    currentProject.value = project;
    showLeaveModal.value = true;
  }
  function closeLeaveModal() {
    currentProject.value = null;
    showLeaveModal.value = false;
  }

  function openKickModal(member) {
    currentMember.value = member;
    showKickModal.value = true;
  }
  function closeKickModal() {
    currentMember.value = null;
    showKickModal.value = false;
  }

  function openShowDeleteDocumentModal(id) {
    showDeleteDocumentModal.value = true;
    currentDocument.value = id;
  }
  function closeShowDeleteDocumentModal() {
    showDeleteDocumentModal.value = false;
    currentDocument.value = null;
  }

  function openCreateDocumentModal() {
    showCreateDocumentModal.value = true
  }
  function closeCreateDocumentModal() {
    showCreateDocumentModal.value = false
  }

  return {
    projects,
    projectInfo,
    projectOwner,
    projectMembers,
    projectDocuments,
    showCreateModal,
    showInviteModal,
    showLeaveModal,
    showKickModal,
    showCreateDocumentModal,
    showDeleteDocumentModal,
    initialLoading,
    createLoading,
    infoLoading,
    membersLoading,
    inviteLoading,
    leaveLoading,
    kickLoading,
    createDocumentLoading,
    documentsLoading,
    serverError,
    success,
    getProjects,
    createProject,
    getProjectInfo,
    getProjectMembers,
    inviteMember,
    leaveProject,
    kickProject,
    getDocuments,
    createDocument,
    deleteDocument,
    openCreateModal,
    closeCreateModal,
    openInviteModal,
    closeInviteModal,
    openLeaveModal,
    closeLeaveModal,
    openKickModal,
    closeKickModal,
    openCreateDocumentModal,
    closeCreateDocumentModal,
    openShowDeleteDocumentModal,
    closeShowDeleteDocumentModal,
    currentMember,
  };
});
