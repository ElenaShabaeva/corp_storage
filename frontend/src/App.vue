<template>
  <PageHeader />
  <main>
      <router-view></router-view>
  </main>
</template>

<script setup>
import { onBeforeMount, onMounted, onUnmounted } from 'vue';
import PageHeader from './components/PageHeader.vue';
import { useNotificationsStore } from './store/notifications';

const store = useNotificationsStore()

onBeforeMount(async () => await store.initialize())
onUnmounted(() => store.disconnectSSE())
</script>