<template>
  <div class="registration">
    <h1 class="title">Регистрация</h1>
    <RegistrationForm />
    <div class="registration__block">
      <span class="registration__text">У вас уже есть аккаунт?</span>
      <router-link class="link" to="/">Войти в аккаунт</router-link>
    </div>
  </div>
  <Loading :title="'Идет регистрация'" v-if="store.loading" />
  <Transition name="modal" appear v-if="!store.loading && store.serverError">
    <div class="modal" :class="{ 'modal--error': store.serverError }">
      {{ store.serverError }}
    </div>
  </Transition>
</template>

<script setup>
import Loading from "../components/Loading.vue";
import RegistrationForm from "../components/RegistrationForm.vue";
import { useAuthStore } from "../store/auth";

const store = useAuthStore();

</script>

<style lang="less">
.registration {
  &__block {
    margin-top: 24px;
    display: flex;
    column-gap: 8px;
  }
}

.modal-appear-from,
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: translateY(-92px);
}

.modal-appear-active,
.modal-enter-active,
.modal-leave-active {
  transition: all 0.4s ease;
}
</style>
