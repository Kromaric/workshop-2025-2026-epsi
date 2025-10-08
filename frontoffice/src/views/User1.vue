<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isButtonEnabled = ref(false)
const isConnected = ref(false)
let websocket = null

onMounted(() => {
  connectWebSocket()
})

onUnmounted(() => {
  if (websocket) {
    websocket.close()
  }
})

function connectWebSocket() {
  websocket = new WebSocket('ws://localhost:8000/ws/user1')

  websocket.onopen = () => {
    isConnected.value = true
    console.log('User1 connected')
  }

  websocket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'button_state') {
      isButtonEnabled.value = data.enabled
    }
  }

  websocket.onclose = () => {
    isConnected.value = false
    setTimeout(connectWebSocket, 3000)
  }

  websocket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
}

function handleButtonClick() {
  if (isButtonEnabled.value && websocket) {
    websocket.send(JSON.stringify({
      action: 'button_click'
    }))
  }
}

function goBack() {
  router.push('/')
}
</script>

<template>
  <div class="page-container user1-theme">
    <div class="top-bar">
      <button @click="goBack" class="back-button">
        ← Retour
      </button>
      <div class="connection-status">
        <span class="status-dot" :class="{ connected: isConnected }"></span>
        {{ isConnected ? 'Connecté' : 'Déconnecté' }}
      </div>
    </div>

    <div class="content-box">
      <div class="user-badge">
        <div class="badge-icon">👤</div>
        <h1>Utilisateur 1</h1>
      </div>

      <div class="state-indicator" :class="{ active: isButtonEnabled }">
        <div class="state-icon">
          {{ isButtonEnabled ? '🔓' : '🔒' }}
        </div>
        <div class="state-text">
          {{ isButtonEnabled ? 'Bouton Activé' : 'Bouton Désactivé' }}
        </div>
      </div>

      <button
        @click="handleButtonClick"
        :disabled="!isButtonEnabled"
        class="action-button"
        :class="{ enabled: isButtonEnabled }"
      >
        <span class="button-text">
          {{ isButtonEnabled ? 'Activer User 2' : 'En attente...' }}
        </span>
      </button>

      <div class="info-message">
        <p v-if="isButtonEnabled">
          ✨ Cliquez sur le bouton pour activer l'Utilisateur 2
        </p>
        <p v-else>
          ⏳ Attendez que l'Utilisateur 2 vous active
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  min-height: 100vh;
  padding: 2rem;
}

.user1-theme {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.back-button {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.75rem;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(-5px);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  color: white;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ef4444;
  transition: background 0.3s;
}

.status-dot.connected {
  background: #22c55e;
  box-shadow: 0 0 10px #22c55e;
}

.content-box {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  border-radius: 2rem;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.user-badge {
  text-align: center;
  margin-bottom: 2rem;
}

.badge-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.user-badge h1 {
  color: #4f46e5;
  font-size: 2rem;
  margin: 0;
}

.state-indicator {
  padding: 1.5rem;
  border-radius: 1rem;
  background: #fee;
  border: 3px solid #fcc;
  margin-bottom: 2rem;
  text-align: center;
  transition: all 0.3s;
}

.state-indicator.active {
  background: #efe;
  border-color: #8e8;
}

.state-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.state-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: #c00;
}

.state-indicator.active .state-text {
  color: #0a0;
}

.action-button {
  width: 100%;
  padding: 1.5rem;
  font-size: 1.25rem;
  font-weight: bold;
  border: none;
  border-radius: 1rem;
  cursor: not-allowed;
  background: #d1d5db;
  color: #6b7280;
  transition: all 0.3s;
  margin-bottom: 1.5rem;
}

.action-button.enabled {
  cursor: pointer;
  background: linear-gradient(135deg, #667eea 0%, #4f46e5 100%);
  color: white;
}

.action-button.enabled:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.action-button.enabled:active {
  transform: translateY(-1px);
}

.info-message {
  text-align: center;
  padding: 1rem;
  background: #f1f5f9;
  border-radius: 0.75rem;
}

.info-message p {
  margin: 0;
  color: #475569;
  font-size: 0.875rem;
  line-height: 1.6;
}
</style>