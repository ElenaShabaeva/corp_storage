<template>
  <PageHeader />
  <main>
      <router-view></router-view>
  </main>
</template>

<script setup>
import PageHeader from './components/PageHeader.vue';
</script>