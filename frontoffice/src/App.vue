<script setup>
import ButtonInteraction from './components/ButtonInteraction.vue'
</script>

<template>
  <div class="app-container">
    <h1>Interaction entre utilisateurs</h1>

    <div class="users-grid">
      <ButtonInteraction userId="user1" />
      <ButtonInteraction userId="user2" />
    </div>
  </div>
</template>

<style>
.app-container {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(to bottom right, #eff6ff, #e0e7ff);
}

.app-container h1 {
  text-align: center;
  color: #1e40af;
  margin-bottom: 2rem;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>