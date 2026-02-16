<template>
  <div class="skeleton">
    <div class="skeleton__wrapper">
      <div class="skeleton__top">
        <div class="skeleton__info">
          <div class="skeleton__name"></div>
          <div class="skeleton__description"></div>
        </div>
        <div class="skeleton__nav">
          <div class="skeleton__link"></div>
          <div class="skeleton__link"></div>
        </div>
      </div>
      <div class="skeleton__members">
        <div class="skeleton__members-top">
          <div class="skeleton__line"></div>
          <div class="skeleton__button"></div>
        </div>
        <div class="skeleton__list">
          <div class="skeleton__item">
            <div class="skeleton__line"></div>
            <div class="skeleton__line"></div>
          </div>
          <div class="skeleton__item">
            <div class="skeleton__line"></div>
            <div class="skeleton__line"></div>
          </div>
          <div class="skeleton__item">
            <div class="skeleton__line"></div>
            <div class="skeleton__line"></div>
          </div>
          <div class="skeleton__item">
            <div class="skeleton__line"></div>
            <div class="skeleton__line"></div>
          </div>
          <div class="skeleton__item">
            <div class="skeleton__line"></div>
            <div class="skeleton__line"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="less" scoped>
.skeleton {
  &__wrapper {
    display: flex;
    flex-direction: column;
    row-gap: 48px;
  }

  &__top {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

  &__info {
    width: 100%;
    display: flex;
    flex-direction: column;
    row-gap: 8px;
  }

  &__name,
  &__link {
    height: 32px;
  }

  &__description {
    height: 20px;
  }

  &__nav {
    display: flex;
    column-gap: 24px;
    padding-left: 4px;
    padding-bottom: 4px;
    border-bottom: 1px solid @border-light;
  }

  &__link {
    width: 150px;
  }

  &__members {
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

  &__members-top {
    display: grid;
    grid-template-columns: 1fr 200px;
    align-items: center;
    column-gap: 20px;
  }

  &__button{
    height: 56px;
    width: 200px;
    border-radius: 16px;
  }

  &__line{
    width: 100%;
    height: 24px;
  }

  &__list{
    display: flex;
    flex-direction: column;
    row-gap: 24px;
  }

  &__item{
    display: grid;
    grid-template-columns: 760px 1fr;
    column-gap: 20px;
  }

  &__name,
  &__description,
  &__link,
  &__line,
  &__button {
    background: @skeleton;
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
  }

  &__name,
  &__description,
  &__link,
  &__line {
    border-radius: 8px;
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
