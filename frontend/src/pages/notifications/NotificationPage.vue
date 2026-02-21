<template>
  <div class="notification">
    <MemberSkeleton v-if="isLoading" />
    <div class="notification__wrapper" v-else>
      <div class="notification__top">
        <h1 class="title">Уведомления</h1>
        <nav class="notification__nav">
          <router-link :to="`/notification/messages`" class="link"
            >Сообщения</router-link
          >
          <router-link :to="`/notification/invites`" class="link"
            >Приглашения</router-link
          >
        </nav>
      </div>
      <router-view />
    </div>
  </div>

  <Transition name="modal" appear v-if="store.serverError">
    <div class="modal" :class="{ 'modal--error': store.serverError }">
      {{ store.serverError }}
    </div>
  </Transition>
</template>

<script setup>
import { useNotificationsStore } from '../../store/notifications';

const store = useNotificationsStore()
</script>

<style lang="less">
.notification {
  &__wrapper {
    display: flex;
    flex-direction: column;
    row-gap: 48px;
  }

  &__top {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

  &__nav {
    display: flex;
    column-gap: 24px;
    padding-left: 4px;
    padding-bottom: 4px;
    border-bottom: 1px solid @border-light;
  }
}
</style>
