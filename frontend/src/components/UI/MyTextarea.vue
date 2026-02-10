<template>
  <textarea
    name=""
    class="textarea"
    :placeholder="placeholder"
    :value="modelValue"
    @input="updateTextarea"
  ></textarea>
</template>

<script setup>
defineOptions({
  name: "my-textarea",
});

const props = defineProps({
  modelValue: [String, Number],
});

const emit = defineEmits(["update:modelValue", "blur"]);
const updateInput = (event) => {
  emit("update:modelValue", event.target.value);
};
</script>

<style lang="less">
.textarea {
  box-shadow: none;
  outline: none;
  color: @text-primary;
  font-size: 14px;

  padding: 12px 8px 12px 12px;
  border: 1px solid @border-light;
  background-color: @white;
  border-radius: 8px;
  height: 216px;
  resize: none;
  transition: all 0.3s;

  &::placeholder{
    color: @text-tertiary;
  }

  &:not(.input--disabled):focus{
    border-color: @blue;
  }

  &:not(.input--disabled):hover {
    border-color: @blue;
  }

  &--error {
    border-color: @error;
  }

  &--disabled {
    color: @text-tertiary;
    background-color: @disable;
    pointer-events: none;
  }

//   &:hover {
//     border: 1px solid @br-medium;
//   }

//   &--error {
//     border-color: @i-error;
//   }
}
</style>
