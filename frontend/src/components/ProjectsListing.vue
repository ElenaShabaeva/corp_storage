<template>
  <div class="projects-listing">
    <h1 class="title">Проекты</h1>
    <p class="projects-listing__none" v-if="!store.projects || store.projects.length === 0">У вас сейчас нет проектов</p>
    <ul class="projects-listing__list" v-else>
      <ProjectCard v-for="project in store.projects" :key="project.id" :project="project"/>
    </ul>
  </div>
</template>

<script setup>
import { useProjectsStore } from "../store/projects";
import ProjectCard from "./ProjectCard.vue";

const store = useProjectsStore()
</script>

<style lang="less">
.projects-listing {
  &__none{
    font-size: 18px;
    font-weight: 700;
    color: @text-tertiary;
  }

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
