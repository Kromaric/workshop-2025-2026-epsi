<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function selectUser(userId) {
  router.push(`/${userId}`)
}
</script>

<template>
  <div class="home-container">
    <div class="welcome-box">
      <h1>🎯 Bienvenue</h1>
      <p class="subtitle">Choisissez votre utilisateur</p>

      <div class="button-grid">
        <button
          @click="selectUser('user1')"
          class="user-button user1-button"
        >
          <div class="button-icon">👤</div>
          <div class="button-label">Utilisateur 1</div>
        </button>

        <button
          @click="selectUser('user2')"
          class="user-button user2-button"
        >
          <div class="button-icon">👤</div>
          <div class="button-label">Utilisateur 2</div>
        </button>
      </div>

      <div class="info-box">
        <p>💡 <strong>Comment ça marche ?</strong></p>
        <p>Chaque utilisateur peut activer le bouton de l'autre en temps réel via WebSocket</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.welcome-box {
  background: white;
  border-radius: 2rem;
  padding: 3rem;
  max-width: 600px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
  text-align: center;
  color: #1e293b;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #64748b;
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

.button-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.user-button {
  padding: 2rem 1rem;
  border: none;
  border-radius: 1rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
}

.user1-button {
  background: linear-gradient(135deg, #667eea 0%, #4f46e5 100%);
}

.user1-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.user2-button {
  background: linear-gradient(135deg, #f093fb 0%, #a855f7 100%);
}

.user2-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4);
}

.button-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.button-label {
  font-size: 1.125rem;
}

.info-box {
  background: #f1f5f9;
  padding: 1.5rem;
  border-radius: 1rem;
  text-align: center;
}

.info-box p {
  margin: 0.5rem 0;
  color: #475569;
  font-size: 0.875rem;
  line-height: 1.6;
}

.info-box strong {
  color: #1e293b;
}

@media (max-width: 640px) {
  .button-grid {
    grid-template-columns: 1fr;
  }
}
</style>