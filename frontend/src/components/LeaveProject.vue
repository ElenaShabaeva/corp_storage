<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Вы точно хотите покинуть проект?</h3>
      <div class="pp__buttons">
        <my-button type="button" @click="closeModal">Отменить</my-button>
        <my-button :filled="true" type="button" @click="handleLeave"
          >Покинуть</my-button
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProjectsStore } from "../store/projects";

const store = useProjectsStore();

async function closeModal() {
  store.closeLeaveModal();
}

async function handleLeave() {
  try {
    await store.leaveProject();
  } catch (e) {}
}
</script>

<style lang="less"></style>
