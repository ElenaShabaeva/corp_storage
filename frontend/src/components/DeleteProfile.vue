<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Вы точно хотите удалить аккаунт?</h3>
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
import { useProfileStore } from "../store/profile";

const store = useProfileStore();

async function closeModal() {
    store.closeModal()
}

async function handleDelete() {
  try {
    await store.deleteProfile();
  } catch (e) {}
}
</script>

<style lang="less"></style>
