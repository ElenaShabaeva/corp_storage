<template>
  <div class="field" :class="{ 'field--disabled': disabled }">
    <label :for="label" class="field__label">{{ label }}*</label>
    <my-input
      :class="{
        'input--error': message,
        'input--disabled': disabled,
      }"
      :id="label"
      :placeholder="placeholder"
      :type="type"
      :required="requared"
      v-model="fieldValue"
      v-bind="$attrs"
      :disabled="disabled"
      autocomplete="off"
      @blur="$emit('blur', $event)"
    />
    <span
      v-if="message"
      :class="['field__message', `field__message--error`]"
    >
      {{ message }}
    </span>
  </div>
</template>

<script setup>
import { computed } from "vue";

defineOptions({
  name: "my-field",
  inheritAttrs: false,
});

const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "",
  },
  type: {
    type: String,
    default: "text",
  },
  requared: {
    type: Boolean,
    default: true,
  },
  message: {
    type: String,
    default: "",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  modelValue: [String, Number],
});

const emit = defineEmits(["update:modelValue", "blur"]);

const fieldValue = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});
</script>

<style lang="less">
.field {
  position: relative;
  display: flex;
  flex-direction: column;
  row-gap: 4px;
  width: 100%;

  &--disabled {
    pointer-events: none;
  }

  &__label,
  &__message {
    font-size: 14px;
    line-height: 1.42;
  }

  &__message {
    position: absolute;
    left: 0;
    bottom: -16px;
    font-size: 12px;

    &--error{
      color: @error;
    }
  }
}
</style>
