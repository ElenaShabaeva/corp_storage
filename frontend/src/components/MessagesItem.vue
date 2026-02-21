<template>
  <li class="message">
    <div class="message__info">
      <p class="message__text">{{ message.message }}</p>
      <span class="message__datetime">Отправлено - {{ message.date_time }}</span>
    </div>
    <div class="message__buttons">
      <my-text-button :color="true" type="button" v-if="!message.is_read" @click="handleRead">Прочитать</my-text-button>
      <my-text-button type="button" @click="handleDelete" v-if="message.is_read">Удалить</my-text-button>
    </div>
  </li>
</template>

<script setup>
import { useNotificationsStore } from '../store/notifications';

const props = defineProps({
  message: {
    type: Object
  }
})

const store = useNotificationsStore()

async function handleRead() {
  try{
    await store.messageRead(props.message.id)
  } catch(e) {}
}

async function handleDelete() {
  try{
    await store.messageDelete(props.message.id)
  } catch(e) {}
}
</script>

<style lang="less">
.message {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: start;
  column-gap: 20px;

  &:not(:last-child) {
    padding-bottom: 12px;
    border-bottom: 1px solid @border-light;
  }

  &__info {
    display: flex;
    flex-direction: column;
    row-gap: 6px;
  }

  &__text {
    font-size: 18px;
    font-weight: 500;
  }

  &__datetime {
    font-size: 14px;
    color: @text-quartenery;
  }

  &__buttons {
    display: flex;
    column-gap: 32px;
  }
}
</style>
