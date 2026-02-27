<template>
  <div class="members">
    <MemberSkeleton v-if="store.membersLoading"/>
    <div class="members__wrapper" v-else>
      <div class="members__top">
        <span>Участников в проекте: {{ store.projectMembers?.length }}</span>
        <my-button
          type="button"
          :filled="true"
          v-if="store.projectOwner"
          @click="showModal"
          >Добавить участника</my-button
        >
      </div>
      <ul class="members__list">
        <MembersItem
          v-for="(member, index) in store.projectMembers"
          :member="member"
          :isFirst="index === 0"
          :key="member.id"
        />
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import MembersItem from "../../components/MembersItem.vue";
import MemberSkeleton from "../../components/skeleton/MemberSkeleton.vue";
import { useProjectsStore } from "../../store/projects";
import { onMounted } from "vue";

const store = useProjectsStore();
const route = useRoute();

async function showModal() {
  store.openInviteModal();
}

onMounted(async () => {
  try {
    await store.getProjectMembers(route.params.id);
  } catch (e) {}
});
</script>

<style lang="less">
.members {
  &__wrapper {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

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
