<template>
  <div class="projects">
    <div class="projects__wrapper">
      <my-button :filled="true" type="button">Создать проект</my-button>
      <ProjectsListing class="projects__listing"/>
    </div>
  </div>
</template>

<script setup>
import ProjectsListing from '../components/ProjectsListing.vue';

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
