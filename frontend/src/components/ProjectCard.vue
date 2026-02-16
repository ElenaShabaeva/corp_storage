<template>
  <li class="project-card" @click="goToProject">
    <p class="project-card__name">{{ project.name }}</p>
    <div class="project-card__body">
      <div class="project-card__info">
        <span>Создан: {{ project.creator_login }}</span>
        <span>Участников: {{ project.members_count }}</span>
      </div>
      <my-text-button>Покинуть проект</my-text-button>
    </div>
  </li>
</template>

<script setup>
import router from '../router';

const props = defineProps({
  project: {
    type: Object,
  },
});

const goToProject = () => {
  router.push(`/project/${props.project.id}/`)
};
</script>

<style lang="less">
.project-card {
  display: flex;
  flex-direction: column;
  padding: 20px 40px;
  border-radius: 16px;
  background-color: @light-blue;
  cursor: pointer;

  &:hover {
    .project-card__name {
      color: @blue;
    }
  }

  &__name {
    font-size: 18px;
    font-weight: 500;
    line-height: 1.4;
    margin-bottom: 24px;
    transition: all 0.3s;
  }

  &__body {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: end;
    column-gap: 20px;
  }

  &__info {
    display: flex;
    flex-direction: column;
    row-gap: 8px;

    span {
      font-size: 14px;
    }
  }
}
</style>
