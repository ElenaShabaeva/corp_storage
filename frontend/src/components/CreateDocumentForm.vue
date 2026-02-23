<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Создание документа</h3>
      <form class="form" @submit.prevent="handleCreate">
        <div class="form__fields">
          <my-field
            :label="'Название документа'"
            :type="'text'"
            :placeholder="'Документация'"
            :message="nameState"
            v-model="name"
            @blur="handleBlurName"
          />
        </div>
        <div class="form__buttons pp__buttons">
          <my-button type="button" @click="closeModal">Отменить</my-button>
          <my-button
            type="submit"
            :filled="true"
            :disabled="!ifFormValid"
            >Создать</my-button
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

const name = ref("");
const isDirtyName = ref(false);

const nameState = computed(() => {
  if (!isDirtyName.value) return "";

  const len = name.value.trim().length;

  if (!len) return "Поле обязятельно";
  if (len > 65) return "Максимум 65 символов";
  return "";
});

async function handleCreate() {
  try {
    const id = route.params.id
    await store.createDocument(id, name.value)
  } catch (e) {}
}

async function closeModal() {
  store.closeCreateDocumentModal()
}

const handleBlurName = () => {
  isDirtyName.value = true;
};

const ifFormValid = computed(() => {
  const hasValidData =
    !!name.value.trim() && name.value.trim().length <= 65;

  return hasValidData;
});
</script>

<style lang="less"></style>
