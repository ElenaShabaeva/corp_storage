<template>
  <div class="projects-listing">
    <h1 class="title">Проекты</h1>
    <ul class="projects-listing__list">
      <ProjectCard />
    </ul>
  </div>
</template>

<script setup>
import ProjectCard from "./ProjectCard.vue";
</script>

<style lang="less">
.projects-listing {
  &__body {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  &__list {
    display: flex;
    flex-direction: column;
    row-gap: 16px;
  }
}
</style>
