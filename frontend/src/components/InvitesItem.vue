<template>
  <li class="invite">
    <div class="invite__wrapper">
      <p>Приглашение</p>
      <div class="invite__info">
        <span>Проект - {{ invite.project_name }}</span>
        <span>Создатель - {{ invite.project_creator }}</span>
      </div>
      <span class="invite__status" :class="{'invite__status--accept': invite.state === 'Принято', 'invite__status--decline': invite.state === 'Отклонено'}" v-if="invite.state !== 'Отправлено'">{{ invite.state }}</span>
      <span class="invite__datetime">Отправлено - {{ invite.date_time }}</span>
    </div>
    <div class="invite__buttons" v-if="invite.state === 'Отправлено'">
      <my-text-button :color="true" type="button" @click="handleAccept">Принять</my-text-button>
      <my-text-button type="button" @click="handleDecline">Отклонить</my-text-button>
    </div>
    <my-text-button type="button" v-else @click="handleDelete">Удалить</my-text-button>
  </li>
</template>

<script setup>
import { useNotificationsStore } from '../store/notifications';

const props = defineProps({
  invite: {
    type: Object
  }
});

const store = useNotificationsStore()

async function handleAccept() {
  try{
    await store.acceptInvite(props.invite.id)
  } catch(e){}
}

async function handleDecline() {
  try{
    await store.declineInvite(props.invite.id)
  } catch(e){}
}

async function handleDelete() {
  try{
    await store.inviteDelete(props.invite.id)
  } catch(e) {}
}
</script>

<style lang="less">
.invite {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: start;
  column-gap: 20px;

  &:not(:last-child) {
    padding-bottom: 12px;
    border-bottom: 1px solid @border-light;
  }

  &__wrapper {
    display: flex;
    flex-direction: column;
    row-gap: 10px;

    p {
      margin: 0;
      font-size: 18px;
      font-weight: 500;
    }
  }

  &__info{
    display: flex;
    flex-direction: column;
    row-gap: 8px;
    color: @text-secondary;
  }

  &__status{
    &--accept{
        color: @success;
    }

    &--decline{
        color: @error;
    }
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
