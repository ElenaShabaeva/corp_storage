<template>
  <div class="skeleton">
    <div class="skeleton__line"></div>
    <div class="skeleton__body">
      <div class="skeleton__editor"></div>
      <div class="skeleton__block">
        <div class="skeleton__button"></div>
        <div class="skeleton__users">
          <div class="skeleton__user"></div>
          <div class="skeleton__user"></div>
          <div class="skeleton__user"></div>
          <div class="skeleton__user"></div>
          <div class="skeleton__user"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="less" scoped>
.skeleton {
  &__line {
    height: 32px;
    margin-bottom: 24px;
  }

  &__body {
    display: flex;
    column-gap: 20px;
  }

  &__editor {
    height: 490px;
    width: 100%;
  }

  &__block{
    display: flex;
    flex-direction: column;
    row-gap: 20px;
    align-items: center;
  }

  &__button{
    width: 76px;
    height: 24px;
  }

  &__users {
    display: flex;
    flex-direction: column;
    row-gap: 6px;
  }

  &__user {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }


  &__line,
  &__editor,
  &__button {
    border-radius: 8px;
  }

  &__line,
  &__editor,
  &__button,
  &__user {
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
