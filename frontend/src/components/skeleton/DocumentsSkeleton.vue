<template>
  <div class="skeleton">
    <div class="skeleton__top">
      <div class="skeleton__line"></div>
      <div class="skeleton__top-buttons">
        <div class="skeleton__button"></div>
      </div>
    </div>
    <div class="skeleton__list">
      <div class="skeleton__item">
        <div class="skeleton__item-info">
          <div class="skeleton__line"></div>
          <div class="skeleton__line"></div>
        </div>
        <div class="skeleton__item-buttons">
          <div class="skeleton__item-button"></div>
          <div class="skeleton__item-button"></div>
        </div>
      </div>
      <div class="skeleton__item">
        <div class="skeleton__item-info">
          <div class="skeleton__line"></div>
          <div class="skeleton__line"></div>
        </div>
        <div class="skeleton__item-buttons">
          <div class="skeleton__item-button"></div>
          <div class="skeleton__item-button"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="less" scoped>
.skeleton {
  display: flex;
  flex-direction: column;
  row-gap: 24px;

  &__top {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    column-gap: 20px;
  }

  &__top-buttons {
    display: flex;
    column-gap: 32px;
  }

  &__button {
    height: 56px;
    width: 200px;
    border-radius: 16px;
  }

  &__list {
    display: flex;
    flex-direction: column;
    row-gap: 12px;
  }

  &__item {
    display: grid;
    grid-template-columns: 1fr auto;
    column-gap: 20px;

    &:not(:last-child) {
      padding-bottom: 12px;
      border-bottom: 1px solid @border-light;
    }
  }

  &__item-info{
    display: flex;
    flex-direction: column;
    row-gap: 8px;
  }

  &__line {
    width: 100%;
    height: 24px;

    &:last-child {
      width: calc(100% / 3);
    }
  }

  &__item-buttons {
    display: flex;
    column-gap: 32px;
  }

  &__item-button{
    width: 76px;
    height: 24px;
  }

  &__line,
  &__item-button {
    border-radius: 8px;
  }

  &__line,
  &__button,
  &__item-button {
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
