<template>
  <header class="header">
    <div class="header__container container">
      <div class="header__logo">
        <SvgLogo />
        CorpStorage
      </div>
      <nav class="header__nav" v-if="isAuth">
        <div class="header__nav-block">
          <ul class="header__links">
            <li class="header__link">Проекты</li>
            <li class="header__link">Профиль</li>
          </ul>
        </div>
        <div class="header__nav-block">
          <ul class="header__links">
            <li class="header__link">Уведомления</li>
            <li class="header__link">Выйти</li>
          </ul>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import SvgLogo from "../assets/svg/SvgLogo.vue";
</script>

<style lang="less">
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 88px;

  z-index: 100;

  &::before {
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    @supports (backdrop-filter: blur(20px)) {
      backdrop-filter: blur(10px);
    }
  }

  &__container {
    position: relative;
    display: flex;
    align-items: center;
    column-gap: 60px;
    padding-block: 22px;
    border-bottom: 1px solid @border-light;
    z-index: 1;
  }

  &__logo {
    display: flex;
    align-items: center;
    column-gap: 4px;

    svg {
      flex-shrink: 0;
      color: @dark-blue;
    }
  }

  &__nav {
    display: flex;
    width: 100%;
    justify-content: space-between;
    column-gap: 32px;
  }

  &__links {
    display: flex;
    column-gap: 32px;
  }
}
</style>
