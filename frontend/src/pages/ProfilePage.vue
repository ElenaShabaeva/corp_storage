<template>
  <div class="profile">
    <ProfileSkeleton v-if="store.initialLoading" />
    <div class="profile__wrapper" v-else>
      <div class="profile__data">
        <h1 class="title">Профиль</h1>
        <ProfileForm/>
      </div>
      <ProjectsListing />
    </div>
  </div>
  <Loading :title="'Идет обновление данных'" v-if="store.updateLoading" />
  <Loading :title="'Идет удаление аккаунта'" v-if="store.deleteLoading" />
  <Loading :title="'Идет выход из проекта'" v-if="store.leaveLoading" />
  <DeleteProfile
    v-if="store.showDeleteModal"
  />
  <LeaveProject v-if="projectsStore.showLeaveModal"/>
  <Transition name="modal" appear v-if="store.serverError || projectsStore.serverError">
    <div class="modal" :class="{ 'modal--error': store.serverError || projectsStore.serverError }">
      {{ store.serverError || projectsStore.serverError }}
    </div>
  </Transition>
  <Transition name="modal" appear v-if="store.success || projectsStore.success">
    <div class="modal" :class="{ 'modal--success': store.success || projectsStore.success }">
      {{ store.success || projectsStore.success }}
    </div>
  </Transition>
</template>

<script setup>
import { onMounted } from "vue";
import ProfileForm from "../components/ProfileForm.vue";
import ProfileSkeleton from "../components/skeleton/ProfileSkeleton.vue";
import { useProfileStore } from "../store/profile";
import DeleteProfile from "../components/DeleteProfile.vue";
import Loading from "../components/Loading.vue";
import ProjectsListing from "../components/ProjectsListing.vue";
import { useProjectsStore } from "../store/projects";
import LeaveProject from "../components/LeaveProject.vue";

const store = useProfileStore();
const projectsStore = useProjectsStore()

onMounted(async () => {
  await store.getProfile();
  await projectsStore.getProjects()
});
</script>

<style lang="less">
.profile {
  &__wrapper {
    display: flex;
    flex-direction: column;
    row-gap: 100px;
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
