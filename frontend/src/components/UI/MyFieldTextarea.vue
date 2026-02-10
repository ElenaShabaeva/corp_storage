<template>
  <div class="field">
    <label :for="label" class="field__label">{{ label }}*</label>
    <my-textarea
      :class="{ 'textarea--error': errorMessage }"
      :id="label"
      :placeholder="placeholder"
      :type="type"
      :required="requared"
      v-model="fieldValue"
      v-bind="$attrs"
      autocomplete="off"
      @blur="$emit('blur', $event)"
    />
    <span class="field__error" v-if="errorMessage">{{ errorMessage }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

defineOptions({
  name: "my-field-textarea",
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