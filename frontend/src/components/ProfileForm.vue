<template>
  <form class="form form--row" @submit.prevent="handleUpdate">
    <div class="form__fields">
      <my-field
        :label="'Имя'"
        :type="'text'"
        :placeholder="'Иван'"
      />
      <my-field
        :label="'Фамилия'"
        :type="'text'"
        :placeholder="'Иванов'"
      />
      <my-field
        :label="'Логин'"
        :type="'text'"
        :placeholder="'Иван'"
        :disabled="true"
        
      />
    </div>
    <div class="form__buttons">
        <my-button :filled="true" type="submit" 
          >Обновить данные</my-button
        >
        <my-button type="button" 
          >Удалить аккаунт</my-button
        >
    </div>
  </form>
</template>

<script setup>

</script>

<style lang="less">

</style>
