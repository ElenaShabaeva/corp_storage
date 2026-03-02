<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Вы точно хотите удалить все приглашения?</h3>
      <div class="pp__buttons">
        <my-button type="button" @click="closeModal">Отменить</my-button>
        <my-button :filled="true" type="button" @click="handleDelete"
          >Удалить</my-button
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { useNotificationsStore } from "../store/notifications";
const store = useNotificationsStore();

async function closeModal() {
    store.closeAllInvitesDeleteModal()
}

async function handleDelete() {
  try {
    await store.allInvitesDelete();
  } catch (e) {}
}
</script>

<style lang="less">

</style>
