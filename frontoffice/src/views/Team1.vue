<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import EnigmeChardin from '../components/EnigmeChardin.vue'
import SuccessPopup from '../components/SuccessPopup.vue'
import ChatBox from '../components/ChatBox.vue'
import ProgressPanel from '../components/ProgressPanel.vue'

const router = useRouter()
const isConnected = ref(false)
const showSuccess = ref(false)
const showSuccessPopup = ref(false)
const showError = ref(false)
const resultMessage = ref('')
const enigmaSolved = ref(false)
const messages = ref([])
const isButtonEnabled = ref(false)

// Progression
const teamScore = ref(0)
const progress = ref([])

let websocket = null

const currentUserId = 'team1'
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
    console.log('✅ Connecté en tant que', currentUserId, 'équipe', teamId)
  }

  websocket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (data.type === 'chardin_result') {
      const result = data.result
      resultMessage.value = result.message

      if (result.success) {
        // Énigme résolue : afficher le popup
        enigmaSolved.value = true
        showSuccessPopup.value = true
      } else {
        // Mauvaise réponse
        showError.value = true
        setTimeout(() => {
          showError.value = false
        }, 3000)
      }
    } else if (data.type === 'button_state') {
      isButtonEnabled.value = data.enabled
    } else if (data.type === 'chat_history') {
      messages.value = data.messages || []
    } else if (data.type === 'chat_message') {
      if (data.message && data.message.text) {
        messages.value = [...messages.value, data.message]
      }
    } else if (data.type === 'progress') {
      // Mise à jour de la progression
      teamScore.value = data.data.team_score || 0
      progress.value = data.data.puzzles || []
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

function handleContinue() {
  // Fermer le popup et afficher l'interface d'interaction
  showSuccessPopup.value = false
}

function goBack() {
  // Déconnecter avant de retourner
  if (websocket) {
    websocket.close()
    websocket = null
  }
  router.push('/')
}
</script>

<template>
  <div class="page-container">
    <!-- Barre du haut -->
    <div class="top-bar">
      <button @click="goBack" class="back-btn">← Retour</button>
      <div class="team-info">
        <span class="team-icon">🏆</span>
        <span>{{ teamName }}</span>
      </div>
      <div class="user-badge">
        <span class="badge-icon">👥</span>
        <span>Équipe 1</span>
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

    <!-- Popup de succès -->
    <SuccessPopup
      :show="showSuccessPopup"
      @continue="handleContinue"
      @close="showSuccessPopup = false"
    />

    <!-- Contenu principal -->
    <div v-if="!enigmaSolved" class="content">
      <!-- Colonne 1 : Énigme Chardin -->
      <div class="enigme-section">
        <EnigmeChardin
          :player-id="currentUserId"
          @submit-answer="handleChardinSubmit"
        />
      </div>
      
      <!-- Colonne 2 : Score + Chat (dans la même colonne) -->
      <div class="score-chat-column">
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

    <!-- Interface d'interaction après résolution -->
    <div v-else class="interaction-content">
      <!-- Colonne 1 : Score + Chat (dans la même colonne) -->
      <div class="score-chat-column">
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

      <!-- Colonne 2 : Section Bouton -->
      <div class="button-section">
        <div class="section-card">
          <h2>🔘 Interaction</h2>

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
            {{ isButtonEnabled ? 'Activer Team 2' : 'En attente...' }}
          </button>

          <p class="info-text">
            {{ isButtonEnabled
              ? '✨ Cliquez pour activer le bouton de l\'Équipe 2'
              : '⏳ Attendez que l\'Équipe 2 vous active'
            }}
          </p>
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

/* Layout Desktop - 2 colonnes */
.content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
}

.enigme-section {
  display: flex;
  flex-direction: column;
}

/* Colonne Score + Chat */
.score-chat-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Interface d'interaction - 2 colonnes */
.interaction-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.section-card {
  background: white;
  border-radius: 2rem;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.section-card h2 {
  text-align: center;
  color: #1e293b;
  font-size: 1.75rem;
  margin: 0 0 2rem 0;
}

/* État du bouton */
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

/* Bouton d'action */
.action-button {
  width: 100%;
  padding: 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  border: none;
  border-radius: 1rem;
  cursor: not-allowed;
  background: #cbd5e1;
  color: #94a3b8;
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

.info-text {
  text-align: center;
  padding: 1rem;
  background: #f1f5f9;
  border-radius: 0.75rem;
  color: #475569;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* Responsive Mobile */
@media (max-width: 968px) {
  .page-container {
    padding: 1rem;
  }

  .top-bar {
    justify-content: center;
    gap: 0.5rem;
  }

  .back-btn,
  .team-info,
  .user-badge,
  .status {
    padding: 0.625rem 1.25rem;
    font-size: 0.95rem;
  }

  .content,
  .interaction-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .section-card {
    padding: 2rem 1.5rem;
  }
}
</style>
