import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { API_URL } from "../api.config";
import api from "../services/api";

export const useNotificationsStore = defineStore("notifications", () => {
  let abortController = null;
  let reconnectTimeout = null;
  const isConnected = ref(false);

  const notificationsInvites = ref([]);
  const notificationsMessages = ref([]);
  const serverError = ref("");

  const messagesLoading = ref(false);
  const invitesLoading = ref(false);

  const showAllMessagesDeleteModal = ref(false);
  const showAllInvitesDeleteModal = ref(false);

  async function getNotificationsMessages() {
    try {
      messagesLoading.value = true;
      const data = await api.request("/notification/messages");
      notificationsMessages.value = data.messages;
    } catch (e) {
      serverError.value = "Не удалось загрузить сообщения";
      notificationsMessages.value = [];
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      messagesLoading.value = false;
    }
  }

  async function messageRead(id) {
    try {
      const data = await api.request(
        `/notification/messages/read?message_id=${id}`,
        {
          method: "PATCH",
        },
      );

      const message = notificationsMessages.value.find((m) => m.id === id);
      if (message) {
        message.is_read = true;
      }
    } catch (e) {
      serverError.value = "Не удалось прочитать сообщение";
    }
  }

  async function messageDelete(id) {
    try {
      const data = await api.request(
        `/notification/messages/delete?message_id=${id}`,
        {
          method: "DELETE",
        },
      );

      notificationsMessages.value = notificationsMessages.value.filter(
        (m) => m.id !== id,
      );
    } catch (e) {
      serverError.value = "Не удалось удалить сообщение";
    }
  }

  async function allMessagesRead() {
    try {
      const data = await api.request("/notification/messages/read-all", {
        method: "PATCH",
      });

      notificationsMessages.value.forEach((m) => {
        if (!m.is_read) {
          m.is_read = true;
        }
      });
    } catch (e) {
      serverError.value = "Не удалось прочитать сообщения";
    }
  }

  async function allMessagesDelete() {
    try {
      showAllMessagesDeleteModal.value = false;
      const data = await api.request("/notification/messages/delete-all", {
        method: "DELETE",
      });

      notificationsMessages.value = notificationsMessages.value.filter(
        (m) => !m.is_read,
      );
    } catch (e) {
      serverError.value = "Не удалось удалить сообщения";
    }
  }

  async function getNotificationsInvites() {
    try {
      invitesLoading.value = true;
      const data = await api.request("/notification/invites");
      notificationsInvites.value = data.invites;
    } catch (e) {
      serverError.value = "Не удалось загрузить приглашения";
      notificationsInvites.value = [];
      setTimeout(() => (serverError.value = ""), 4000);
    } finally {
      invitesLoading.value = false;
    }
  }

  async function acceptInvite(id) {
    try {
      const data = await api.request(
        `/notification/invites/accept?invite_id=${id}`,
        {
          method: "POST",
        },
      );

      const invite = notificationsInvites.value.find((i) => i.id === id);
      if (invite) {
        invite.state = "Принято";
      }
    } catch (e) {
      serverError.value = "Не удалось принять приглашение";
    }
  }

  async function declineInvite(id) {
    try {
      const data = await api.request(
        `/notification/invites/decline?invite_id=${id}`,
        {
          method: "POST",
        },
      );

      const invite = notificationsInvites.value.find((i) => i.id === id);
      if (invite) {
        invite.state = "Отклонено";
      }
    } catch (e) {
      serverError.value = "Не удалось отклонить приглашение";
    }
  }

  async function inviteDelete(id) {
    try {
      const data = await api.request(
        `/notification/invites/delete?invite_id=${id}`,
        {
          method: "DELETE",
        },
      );

      notificationsInvites.value = notificationsInvites.value.filter(
        (i) => i.id !== id,
      );
    } catch (e) {
      serverError.value = "Не удалось удалить приглашение";
    }
  }

  async function allInvitesDelete() {
    try {
      showAllInvitesDeleteModal.value = false;
      const data = await api.request("/notification/invites/delete-all", {
        method: "DELETE",
      });

      notificationsInvites.value = notificationsInvites.value.filter(
        (i) => i.state === "Отправлено",
      );
    } catch (e) {
      serverError.value = "Не удалось удалить приглашения";
    }
  }

  async function openAllMessagesDeleteModal() {
    showAllMessagesDeleteModal.value = true;
  }
  async function closeAllMessagesDeleteModal() {
    showAllMessagesDeleteModal.value = false;
  }

  async function openAllInvitesDeleteModal() {
    showAllInvitesDeleteModal.value = true;
  }
  async function closeAllInvitesDeleteModal() {
    showAllInvitesDeleteModal.value = false;
  }

  const unreadCount = computed(() => {
    const unreadMessages = notificationsMessages.value.filter(
      (m) => !m.is_read,
    ).length;

    const unreadInvites = notificationsInvites.value.filter(
      (n) => n.state === "Отправлено",
    ).length;

    return unreadMessages + unreadInvites;
  });

  const hasUnread = computed(() => unreadCount.value > 0);

  const getAuthToken = () => {
    return localStorage.getItem("token");
  };

  const connectSSE = async () => {
    disconnectSSE();

    const token = getAuthToken();
    if (!token) {
      return false;
    }

    abortController = new AbortController();

    try {
      await fetchEventSource(`${API_URL}/notification/connect`, {
        method: "GET",
        signal: abortController.signal,
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "text/event-stream",
          "Cache-Control": "no-cache",
        },
        onopen(response) {
          console.log("SSE подключено к /notification/connect");
          isConnected.value = true;
        },
        onmessage(event) {
          try {
            const notificationData = JSON.parse(event.data);

            if (notificationData.state === "Отправлено") {
              notificationsInvites.value = [
                notificationData,
                ...notificationsInvites.value,
              ];
            } else if (notificationData.is_read !== undefined) {
              notificationsMessages.value = [
                notificationData,
                ...notificationsMessages.value,
              ];
            }

            console.log("Получено уведомление:", notificationData);
          } catch (error) {
            console.error("Ошибка парсинга уведомления:", error);
          }
        },
        onerror(error) {
          console.error("SSE ошибка:", error);
          isConnected.value = false;
          scheduleReconnect();
        },
        openWhenHidden: true,
      });
    } catch (error) {
      if (error.name !== "AbortError") {
        console.error("Ошибка подключения SSE:", error);
        scheduleReconnect();
      }
    }

    return true;
  };

  const scheduleReconnect = (delay = 3000) => {
    if (reconnectTimeout) clearTimeout(reconnectTimeout);

    reconnectTimeout = setTimeout(() => {
      const token = getAuthToken();
      if (token) {
        console.log("Переподключение к SSE...");
        connectSSE();
      }
    }, delay);
  };

  const disconnectSSE = () => {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout);
      reconnectTimeout = null;
    }

    if (abortController) {
      abortController.abort();
      abortController = null;
    }

    isConnected.value = false;
  };

  const initialize = async () => {
    const token = getAuthToken();
    if (!token) return false;

    try {
      await getNotificationsInvites()
      await getNotificationsMessages()
      return await connectSSE();
    } catch (error) {
      console.error("Initialize error:", error);
      return false;
    }
  };

  const destroy = () => {
    disconnectSSE();
    notificationsInvites.value = [];
    notificationsMessages.value = [];
  };

  return {
    notificationsInvites,
    notificationsMessages,
    unreadCount,
    hasUnread,
    isConnected,
    messagesLoading,
    invitesLoading,
    serverError,
    showAllMessagesDeleteModal,
    showAllInvitesDeleteModal,
    connectSSE,
    disconnectSSE,
    initialize,
    destroy,
    getNotificationsInvites,
    getNotificationsMessages,
    acceptInvite,
    declineInvite,
    messageRead,
    messageDelete,
    allMessagesRead,
    allMessagesDelete,
    inviteDelete,
    allInvitesDelete,
    openAllMessagesDeleteModal,
    closeAllMessagesDeleteModal,
    openAllInvitesDeleteModal,
    closeAllInvitesDeleteModal,
  };
});
