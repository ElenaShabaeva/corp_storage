<template>
  <div class="profile">
    <ProfileSkeleton v-if="store.initialLoading" />
    <div class="profile__wrapper" v-else>
      <div class="profile__data">
        <h1 class="title">Профиль</h1>
        <ProfileForm/>
      </div>
    </div>
  </div>
  <Loading :title="'Идет обновление данных'" v-if="store.updateLoading" />
  <Loading :title="'Идет удаление аккаунта'" v-if="store.deleteLoading" />
  <DeleteProfile
    v-if="store.showDeleteModal"
  />
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
import { onMounted } from "vue";
import ProfileForm from "../components/ProfileForm.vue";
import ProfileSkeleton from "../components/skeleton/ProfileSkeleton.vue";
import { useProfileStore } from "../store/profile";
import DeleteProfile from "../components/DeleteProfile.vue";
import Loading from "../components/Loading.vue";

const store = useProfileStore();

onMounted(async () => {
  await store.getProfile();
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
