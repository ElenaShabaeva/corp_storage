<template>
  <div class="skeleton">
    <div class="skeleton__wrapper">
      <div>
        <h1 class="title">Профиль</h1>
        <div class="skeleton__form form form--row">
          <div class="skeleton__fields form__fields">
            <div class="skeleton__field">
              <div class="skeleton__field-label"></div>
              <div class="skeleton__field-input"></div>
            </div>
            <div class="skeleton__field">
              <div class="skeleton__field-label"></div>
              <div class="skeleton__field-input"></div>
            </div>
            <div class="skeleton__field">
              <div class="skeleton__field-label"></div>
              <div class="skeleton__field-input"></div>
            </div>
          </div>
          <div class="skeleton__buttons form__buttons">
            <div class="skeleton__button"></div>
            <div class="skeleton__button"></div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="title">Проекты</h2>
        <div class="skeleton__projects">
          <div class="skeleton__project"></div>
          <div class="skeleton__project"></div>
          <div class="skeleton__project"></div>
          <div class="skeleton__project"></div>
          <div class="skeleton__project"></div>
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
    row-gap: 100px;
  }

  &__field {
    display: flex;
    flex-direction: column;
    row-gap: 4px;
  }

  &__field-label,
  &__field-input,
  &__button,
  &__project {    
    background: @skeleton;
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
  }

  &__field-label,
  &__field-input {
    border-radius: 8px;
  }

  &__button,
  &__project {
    border-radius: 16px;
  }

  &__field-label {
    width: 100px;
    height: 24px;
  }

  &__field-input {
    width: 100%;
    height: 48px;
  }

  &__button {
    width: 250px;
    height: 56px;
  }

  &__projects {
    display: flex;
    column-gap: 60px;
    row-gap: 40px;
    flex-wrap: wrap;
  }

  &__project {
    width: calc(25% - 45px);
    height: 124px;
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
