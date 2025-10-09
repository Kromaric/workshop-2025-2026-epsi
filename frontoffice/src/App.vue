<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

#app {
  min-height: 100vh;
}
</style>
