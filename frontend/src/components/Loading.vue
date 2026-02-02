<template>
  <div class="loading">
    <div class="loading__container">
      <h1 class="title">{{ title }}</h1>
      <div class="loader"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';

defineProps({
  title: {
    type: String,
  },
});

onMounted(() => {
    document.documentElement.style.overflowY = 'hidden';
  document.body.style.overflow = 'hidden';
});
onUnmounted(() => {
  document.body.style.overflow = '';
  document.documentElement.style.overflowY = 'scroll';
});
</script>

<style lang="less">
.loading {
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  z-index: 100;

  &::before {
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: fade(@dark, 50%);

    @supports (backdrop-filter: blur(20px)) {
      background-color: fade(@dark, 50%);
      backdrop-filter: blur(10px);
    }
  }

  &__container {
    position: relative;
    z-index: 1;

    min-width: 500px;
    background-color: @white;
    padding: 30px 60px;
    border-radius: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  html, body{
    overflow: hidden !important;
  }
}
.loader {
  height: 80px;
  aspect-ratio: 1;
  padding: 10px;
  border-radius: 50%;
  box-sizing: border-box;
  position: relative;
  mask:
    conic-gradient(#000 0 0) content-box exclude,
    conic-gradient(#000 0 0);
  filter: blur(12px);
}
.loader:before {
  content: "";
  position: absolute;
  inset: 0;
  background: repeating-conic-gradient(#0000 0 5%, @dark-blue, #0000 20% 50%);
  animation: l2 1.5s linear infinite;
}
@keyframes l2 {
  to {
    rotate: 1turn;
  }
}
</style>
