<template>
  <form class="form form--row" @submit.prevent="handleUpdate">
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
      <my-button :filled="true" type="submit" v-if="isFormValid">Обновить данные</my-button>
      <my-button type="button" @click="showModal">Удалить аккаунт</my-button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, watch, ref } from "vue";
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

async function handleUpdate() {
  try {
    await store.updateProfile({
      name: user.name,
      surname: user.surname
    })
  } catch (e) {}
}

async function showModal() {
  store.openModal()
}

const hasChanges = computed(() => {
  return (
    user.name.trim() !== (store.user?.name || '').trim() ||
    user.surname.trim() !== (store.user?.surname || '').trim()
  )
})

const isFormValid = computed(() => {
  const hasValidData = (
    !!user.name.trim() &&
    user.name.trim().length >= 1 &&
    user.name.trim().length <= 150 &&
    !!user.surname.trim() &&
    user.surname.trim().length >= 1 &&
    user.surname.trim().length <= 150
  )
  
  return hasValidData && hasChanges.value
})

const isDirtyName = ref(false);
const isDirtySurname = ref(false);

const nameState = computed(() => {
  if (!isDirtyName.value) return "";

  const len = user.name.trim().length;

  if (!len) return "Поле обязательно";
  if (len > 150) return "Максимум 150 символов";
  return "";
});

const surnameState = computed(() => {
  if (!isDirtySurname.value) return "";

  const len = user.surname.trim().length;

  if (!len) return "Поле обязательно";
  if (len > 150) return "Максимум 150 символов";
  return "";
});

const handleBlurName = () => {
  isDirtyName.value = true;
};
const handleBlurSurname = () => {
  isDirtySurname.value = true;
};
</script>

<style lang="less"></style>
