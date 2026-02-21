<template>
  <div class="skeleton">
    <div class="skeleton__buttons">
      <div class="skeleton__button"></div>
      <div class="skeleton__button"></div>
    </div>
    <div class="skeleton__messages">
      <div class="skeleton__message">
        <div class="skeleton__message-info">
          <div class="skeleton__line"></div>
          <div class="skeleton__line"></div>
        </div>
        <div class="skeleton__message-buttons">
          <div class="skeleton__message-button"></div>
          <div class="skeleton__message-button"></div>
        </div>
      </div>
      <div class="skeleton__message">
        <div class="skeleton__message-info">
          <div class="skeleton__line"></div>
          <div class="skeleton__line"></div>
        </div>
        <div class="skeleton__message-buttons">
          <div class="skeleton__message-button"></div>
          <div class="skeleton__message-button"></div>
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
  row-gap: 48px;

  &__buttons {
    margin-left: auto;
    display: flex;
    column-gap: 24px;
  }

  &__button {
    width: 182px;
    height: 56px;
    border-radius: 16px;
  }

  &__messages{
    display: flex;
    flex-direction: column;
    row-gap: 12px;
  }

  &__message {
    display: grid;
    grid-template-columns: 1fr auto;
    column-gap: 20px;

    &:not(:last-child) {
      padding-bottom: 12px;
      border-bottom: 1px solid @border-light;
    }
  }

  &__message-info {
    display: flex;
    flex-direction: column;
    row-gap: 6px;
  }

  &__message-buttons {
    display: flex;
    column-gap: 32px;
  }

  &__message-button {
    width: 76px;
    height: 24px;
  }

  &__line {
    width: 100%;
    height: 24px;

    &:last-child {
      width: calc(100% / 3);
    }
  }

  &__line,
  &__message-button {
    border-radius: 8px;
  }

  &__button,
  &__line,
  &__message-button {
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
