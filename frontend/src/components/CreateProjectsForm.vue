<template>
  <div class="pp">
    <div class="pp__container">
      <h3 class="title">Создание проекта</h3>
      <form class="form" @submit.prevent="handleCreate">
        <div class="form__fields">
          <my-field
            :label="'Название'"
            :type="'text'"
            :placeholder="'Проект по разработке'"
            :message="nameState"
            v-model="project.name"
            @blur="handleBlurName"
          />
          <my-field-textarea
            :label="'Описание (необязятельно)'"
            :type="'text'"
            :placeholder="'Проект по разработке'"
            v-model="project.description"
          />
        </div>
        <div class="form__buttons pp__buttons">
          <my-button type="button" @click="closeCreateModal"
            >Отменить</my-button
          >
          <my-button type="submit" :filled="true" :disabled="!ifFormValid"
            >Создать</my-button
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useProjectsStore } from "../store/projects";

const store = useProjectsStore();

const project = reactive({
  name: "",
  description: "",
});

async function closeCreateModal() {
  store.closeCreateModal();
}

const isDirtyName = ref(false);

const nameState = computed(() => {
  if (!isDirtyName.value) return "";

  const len = project.name.trim().length;

  if (!len) return "Поле обязятельно";
  if (len > 65) return "Максимум 65 символов";
  return "";
});

const handleBlurName = () => {
  isDirtyName.value = true;
};

const ifFormValid = computed(() => {
  const hasValidData =
    !!project.name.trim() && project.name.trim().length <= 65;

  return hasValidData;
});
</script>

<style lang="less"></style>
