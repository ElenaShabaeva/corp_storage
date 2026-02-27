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
          <router-link :to="`/project/${route.params.id}/documents`" class="link">
            Документы
          </router-link>
        </nav>
      </div>
      <router-view />
    </div>
  </div>

  <InviteMemberForm v-if="store.showInviteModal"/>
  <KickMember v-if="store.showKickModal"/>

  <Loading :title="'Идет отправка приглашения'" v-if="store.inviteLoading" />
  <Loading :title="'Идет исключение из проекта'" v-if="store.kickLoading" />

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
import KickMember from "../../components/KickMember.vue";

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
  }
}

.modal-move,
.modal-enter-active,
.modal-leave-active {
  transition: all 0.4s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: translateY(-92px);
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
