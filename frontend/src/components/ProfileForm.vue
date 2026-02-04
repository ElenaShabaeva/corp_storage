<template>
  <form class="form form--row">
    <div class="form__fields">
      <my-field
        :label="'Имя'"
        :type="'text'"
        :placeholder="'Иван'"
        v-model="user.name"
        :message="nameState"
        @blur="handleBlurName"
      />
      <my-field
        :label="'Фамилия'"
        :type="'text'"
        :placeholder="'Иванов'"
        v-model="user.surname"
        :message="surnameState"
        @blur="handleBlurSurname"
      />
      <my-field
        :label="'Логин'"
        :type="'text'"
        :placeholder="'Иван'"
        :disabled="true"
        v-model="user.login"
      />
    </div>
    <div class="form__buttons">
      <my-button :filled="true" type="submit">Обновить данные</my-button>
      <my-button type="button">Удалить аккаунт</my-button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, watch } from "vue";
import { useProfileStore } from "../store/profile";

const store = useProfileStore();

const user = reactive({
  name: "",
  surname: "",
  login: "",
});

const userData = computed(() => ({
  name: store.user?.name || '',
  surname: store.user?.surname || '',
  login: store.user?.login || ''
}))

watch(() => store.user, (newUser) => {
  if (newUser) Object.assign(user, userData.value);
}, { immediate: true });
</script>

<style lang="less"></style>
