<template>
  <li class="document">
    <div class="document__info">
      <p>{{ document?.name }}</p>
      <span>Создал - {{ document?.creator }}</span>
    </div>
    <div class="document__buttons">
      <my-text-button type="button" v-if="document?.can_delete" @click="handleDelete">Удалить</my-text-button>
    </div>
  </li>
</template>

<script setup>
import { useProjectsStore } from '../store/projects';

const props = defineProps({
  document: {
    type: Object
  }
})

const store = useProjectsStore()

function handleDelete() {
  store.openShowDeleteDocumentModal(props.document.id)
}
</script>

<style lang="less">
.document {
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
    row-gap: 8px;

    p {
      margin: 0;
      font-size: 18px;
      font-weight: 500;
    }

    span {
      font-size: 14px;
      color: @text-quartenery;
    }
  }

  &__buttons{
    display: flex;
    column-gap: 32px;
  }
}
</style>
