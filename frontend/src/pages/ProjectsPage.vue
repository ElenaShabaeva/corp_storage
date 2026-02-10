<template>
  <div class="projects">
    <div class="projects__wrapper">
      <my-button :filled="true" type="button" @click="showCreateModal">Создать проект</my-button>
      <ProjectsListing class="projects__listing"/>
    </div>
  </div>
  <CreateProjectsForm v-if="store.showCreateModal"/>
</template>

<script setup>
import CreateProjectsForm from '../components/CreateProjectsForm.vue';
import ProjectsListing from '../components/ProjectsListing.vue';
import { useProjectsStore } from '../store/projects';

const store = useProjectsStore()

async function showCreateModal() {
  store.openCreateModal()
}
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
