<template>
  <div class="profile">
    <h1 class="title">Профиль</h1>
    <div class="profile__block">
      <ProfileForm />
    </div>
  </div>
</template>

<script setup>
import ProfileForm from '../components/ProfileForm.vue';

</script>

<style lang="less">
.profile{
  &__block{
    display: flex;
    flex-direction: column;
    row-gap: 100px;
  }
}
</style>
