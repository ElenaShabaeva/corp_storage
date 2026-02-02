<template>
  <input class="input" :value="modelValue" @input="updateInput" @blur="$emit('blur', $event)"/>
</template>

<script setup>
defineOptions({
  name: 'my-input'
})

const props = defineProps({
  modelValue: [String, Number]
})

const emit = defineEmits(["update:modelValue", "blur"])
const updateInput = (event) => {
  emit("update:modelValue", event.target.value);
};
</script>

<style lang="less">
.input {
  box-shadow: none;
  outline: none;
  color: @text-primary;
  font-size: 14px;

  padding: 12px 8px 12px 12px;
  border: 1px solid @border-light;
  background-color: @white;
  border-radius: 8px;
  height: 44px;
  transition: all 0.3s;

  &::placeholder{
    color: @text-tertiary;
  }

  &:focus{
    border-color: @blue;
  }

  &:not(:disabled):hover {
    border-color: @blue;
  }

  &--error {
    border-color: @error;
  }

  &--disabled {
    color: @text-tertiary;
    background-color: @disable;
  }
}
</style>
