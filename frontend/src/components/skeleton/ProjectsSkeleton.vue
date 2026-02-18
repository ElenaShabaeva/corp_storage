<template>
  <div class="skeleton">
    <h2 class="title">Проекты</h2>
    <div class="skeleton__projects">
      <div class="skeleton__project"></div>
      <div class="skeleton__project"></div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="less" scoped>
.skeleton {
  &__projects {
    display: flex;
    flex-direction: column;
    row-gap: 16px;
  }

  &__project{
    width: 100%;
    height: 130px;
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
