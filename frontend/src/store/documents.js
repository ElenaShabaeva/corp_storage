import { defineStore } from "pinia";
import { computed, nextTick, ref } from "vue";
import * as Y from "yjs";
import { HocuspocusProvider } from "@hocuspocus/provider";

export const useDocumentStore = defineStore("document", () => {
  const ydoc = ref(null);
  const ytext = ref(null);
  const provider = ref(null);
  const url = "ws://26.122.80.20:1234";
  const token = localStorage.getItem("token");

  const currentDocId = ref("");
  const isConnected = ref(false);
  const awarenessStates = ref([]);

  const generateUserColor = (name) => {
    const seed = name || "user";
    let hash = 0;
    for (let i = 0; i < seed.length; i++) {
      hash = seed.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash) % 360;
    return `hsl(${hue}, 70%, 55%)`;
  };

  const connect = async (docId) => {
    if (!docId) {
      console.log("Не передан docId");
      return;
    }

    currentDocId.value = docId;

    ydoc.value = new Y.Doc();
    ytext.value = ydoc.value.getText("quill");

    const username = localStorage.getItem("username") || "Неизвестный пользователь";

    provider.value = new HocuspocusProvider({
      url: url,
      name: docId,
      document: ydoc.value,
      token: token,
      
      onConnect: () => {
        isConnected.value = true;
        console.log("Подключено к документу:", docId);
        
        provider.value.awareness.setLocalState({
          name: username,
          color: generateUserColor(username),
        });
      },
      
      onDisconnect: () => {
        isConnected.value = false;
        console.log("Отключено от документа");
      },
      
      onAwarenessUpdate: () => {
        updateAwarenessStates();
      }
    });

    const updateAwarenessStates = () => {
      try {
        const states = provider.value.awareness.getStates();
        awarenessStates.value = Array.from(states.values()).map((state) => ({
          clientId: state.clientId || Math.random(),
          name: state.name || "Неизвестный",
          color: state.color || generateUserColor(state.name || "user"),
        }));
      } catch (e) {
        console.log("Ошибка обновления:", e);
      }
    };

    provider.value.awareness.on("change", updateAwarenessStates);
    nextTick(() => updateAwarenessStates());
  };

  const disconnect = () => {
    if (provider.value) {
      provider.value.destroy();
      provider.value = null;
    }
    ydoc.value = null;
    ytext.value = null;
    isConnected.value = false;
    awarenessStates.value = [];
  };

  const visibleUsers = computed(() => {
    return awarenessStates.value.slice(0, 5);
  });

  const hiddenUsersCount = computed(() => {
    return Math.max(0, awarenessStates.value.length - 5);
  });

  const getUserInitials = (name) => {
    if (!name) return "?";
    return name
      .split(" ")
      .slice(0, 2)
      .map((word) => word[0])
      .join("")
      .toUpperCase();
  };

  return {
    ydoc,
    ytext,
    provider,
    currentDocId,
    isConnected,
    visibleUsers,
    awarenessStates,
    hiddenUsersCount,
    getUserInitials,
    connect,
    disconnect,
  };
});
