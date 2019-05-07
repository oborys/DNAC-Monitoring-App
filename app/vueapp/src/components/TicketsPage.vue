<template>
  <t-cio-view v-if="['CIO', 'Admin'].includes(user_role)"></t-cio-view>
  <t-dev-view v-else-if="user_role === 'DevOps'"></t-dev-view>
  <t-dir-view v-else-if="user_role === 'ITDirector'"></t-dir-view>
</template>

<script>
  module.exports = {
    name: 'tickets-page',

    data: function () {
      return {
        user_role: this.$root.user_role
      }
    }
  }
</script>

<style scoped>

</style>
