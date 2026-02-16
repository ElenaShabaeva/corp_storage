<template>
  <div class="project">
    <MemberSkeleton v-if="isLoading "/>
    <div class="project__wrapper" v-else>
      <div class="project__top">
        <div class="project__info">
          <h1 class="title">{{ store.projectInfo?.name || 'Название проекта' }}</h1>
          <p>
            {{ store.projectInfo?.description || "У проекта нет описания" }}
          </p>
        </div>
        <nav class="project__nav">
          <router-link :to="`/project/${route.params.id}/members`" class="link">
            Участники
          </router-link>
          <my-text-button v-if="store.projectOwner">Изменить название / описание</my-text-button>
        </nav>
      </div>
      <router-view />
    </div>
  </div>

  <InviteMemberForm v-if="store.showInviteModal"/>

  <Loading :title="'Идет отправка приглашения'" v-if="store.inviteLoading" />

  <Transition name="modal" appear v-if="store.serverError">
    <div class="modal" :class="{ 'modal--error': store.serverError }">
      {{ store.serverError }}
    </div>
  </Transition>
  <Transition name="modal" appear v-if="store.success">
    <div class="modal" :class="{ 'modal--success': store.success }">
      {{ store.success }}
    </div>
  </Transition>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useProjectsStore } from "../../store/projects";
import { computed, onMounted } from "vue";
import MemberSkeleton from "../../components/skeleton/MemberSkeleton.vue";
import InviteMemberForm from "../../components/InviteMemberForm.vue";

const route = useRoute();
const id = route.params.id;

const store = useProjectsStore();

const isLoading = computed(() => 
  store.infoLoading || store.membersLoading
)

onMounted(async () => {
  try {
    await store.getProjectInfo(route.params.id)
  } catch (e) {
    console.error('Ошибка проекта:', e)
  }
  
  try {
    await store.getProjectMembers(route.params.id)
  } catch (e) {
    console.error('Ошибка участников:', e)
  }
})
</script>

<style lang="less">
.project {
  &__wrapper {
    display: flex;
    flex-direction: column;
    row-gap: 48px;
  }

  &__top {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

  &__info {
    display: flex;
    flex-direction: column;

    p {
      margin-top: -16px;
      font-size: 14px;
      line-height: 1.42;
      color: @text-quartenery;
    }
  }

  &__nav {
    display: flex;
    column-gap: 24px;
    padding-left: 4px;
    padding-bottom: 4px;
    border-bottom: 1px solid @border-light;

    button{
      margin-left: auto;
    }
  }
}
</style>
