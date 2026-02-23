<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Вы точно хотите удалить документ?</h3>
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
import { useRoute } from 'vue-router';
import { useProjectsStore } from '../store/projects';

const store = useProjectsStore()
const route = useRoute()

async function closeModal() {
    store.closeShowDeleteDocumentModal()
}

async function handleDelete() {
  try {
    await store.deleteDocument(route.params.id)
  } catch (e) {}
}
</script>

<style lang="less"></style>
