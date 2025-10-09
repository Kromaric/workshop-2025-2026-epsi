<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

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
  websocket = new WebSocket(`ws://localhost:8000/ws/${props.userId}`)

  websocket.onopen = () => {
    isConnected.value = true
    console.log(`User ${props.userId} connected`)
  }

  websocket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (data.type === 'button_state') {
      isButtonEnabled.value = data.enabled
    }
  }

  websocket.onclose = () => {
    isConnected.value = false
    console.log(`User ${props.userId} disconnected`)

    // Reconnexion automatique après 3 secondes
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
</script>

<template>
  <div class="button-container">
    <div class="user-header">
      <h2>{{ userId }}</h2>
      <span
        class="status-indicator"
        :class="{ connected: isConnected }"
      />
    </div>

    <div class="button-state">
      {{ isButtonEnabled ? '✓ Activé' : '✗ Désactivé' }}
    </div>

    <button
      @click="handleButtonClick"
      :disabled="!isButtonEnabled"
      class="interaction-button"
      :class="{ enabled: isButtonEnabled }"
    >
      {{ isButtonEnabled ? '🔓 Cliquez ici' : '🔒 Désactivé' }}
    </button>

    <p class="info-text">
      {{ isButtonEnabled
        ? 'Cliquez pour activer l\'autre utilisateur'
        : 'En attente de l\'autre utilisateur...'
      }}
    </p>
  </div>
</template>

<style scoped>
.button-container {
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-header h2 {
  margin: 0;
  color: #4f46e5;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ef4444;
  transition: background-color 0.3s;
}

.status-indicator.connected {
  background-color: #22c55e;
}

.button-state {
  padding: 0.5rem 1rem;
  background: #fee;
  color: #c00;
  border-radius: 0.5rem;
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 600;
}

.button-state:has(+ .interaction-button.enabled) {
  background: #efe;
  color: #0a0;
}

.interaction-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.125rem;
  font-weight: bold;
  border: none;
  border-radius: 0.75rem;
  cursor: not-allowed;
  background: #d1d5db;
  color: #6b7280;
  transition: all 0.3s;
}

.interaction-button.enabled {
  cursor: pointer;
  background: #4f46e5;
  color: white;
}

.interaction-button.enabled:hover {
  background: #4338ca;
  transform: scale(1.05);
}

.info-text {
  margin-top: 1rem;
  text-align: center;
  color: #6b7280;
  font-size: 0.875rem;
}
</style>