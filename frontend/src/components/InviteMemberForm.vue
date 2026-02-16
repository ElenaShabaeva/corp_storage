<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Добавление участника</h3>
      <form class="form" @submit.prevent="handleInvite">
        <div class="form__fields">
          <my-field
            :label="'Имя * (укажите nickname пользователя)'"
            :type="'text'"
            :placeholder="'nickname'"
            :message="nicknameState"
            v-model="nickname"
            @blur="handleBlurNickname"
          />
        </div>
        <div class="form__buttons pp__buttons">
          <my-button type="button" @click="closeModal">Отменить</my-button>
          <my-button
            type="submit"
            :filled="true"
            :disabled="!ifFormValid"
            >Добавить</my-button
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useProjectsStore } from "../store/projects";
import { useRoute } from "vue-router";

const route = useRoute()
const store = useProjectsStore();

const nickname = ref("");
const isDirtyNickname = ref(false);

const nicknameState = computed(() => {
  if (!isDirtyNickname.value) return "";

  const len = nickname.value.trim().length;

  if (!len) return "Поле обязятельно";
  if (len > 65) return "Максимум 65 символов";
  return "";
});

async function handleInvite() {
  try {
    const id = route.params.id
    await store.inviteMember(id, nickname.value)
  } catch (e) {}
}

async function closeModal() {
  store.closeInviteModal();
}

const handleBlurNickname = () => {
  isDirtyNickname.value = true;
};

const ifFormValid = computed(() => {
  const hasValidData =
    !!nickname.value.trim() && nickname.value.trim().length <= 65;

  return hasValidData;
});
</script>

<style lang="less"></style>
