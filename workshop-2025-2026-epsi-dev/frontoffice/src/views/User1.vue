<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ChatBox from '../components/ChatBox.vue'
import EnigmeChardin from '../components/EnigmeChardin.vue'
import SchemaSekhmet from '../components/SchemaSekhmet.vue'  // ✅ Nouveau composant
import SuccessPopup from '../components/SuccessPopup.vue'

const router = useRouter()
const isConnected = ref(false)
const showError = ref(false)
const showSuccessPopup = ref(false)
const showSekhmetSuccess = ref(false)
const resultMessage = ref('')
const chardinSolved = ref(false)
const messages = ref([])

// Énigmes
const sekhmetSchemas = ref(null)

let websocket = null

const currentUserId = 'user1'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

onMounted(() => {
  connectWebSocket()
})

onUnmounted(() => {
  if (websocket) {
    websocket.close()
  }
})

function connectWebSocket() {
  const wsUrl = `${WS_URL}/ws/team1/${currentUserId}`
  websocket = new WebSocket(wsUrl)

  websocket.onopen = () => {
    isConnected.value = true
  }

  websocket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (data.type === 'chardin_result') {
      const result = data.result
      resultMessage.value = result.message

      if (result.success) {
        chardinSolved.value = true
        showSuccessPopup.value = true
      } else {
        showError.value = true
        setTimeout(() => {
          showError.value = false
        }, 3000)
      }
    } else if (data.type === 'sekhmet_schemas') {
      // Recevoir les schémas Sekhmet
      sekhmetSchemas.value = data.enigma
    } else if (data.type === 'sekhmet_result') {
      const result = data.result
      if (result.success) {
        showSekhmetSuccess.value = true
        resultMessage.value = result.message
      }
    } else if (data.type === 'chat_history') {
      messages.value = data.messages || []
    } else if (data.type === 'chat_message') {
      if (data.message && data.message.text) {
        messages.value = [...messages.value, data.message]
      }
    }
  }

  websocket.onclose = () => {
    isConnected.value = false
    setTimeout(connectWebSocket, 3000)
  }
}

function handleChardinSubmit(data) {
  if (websocket && isConnected.value) {
    websocket.send(JSON.stringify({
      action: 'validate_chardin',
      code: data.code
    }))
  }
}

function handleSendMessage(messageText) {
  if (websocket && isConnected.value) {
    websocket.send(JSON.stringify({
      action: 'send_message',
      message: messageText
    }))
  }
}

function handleContinue() {
  showSuccessPopup.value = false
}

function closeSekhmetSuccess() {
  showSekhmetSuccess.value = false
}

function goBack() {
  router.push('/')
}
</script>

<template>
  <div class="page-container">
    <!-- Barre du haut -->
    <div class="top-bar">
      <button @click="goBack" class="back-btn">← Retour</button>
      <div class="user-badge">
        <span class="badge-icon">👤</span>
        <span>Utilisateur 1</span>
      </div>
      <div class="status" :class="{ connected: isConnected }">
        <span class="dot"></span>
        {{ isConnected ? 'Connecté' : 'Déconnecté' }}
      </div>
    </div>

    <!-- Notification d'erreur -->
    <transition name="slide-down">
      <div v-if="showError" class="notification error">
        ❌ {{ resultMessage }}
      </div>
    </transition>

    <!-- Notification succès Sekhmet -->
    <transition name="slide-down">
      <div v-if="showSekhmetSuccess" class="notification success">
        <span>{{ resultMessage }}</span>
        <button @click="closeSekhmetSuccess" class="close-notif">×</button>
      </div>
    </transition>

    <!-- Popup de succès Chardin -->
    <SuccessPopup
      :show="showSuccessPopup"
      @continue="handleContinue"
      @close="showSuccessPopup = false"
    />

    <!-- Avant Chardin : Énigme Chardin -->
    <div v-if="!chardinSolved" class="content">
      <EnigmeChardin
        :player-id="currentUserId"
        @submit-answer="handleChardinSubmit"
      />
    </div>

    <!-- Après Chardin : Schémas Sekhmet + Chat -->
    <div v-else class="interaction-content">
      <div class="main-grid">
        <!-- Schémas Sekhmet (User1 = Guide) -->
        <div class="schemas-section">
          <SchemaSekhmet
            v-if="sekhmetSchemas"
            :enigma="sekhmetSchemas"
          />
          <div v-else class="loading-box">
            <div class="loading-spinner">⏳</div>
            <p>Chargement des schémas...</p>
          </div>
        </div>

        <!-- Chat -->
        <div class="chat-section">
          <ChatBox
            :messages="messages"
            :current-user-id="currentUserId"
            :disabled="!isConnected"
            @send-message="handleSendMessage"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto 2rem;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.back-btn {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 0.75rem;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-badge {
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

.badge-icon {
  font-size: 1.25rem;
}

.status {
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

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ef4444;
  transition: background 0.3s;
}

.status.connected .dot {
  background: #22c55e;
  box-shadow: 0 0 8px #22c55e;
}

/* Notifications */
.notification {
  position: fixed;
  top: 2rem;
  left: 50%;
  transform: translateX(-50%);
  padding: 1.25rem 2rem;
  border-radius: 1rem;
  font-weight: 600;
  font-size: 1.125rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  max-width: 90%;
}

.notification.error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.notification.success {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.close-notif {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  flex-shrink: 0;
}

.close-notif:hover {
  background: rgba(255, 255, 255, 0.3);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.4s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.content {
  max-width: 600px;
  margin: 0 auto;
}

/* Interface après Chardin */
.interaction-content {
  max-width: 1400px;
  margin: 0 auto;
}

.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.schemas-section,
.chat-section {
  background: transparent;
}

.loading-box {
  background: white;
  border-radius: 2rem;
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-box p {
  margin: 0;
  color: #64748b;
  font-size: 1.125rem;
}

/* Responsive */
@media (max-width: 968px) {
  .page-container {
    padding: 1rem;
  }

  .top-bar {
    justify-content: center;
    gap: 0.5rem;
  }

  .main-grid {
    grid-template-columns: 1fr;
  }

  .notification {
    font-size: 1rem;
    padding: 1rem 1.5rem;
  }
}

@media (max-width: 640px) {
  .page-container {
    padding: 0.75rem;
  }

  .back-btn,
  .user-badge,
  .status {
    padding: 0.625rem 1.25rem;
    font-size: 0.95rem;
  }
}
</style>