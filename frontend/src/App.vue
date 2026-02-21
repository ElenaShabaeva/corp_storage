<template>
  <PageHeader />
  <main>
      <router-view></router-view>
  </main>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import PageHeader from './components/PageHeader.vue';
import { useNotificationsStore } from './store/notifications';

const store = useNotificationsStore()

onMounted(() => store.initialize())
onUnmounted(() => store.disconnectSSE())
</script>