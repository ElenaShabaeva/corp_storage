<template>
  <div class="documents">
    <DocumentsSkeleton v-if="store.documentsLoading"/>
    <div class="documents__wrapper" v-else>
      <div class="documents__none" v-if="store.projectDocuments?.count === 0">
        <p class="none">В проекте нет документов</p>
        <div class="documents__top-buttons">
          <my-button :filled="true" type="button" @click="handleCreate">Создать</my-button>
        </div>
      </div>
      <div class="documents__body" v-else>
        <div class="documents__top">
          <span>Документов в проекте: {{ store.projectDocuments?.length }}</span>
          <div class="documents__top-buttons">
            <my-button :filled="true" type="button" @click="handleCreate">Создать</my-button>
          </div>
        </div>
        <ul class="documents__list">
          <DocumentsItem v-for="document in store.projectDocuments" :key="document.id" :document="document"/>
        </ul>
      </div>
    </div>
  </div>
  <DeleteDocument v-if="store.showDeleteDocumentModal"/>
  <CreateDocumentForm v-if="store.showCreateDocumentModal"/>

  <Loading :title="'Идет создание документа'" v-if="store.createDocumentLoading" />
</template>

<script setup>
import { onMounted } from "vue";
import DocumentsItem from "../../components/DocumentsItem.vue";
import DocumentsSkeleton from "../../components/skeleton/DocumentsSkeleton.vue";
import { useProjectsStore } from "../../store/projects";
import { useRoute } from "vue-router";
import DeleteDocument from "../../components/DeleteDocument.vue";
import CreateDocumentForm from "../../components/CreateDocumentForm.vue";

const store = useProjectsStore()
const route = useRoute()

function handleCreate() {
  store.openCreateDocumentModal()
}

onMounted(async () => {
  try {
    await store.getDocuments(route.params.id)
  } catch (e) {}
});
</script>

<style lang="less">
.documents {
  &__body {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

  &__none {
    display: flex;
    flex-direction: column;
    align-items: center;
    row-gap: 24px;
  }

  &__top {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    column-gap: 20px;
  }

  &__top-buttons {
    display: flex;
    column-gap: 32px;
  }

  &__list {
    display: flex;
    flex-direction: column;
    row-gap: 12px;
  }
}
</style>
