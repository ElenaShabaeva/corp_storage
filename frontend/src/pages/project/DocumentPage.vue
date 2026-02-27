<template>
  <div class="editor">
    <document-skeleton v-if="store.isLoading"/>
    <div class="editor__wrapper" v-else>
      <h1 class="title">{{ route.params.name }}</h1>
      <div class="editor__body">
        <div class="editor__field">
          <div v-if="!store.isLoading" ref="editorContainer" class="editor__quill" style="height: 490px;"></div>
        </div>

        <div class="editor__block">
          <div class="editor__users">
            <div
              v-for="user in store.visibleUsers"
              :key="user.clientId"
              class="editor__user"
              :style="{ backgroundColor: user.color }"
              :title="user.name || 'Неизвестный пользователь'"
            >
              <span class="editor__user-initials">
                {{ store.getUserInitials(user.name) }}
              </span>
            </div>

            <div
              v-if="store.hiddenUsersCount > 0"
              class="editor__others"
              :title="`+${store.hiddenUsersCount} других пользователей`"
            >
              <span class="editor__others-count">+{{ store.hiddenUsersCount }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, nextTick, watch } from "vue";
import { useRoute } from "vue-router";
import { useDocumentStore } from "../../store/documents";
import Quill from "quill";
import "quill/dist/quill.snow.css";
import DocumentSkeleton from "../../components/skeleton/DocumentSkeleton.vue";

const store = useDocumentStore();
const route = useRoute();
const editorContainer = ref(null);
let quill = null;
let isFromYjs = false;
let isFromQuill = false;

const initQuill = async () => {
  await nextTick();
  await nextTick(); 
  
  if (!editorContainer.value) {
    console.error("Контейнер редактора не найден");
    return;
  }

  if (quill) {
    quill = null;
  }

  editorContainer.value.innerHTML = '';

  try {
    quill = new Quill(editorContainer.value, {
      theme: "snow",
      modules: {
        toolbar: [
          [{ header: [1, 2, 3, 4, 5, 6, false] }],
          ["bold", "italic", "underline", "strike"],
          [{ color: [] }, { background: [] }],
          [],
          ["blockquote"],
          [{ list: "ordered" }, { list: "bullet" }],
          [{ indent: "-1" }, { indent: "+1" }],
          [{ align: [] }],
          ["link"],
          ["clean"]
        ]
      },
    });

    if (store.ytext && store.ytext.length > 0) {
      try {
        const savedDelta = JSON.parse(store.ytext.toString());
        if (savedDelta.ops) {
          quill.setContents(savedDelta);
        } else {
          quill.setText(store.ytext.toString());
        }
      } catch {
        quill.setText(store.ytext.toString());
      }
    }

    const yObserver = () => {
      if (isFromQuill || !quill) return;
      
      isFromYjs = true;
      
      const selection = quill.getSelection();
      const yContent = store.ytext.toString();
      
      try {
        const yDelta = JSON.parse(yContent);
        if (yDelta && yDelta.ops) {
          quill.setContents(yDelta);
        } else {
          quill.setText(yContent);
        }
      } catch {
        quill.setText(yContent);
      }

      nextTick(() => {
        if (selection && quill.hasFocus()) {
          const length = quill.getLength();
          const newPos = Math.min(selection.index, length - 1);
          quill.setSelection(newPos, 0);
        }
      });
      
      isFromYjs = false;
    };
    
    store.ytext.observe(yObserver);

    quill.on('text-change', (delta, oldDelta, source) => {
      if (source === 'user' && !isFromYjs) {
        isFromQuill = true;
        
        const currentDelta = quill.getContents();
        const deltaJson = JSON.stringify(currentDelta);
        
        store.ydoc.transact(() => {
          store.ytext.delete(0, store.ytext.length);
          store.ytext.insert(0, deltaJson);
        }, 'local');
        
        isFromQuill = false;
      }
    });

    quill.on('selection-change', (range) => {
      if (!range && !isFromYjs && !isFromQuill && quill) {
        const currentDelta = quill.getContents();
        const deltaJson = JSON.stringify(currentDelta);
        
        store.ydoc.transact(() => {
          store.ytext.delete(0, store.ytext.length);
          store.ytext.insert(0, deltaJson);
        }, 'local');
      }
    });

  } catch (error) {
    console.error("Ошибка инициализации Quill:", error);
  }
};

watch(() => store.isLoading, (newValue) => {
  if (!newValue) {
    initQuill();
  }
});

onMounted(async () => {
  await store.connect(route.params.id);
});

onUnmounted(() => {
  if (quill) {
    try {
      const currentDelta = quill.getContents();
      const deltaJson = JSON.stringify(currentDelta);
      
      if (store.ydoc) {
        store.ydoc.transact(() => {
          store.ytext.delete(0, store.ytext.length);
          store.ytext.insert(0, deltaJson);
        }, 'local');
      }
    } catch (e) {
      console.error("Ошибка при сохранении:", e);
    }
    
    quill = null;
  }
  
  store.disconnect();
});
</script>

<style lang="less">
@import "quill/dist/quill.snow.css";

.editor {
  width: 100%;
  max-width: 1400px;
  width: 1400px;
  margin-left: -220px;
  margin-top: -50px;

  &__wrapper {
    width: 100%;
  }

  &__body {
    display: flex;
    column-gap: 20px;
  }

  &__field {
    position: relative;
    width: 100%;
    flex: 1;
  }

  &__indicator {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 6px 12px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #e0e0e0;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 6px;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  &__block {
    display: flex;
    flex-direction: column;
    row-gap: 20px;
    align-items: center;
  }

  &__users {
    display: flex;
    flex-direction: column;
    row-gap: 6px;
  }

  &__user {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);

    &:hover {
      transform: scale(1.1);
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
  }

  &__user-initials {
    font-size: 12px;
    font-weight: 600;
    color: white;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }

  &__others {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border: 2px solid white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      transform: scale(1.1);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
  }

  &__quill {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 500px;
    background: white;
    border-radius: 8px;
  }
}

.ql-toolbar {
  border: 1px solid #e0e0e0;
  border-radius: 8px 8px 0 0;
  background: #f8f9fa;
}

.ql-container {
  border: 1px solid #e0e0e0;
  border-top: none;
  border-radius: 0 0 8px 8px;
  min-height: 450px;
  font-size: 14px;
  
  .ql-editor {
    min-height: 450px;
    font-size: 14px;
    line-height: 1.6;
  }
}
</style>