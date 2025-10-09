<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ChatBox from '../components/ChatBox.vue'
import HieroglyphKeyboard from '../components/HieroglyphKeyboard.vue'
import ProgressPanel from '../components/ProgressPanel.vue'

const router = useRouter()
const isConnected = ref(false)
const messages = ref([])
const isButtonEnabled = ref(false)

// Sekhmet
const sekhmetDivinities = ref([])
const showSekhmetSelection = ref(false)
const showSekhmetSuccess = ref(false)
const sekhmetResultMessage = ref('')
const showError = ref(false)
const errorMessage = ref('')

// Progression
const teamScore = ref(0)
const progress = ref([])

let websocket = null

const currentUserId = 'team2'
const teamId = localStorage.getItem('teamId') || 'escape_team'
const teamName = localStorage.getItem('teamName') || 'Escape Team'
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
  const wsUrl = `${WS_URL}/ws/${teamId}/${currentUserId}`
  websocket = new WebSocket(wsUrl)

  websocket.onopen = () => {
    isConnected.value = true
  }

  websocket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (data.type === 'button_state') {
      isButtonEnabled.value = data.enabled
    } else if (data.type === 'chat_history') {
      messages.value = data.messages || []
    } else if (data.type === 'chat_message') {
      if (data.message && data.message.text) {
        messages.value = [...messages.value, data.message]
      }
    } else if (data.type === 'sekhmet_selection') {
      sekhmetDivinities.value = data.divinities
      showSekhmetSelection.value = true
    } else if (data.type === 'sekhmet_result') {
      const result = data.result
      if (result.success) {
        showSekhmetSuccess.value = true
        sekhmetResultMessage.value = result.message
      } else {
        showError.value = true
        errorMessage.value = result.message
        setTimeout(() => {
          showError.value = false
        }, 3000)
      }
    } else if (data.type === 'progress') {
      teamScore.value = data.data.team_score || 0
      progress.value = data.data.puzzles || []
    }
  }

  websocket.onclose = () => {
    isConnected.value = false
    setTimeout(connectWebSocket, 3000)
  }
}

function handleButtonClick() {
  if (isButtonEnabled.value && websocket) {
    websocket.send(JSON.stringify({
      action: 'button_click'
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

function handleSekhmetValidate(data) {
  if (websocket && isConnected.value) {
    websocket.send(JSON.stringify({
      action: 'validate_sekhmet',
      hieroglyph_code: data.hieroglyph_code
    }))
  }
}

function closeSekhmetSuccess() {
  showSekhmetSuccess.value = false
}

function goBack() {
  router.push('/')
}
</script>

<template>
  <div class="page-container user2-theme">
    <!-- Barre du haut -->
    <div class="top-bar">
      <button @click="goBack" class="back-button">
        ← Retour
      </button>
      <div class="team-info">
        <span class="team-icon">🏆</span>
        <span>{{ teamName }}</span>
      </div>
      <div class="user-badge">
        <span class="badge-icon">👥</span>
        <span>Équipe 2</span>
      </div>
      <div class="connection-status">
        <span class="status-dot" :class="{ connected: isConnected }"></span>
        {{ isConnected ? 'Connecté' : 'Déconnecté' }}
      </div>
    </div>

    <!-- Notification d'erreur -->
    <transition name="slide-down">
      <div v-if="showError" class="notification error">
        {{ errorMessage }}
      </div>
    </transition>

    <!-- Notification succès Sekhmet -->
    <transition name="slide-down">
      <div v-if="showSekhmetSuccess" class="notification success">
        <span>{{ sekhmetResultMessage }}</span>
        <button @click="closeSekhmetSuccess" class="close-notif">×</button>
      </div>
    </transition>

    <!-- Contenu principal -->
    <div class="main-content">
      <!-- Avant l'énigme Sekhmet : interface de base -->
      <div v-if="!showSekhmetSelection" class="waiting-section">
        <div class="content-box">
          <div class="user-badge-large">
            <div class="badge-icon-large">👥</div>
            <h1>Équipe 2</h1>
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
              {{ isButtonEnabled ? 'Activer Équipe 1' : 'En attente...' }}
            </span>
          </button>

          <div class="info-message">
            <p v-if="isButtonEnabled">
              ✨ Cliquez sur le bouton pour activer l'Équipe 1
            </p>
            <p v-else>
              ⏳ En attente que l'Équipe 1 résolve l'énigme de Chardin...
            </p>
          </div>
        </div>

        <div class="side-section">
          <ProgressPanel
            :team-score="teamScore"
            :progress="progress"
          />
          
          <ChatBox
            :messages="messages"
            :current-user-id="currentUserId"
            :disabled="!isConnected"
            @send-message="handleSendMessage"
          />
        </div>
      </div>

      <!-- Après Chardin : énigme Sekhmet avec clavier hiéroglyphique -->
      <div v-else class="sekhmet-active">
        <div class="sekhmet-section">
          <HieroglyphKeyboard
            :player-id="currentUserId"
            @validate-answer="handleSekhmetValidate"
          />
        </div>

        <div class="side-section">
          <ProgressPanel
            :team-score="teamScore"
            :progress="progress"
          />
          
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
  padding: 1.5rem;
}

.user2-theme {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
  gap: 0.75rem;
  flex-wrap: wrap;
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

.team-info {
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

.team-icon {
  font-size: 1.25rem;
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

.main-content {
  max-width: 1400px;
  margin: 0 auto;
}

.waiting-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.sekhmet-active {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.side-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.content-box {
  background: white;
  border-radius: 2rem;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.user-badge-large {
  text-align: center;
  margin-bottom: 2rem;
}

.badge-icon-large {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.user-badge-large h1 {
  color: #f5576c;
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
  margin-bottom: 0.75rem;
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.action-button.enabled:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
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
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 968px) {
  .page-container {
    padding: 1rem;
  }

  .top-bar {
    justify-content: center;
  }

  .waiting-section,
  .sekhmet-active {
    grid-template-columns: 1fr;
  }

  .content-box {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 640px) {
  .page-container {
    padding: 0.75rem;
  }

  .back-button,
  .team-info,
  .user-badge,
  .connection-status {
    padding: 0.625rem 1.25rem;
    font-size: 0.95rem;
  }

  .content-box {
    padding: 1.5rem 1.25rem;
  }
}
</style>
