<template>
  <li class="members-item">
    <span>{{ member.login }}</span>
    <my-text-button type="button" v-if="store.projectOwner && !isFirst" @click="handleKick">Исключить из проекта</my-text-button>
  </li>
</template>

<script setup>
import { useProjectsStore } from '../store/projects';


const props = defineProps({
  member: {
    type: Object,
  },
  isOwner: Boolean,
  isFirst: Boolean
});

const store = useProjectsStore()

async function handleKick() {
  store.openKickModal(props.member.login)
}
</script>

<style lang="less">
.members-item {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  column-gap: 20px;
  padding-left: 20px;

  span {
    &::before {
      content: "";
      position: absolute;
      top: 7px;
      left: 0;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background-color: @blue;
    }
  }
}
</style>
