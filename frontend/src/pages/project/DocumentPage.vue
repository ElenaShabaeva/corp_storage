<template>
  <div class="editor">
    <div class="editor__wrapper">
      <h1 class="title">{{ route.params.name }}</h1>
      <div class="editor__body">
        <div class="editor__field">
          <div ref="quillContainer" class="editor__quill"></div>
          <!-- <div class="editor__indicator">
            <span>Сохраненение</span>
            <span>Сохранено</span>
          </div> -->
        </div>

        <div class="editor__block">
          <my-text-button :color="true">Экспорт</my-text-button>
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
import { onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useDocumentStore } from '../../store/documents'

const store = useDocumentStore()
const route = useRoute()

onMounted(async () => {
  await store.connect(route.params.id)
})

onUnmounted(() => {
  store.disconnect()
})
</script>

<style lang="less">
@import "quill/dist/quill.snow.css";

.editor {
  width: 100%;
  width: 1400px;
  margin-left: -220px;
  margin-top: -50px;

  &__body {
    display: flex;
    column-gap: 20px;
  }

  &__indicator {
    position: absolute;
    top: 5px;
    right: 8px;
    padding: 4px 10px;
    border-radius: 6px;
    background-color: @border-extralight;
  }

  &__field {
    position: relative;
    width: 100%;
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
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      transform: scale(1.1);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }

  &__user-initials {
    font-size: 12px;
    font-weight: 600;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  }

  &__others {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: @skeleton;
    font-size: 12px;
    user-select: none;
    cursor: pointer;
  }

  &__others-count {
    font-weight: 700;
    text-shadow: none;
  }

  &__quill {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    height: 490px;
    border: 1px solid @border-light;
  }
}

.ql-toolbar {
  border-top: 1px solid @border-light;
  border-left: 1px solid @border-light;
  border-right: 1px solid @border-light;
  border-radius: 8px 8px 0 0;
}

.ql-container {
  height: calc(400px - 50px);
  border-bottom: 1px solid @border-light;
  border-left: 1px solid @border-light;
  border-right: 1px solid @border-light;
  border-radius: 0 0 8px 8px;
}
</style>
