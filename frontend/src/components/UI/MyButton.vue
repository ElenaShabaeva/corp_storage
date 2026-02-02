<template>
  <button class="button" :class="{ 'button--filled': filled }">
    <slot></slot>
  </button>
</template>

<script setup>
defineOptions({
  name: "my-button",
});

const props = defineProps({
  filled: {
    type: Boolean,
    default: false,
  },
});
</script>

<style lang="less">
.button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  outline: none;
  background-color: transparent;
  border: none;
  text-decoration: none;
  text-align: center;
  transition: all 0.3s;
  overflow: hidden;
  cursor: pointer;

  padding: 16px 32px;
  border-radius: 16px;
  border: 1px solid @border-light;
  background-color: @bg-secondary;

  &:hover {
    background-color: @white;
    border-color: @border-medium;
  }

  &--filled {
    border: 1px solid @blue;
    background-color: @blue;
    color: @text-invert;

    &:hover {
      background-color: @dark-blue;
    }
  }

  &:disabled{
    cursor: default;
    border-color: @border-extralight;
    background-color: @white;
    color: @text-tertiary;
  }
}
</style>
