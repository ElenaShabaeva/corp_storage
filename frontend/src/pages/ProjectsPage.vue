<template>
  <div class="projects">
    <div class="projects__wrapper">
      <my-button :filled="true" type="button" @click="showCreateModal">Создать проект</my-button>
      <ProjectsListing class="projects__listing"/>
    </div>
  </div>
  <CreateProjectsForm v-if="store.showCreateModal"/>
  <Loading :title="'Идет создание проекта'" v-if="store.createLoading" />
  <Transition name="modal" appear v-if="store.serverError">
    <div class="modal" :class="{ 'modal--error': store.serverError }">
      {{ store.serverError }}
    </div>
  </Transition>
</template>

<script setup>
import { onMounted } from 'vue';
import CreateProjectsForm from '../components/CreateProjectsForm.vue';
import ProjectsListing from '../components/ProjectsListing.vue';
import { useProjectsStore } from '../store/projects';
import Loading from '../components/Loading.vue';

const store = useProjectsStore()

async function showCreateModal() {
  store.openCreateModal()
}

onMounted(async () => {
  await store.getProjects();
});
</script>

<style lang="less">
.projects {
  &__wrapper {
    display: flex;
    flex-direction: column;
    align-items: end;
    row-gap: 48px;
  }

  &__listing{
    width: 100%;
  }
}
</style>
