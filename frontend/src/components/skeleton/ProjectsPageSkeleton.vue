<template>
  <div class="skeleton">
    <div class="skeleton__button"></div>
    <ProjectsSkeleton />
  </div>
</template>

<script setup>
import ProjectsSkeleton from "./ProjectsSkeleton.vue";
</script>

<style lang="less" scoped>
.skeleton {
  display: flex;
  flex-direction: column;
  row-gap: 48px;

  &__button {
    margin-left: auto;
    width: 182px;
    height: 56px;
    border-radius: 16px;
    background: @skeleton;
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
  }
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
