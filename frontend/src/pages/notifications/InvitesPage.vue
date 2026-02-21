<template>
  <div class="invites">
    <InvitesSkeleton v-if="store.invitesLoading"/>
    <div class="invites__wrapper" v-else>
      <p class="invites__none" v-if="store.notificationsInvites.length === 0">
        У вас сейчас нет приглашений
      </p>
      <div class="invites__body">
        <my-button
          type="button"
          @click="handleDeleteAll"
          v-if="store.notificationsInvites.length > 0"
          :disabled="!store.notificationsInvites.some(i => i.state !== 'Отправлено')"
          >Удалить все</my-button
        >
        <ul class="invites__list">
          <InvitesItem
            v-for="invite in store.notificationsInvites"
            :key="invite.id"
            :invite="invite"
          />
        </ul>
      </div>
    </div>
  </div>
  <DeleteAllInvites v-if="store.showAllInvitesDeleteModal"/>
</template>

<script setup>
import { onMounted, watch } from "vue";
import InvitesItem from "../../components/InvitesItem.vue";
import { useNotificationsStore } from "../../store/notifications";
import InvitesSkeleton from "../../components/skeleton/InvitesSkeleton.vue";
import DeleteAllInvites from "../../components/DeleteAllInvites.vue";

const store = useNotificationsStore();

async function handleDeleteAll() {
  await store.openAllInvitesDeleteModal()
}

watch(
  () => store.notificationsInvites.length,
  (newLength, oldLength) => {
    if (newLength > oldLength) {
      console.log("✅ Новое приглашение через SSE!");
    }
  },
  { immediate: false },
);

onMounted(async () => {
  await store.getNotificationsInvites();
});
</script>

<style lang="less">
.invites {
  &__none {
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    color: @text-tertiary;
  }

  &__body {
    display: flex;
    flex-direction: column;
    row-gap: 48px;
  }

  button {
    margin-left: auto;
  }

  &__list {
    display: flex;
    flex-direction: column;
    row-gap: 12px;
  }
}
</style>
