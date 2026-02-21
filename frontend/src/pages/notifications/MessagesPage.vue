<template>
  <div class="messages">
    <MessagesSkeleton v-if="store.messagesLoading"/>
    <div class="message__wrapper" v-else>
      <p class="messages__none" v-if="store.notificationsMessages.length === 0">
        У вас сейчас нет сообщений
      </p>
      <div class="messages__body" v-else>
        <div class="messages__buttons">
          <my-button
            type="button"
            :filled="true"
            @click="handleReadAll"
            :disabled="!store.hasUnread"
            >Прочитать все</my-button
          >
          <my-button
            type="button"
            @click="handleDeleteAll"
            :disabled="!store.notificationsMessages.some(m => m.is_read)"
            >Удалить все</my-button
          >
        </div>
        <ul class="messages__list">
          <MessagesItem
            v-for="message in store.notificationsMessages"
            :message="message"
            :key="message.id"
          />
        </ul>
      </div>
    </div>
  </div>
  <DeleteAllMesages v-if="store.showAllMessagesDeleteModal"/>
</template>

<script setup>
import { onMounted, watch } from "vue";
import MessagesItem from "../../components/MessagesItem.vue";
import { useNotificationsStore } from "../../store/notifications";
import MessagesSkeleton from "../../components/skeleton/MessagesSkeleton.vue";
import DeleteAllMesages from "../../components/DeleteAllMesages.vue";

const store = useNotificationsStore();

async function handleReadAll() {
  try {
    await store.allMessagesRead();
  } catch (e) {}
}

async function handleDeleteAll() {
  await store.openAllMessagesDeleteModal()
}

watch(
  () => store.notificationsMessages.length,
  (newLength, oldLength) => {
    if (newLength > oldLength) {
      console.log("✅ Новое сообщение через SSE!");
    }
  },
  { immediate: false },
);

onMounted(async () => {
  await store.getNotificationsMessages();
});
</script>

<style lang="less">
.messages {
  &__none {
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    color: @text-tertiary;
  }

  &__body {
    display: flex;
    flex-direction: column;
    row-gap: 48px;
  }

  &__buttons {
    margin-left: auto;
    display: flex;
    column-gap: 24px;
  }

  &__list {
    display: flex;
    flex-direction: column;
    row-gap: 12px;
  }
}
</style>
