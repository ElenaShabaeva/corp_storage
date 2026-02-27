<template>
  <div class="members">
    <div class="members__top">
      <span
        >Участников в проекте:
        {{ store.projectMembers?.length }}</span
      >
      <my-button type="button" :filled="true" v-if="store.projectOwner" @click="showModal"
        >Добавить участника</my-button
      >
    </div>
    <ul class="members__list">
      <MembersItem
        v-for="member in store.projectMembers"
        :member="member"
        :key="member.id"
      />
    </ul>
  </div>
</template>

<script setup>
import MembersItem from "../../components/MembersItem.vue";
import { useProjectsStore } from "../../store/projects";

const store = useProjectsStore();

async function showModal() {
  store.openInviteModal()
}
</script>

<style lang="less">
.members {
  display: flex;
  flex-direction: column;
  row-gap: 24px;

  &__top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    column-gap: 20px;
  }

  &__list {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }
}
</style>
