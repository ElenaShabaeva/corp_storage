<template>
  <form class="form" @submit.prevent="handleRegistration">
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
      v-model="user.login"
      :message="loginState || store.fieldError"
      @blur="handleBlurLogin"
    />
    <my-field
      :label="'Пароль'"
      :type="'password'"
      :placeholder="'********'"
      v-model="user.password"
      :message="passwordState"
      @blur="handleBlurPassword"
    />
    <my-button :filled="true" type="submit" :disabled="!isFormValid"
      >Зарегистрироваться</my-button
    >
  </form>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import { useAuthStore } from "../store/auth";

const store = useAuthStore();

const user = reactive({
  name: "",
  surname: "",
  login: "",
  password: "",
});

const handleRegistration = async () => {
  isDirtyName.value = true;
  isDirtySurname.value = true;
  isDirtyLogin.value = true;
  isDirtyPassword.value = true;

  if (!isFormValid.value) return;

  try {
    await store.registration(user);

    user.name = "";
    user.surname = "";
    user.login = "";
    user.password = "";
    isDirtyName.value = false;
    isDirtySurname.value = false;
    isDirtyLogin.value = false;
    isDirtyPassword.value = false;

  } catch (e) {
  }
};

const isFormValid = computed(() => {
  return (
    !!user.name &&
    user.name.length >= 1 &&
    user.name.length <= 150 &&
    !!user.surname &&
    user.surname.length >= 1 &&
    user.surname.length <= 150 &&
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

const isDirtyName = ref(false);
const isDirtySurname = ref(false);
const isDirtyLogin = ref(false);
const isDirtyPassword = ref(false);

const nameState = computed(() => {
  if (!isDirtyName.value) return "";

  const len = user.name.length;

  if (!len) return "Поле обязательно";
  if (len > 150) return "Максимум 150 символов";
  return "";
});

const surnameState = computed(() => {
  if (!isDirtySurname.value) return "";

  const len = user.surname.length;

  if (!len) return "Поле обязательно";
  if (len > 150) return "Максимум 150 символов";
  return "";
});

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

const handleBlurName = () => {
  isDirtyName.value = true;
};
const handleBlurSurname = () => {
  isDirtySurname.value = true;
};
const handleBlurLogin = () => {
  isDirtyLogin.value = true;
};
const handleBlurPassword = () => {
  isDirtyPassword.value = true;
};
</script>
