<template>
  <div class="profile">
    <ProfileSkeleton v-if="store.initialLoading" />
    <div
      class="profile__wrapper"
      v-else
    >
      <div class="profile__data">
        <h1 class="title">Профиль</h1>
        <ProfileForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import ProfileForm from "../components/ProfileForm.vue";
import ProfileSkeleton from "../components/skeleton/ProfileSkeleton.vue";
import { useProfileStore } from "../store/profile";

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

</style>
