<template>
  <form class="form" @submit.prevent="handleAuthorization">
    <my-field
      :label="'Логин'"
      :type="'text'"
      :placeholder="'Иван'"
      v-model="user.login"
      :message="loginState"
      @blur="handleBlurLogin"
    />
    <my-field
      :label="'Пароль'"
      :type="'password'"
      :placeholder="'********'"
      v-model="user.password"
      :message="passwordState || store.fieldError"
      @blur="handleBlurPassword"
    />
    <my-button :filled="true" type="submit" :disabled="!isFormValid"
      >Войти в аккаунт</my-button
    >
  </form>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import { useAuthStore } from "../store/auth";

const store = useAuthStore();

const user = reactive({
  login: "",
  password: "",
});

const handleAuthorization = async () => {
  isDirtyLogin.value = true;
  isDirtyPassword.value = true;

  if (!isFormValid.value) return;

  try {
    await store.authorization(user);

    user.login = "";
    user.password = "";
    isDirtyLogin.value = false;
    isDirtyPassword.value = false;

  } catch (e) {
  }
};

const isFormValid = computed(() => {
  return (
    !!user.login &&
    user.login.length >= 4 &&
    user.login.length <= 16 &&
    !!user.password &&
    user.password.length >= 8 &&
    user.password.length <= 16 &&
    /[a-z]/.test(user.password) &&
    /[A-Z]/.test(user.password) &&
    /[0-9]/.test(user.password)
  );
});

const isDirtyLogin = ref(false);
const isDirtyPassword = ref(false);

const loginState = computed(() => {
  if (!isDirtyLogin.value) return "";

  const len = user.login.length;

  if (!len) return "Поле обязательно";
  if (len < 4) return "Минимум 4 символа";
  if (len > 16) return "Максимум 16 символов";
  return "";
});

const passwordState = computed(() => {
  if (!isDirtyPassword.value) return "";

  const len = user.password.length;
  if (!len) return "Поле обязательно";
  if (len < 8) return "Минимум 8 символов";
  if (len > 16) return "Максимум 16 символов";

  if (!/[a-z]/.test(user.password))
    return "Должна быть хотя бы одна маленькая английская буква";
  if (!/[A-Z]/.test(user.password))
    return "Должна быть хотя бы одна большая английская буква";
  if (!/[0-9]/.test(user.password)) return "Должна быть хотя бы одна цифра";

  return "";
});

const handleBlurLogin = () => {
  isDirtyLogin.value = true;
};
const handleBlurPassword = () => {
  isDirtyPassword.value = true;
};
</script>
