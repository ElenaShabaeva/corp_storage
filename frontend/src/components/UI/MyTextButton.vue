<template>
  <button class="text-button" :class="{ 'text-button--color': color }">
    <slot></slot>
  </button>
</template>

<script setup>
defineOptions({
  name: "my-text-button",
});

const props = defineProps({
  color: {
    type: Boolean,
    default: false,
  },
});
</script>

<style lang="less">
.text-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  outline: none;
  background-color: transparent;
  border: none;
  text-decoration: underline;
  text-align: center;
  transition: all 0.3s;
  overflow: hidden;
  cursor: pointer;
  color: @text-tertiary;

  &:hover {
    color: @text-primary;
  }

  &--color {
    color: @blue;

    &:hover {
      color: @dark-blue;
    }
  }

  &:disabled{
    cursor: default;
    text-decoration: none;
    color: @text-quartenery;
  }
}
</style>
