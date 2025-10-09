<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ChatBox from '../components/ChatBox.vue'

const router = useRouter()
const isConnected = ref(false)
const messages = ref([])
const isButtonEnabled = ref(false)
let websocket = null

const currentUserId = 'user2'
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
  console.log('🔌 Connexion WebSocket à:', wsUrl)

  websocket = new WebSocket(wsUrl)

  websocket.onopen = () => {
    isConnected.value = true
    console.log('✅ User2 connecté à', wsUrl)
  }

  websocket.onmessage = (event) => {
    console.log('📨 Message reçu:', event.data)

    try {
      const data = JSON.parse(event.data)

      if (data.type === 'button_state') {
        console.log('🔘 État bouton:', data.enabled)
        isButtonEnabled.value = data.enabled

      } else if (data.type === 'chat_history') {
        console.log('📜 Historique chat:', data.messages)
        messages.value = data.messages || []

      } else if (data.type === 'chat_message') {
        console.log('💬 Nouveau message:', data.message)
        if (data.message && data.message.text) {
          messages.value = [...messages.value, data.message]
        }
      }
    } catch (error) {
      console.error('❌ Erreur parsing:', error)
    }
  }

  websocket.onclose = () => {
    isConnected.value = false
    console.log('❌ User2 déconnecté')
    setTimeout(connectWebSocket, 3000)
  }

  websocket.onerror = (error) => {
    console.error('❌ WebSocket error:', error)
  }
}

function handleButtonClick() {
  console.log('🖱️ Clic sur le bouton')

  if (isButtonEnabled.value && websocket) {
    websocket.send(JSON.stringify({
      action: 'button_click'
    }))
  }
}

function handleSendMessage(messageText) {
  console.log('📤 Envoi du message:', messageText)

  if (websocket && isConnected.value) {
    websocket.send(JSON.stringify({
      action: 'send_message',
      message: messageText
    }))
  }
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
      <div class="user-badge">
        <span class="badge-icon">👤</span>
        <span>Utilisateur 2</span>
      </div>
      <div class="connection-status">
        <span class="status-dot" :class="{ connected: isConnected }"></span>
        {{ isConnected ? 'Connecté' : 'Déconnecté' }}
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="main-content">
      <!-- Section Bouton -->
      <div class="button-section">
        <div class="content-box">
          <div class="user-badge-large">
            <div class="badge-icon-large">👤</div>
            <h1>Utilisateur 2</h1>
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
              {{ isButtonEnabled ? 'Activer User 1' : 'En attente...' }}
            </span>
          </button>

          <div class="info-message">
            <p v-if="isButtonEnabled">
              ✨ Cliquez sur le bouton pour activer l'Utilisateur 1
            </p>
            <p v-else>
              ⏳ Attendez que l'Utilisateur 1 vous active
            </p>
          </div>
        </div>
      </div>

      <!-- Section Chat -->
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

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.button-section,
.chat-section {
  background: transparent;
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
  color: #a855f7;
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
  background: linear-gradient(135deg, #f093fb 0%, #a855f7 100%);
  color: white;
}

.action-button.enabled:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4);
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

/* Responsive Mobile */
@media (max-width: 968px) {
  .page-container {
    padding: 1rem;
  }

  .top-bar {
    justify-content: center;
    gap: 0.5rem;
  }

  .back-button,
  .user-badge,
  .connection-status {
    padding: 0.625rem 1.25rem;
    font-size: 0.95rem;
  }

  .badge-icon {
    font-size: 1.125rem;
  }

  .main-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .content-box {
    padding: 2rem 1.5rem;
  }

  .user-badge-large h1 {
    font-size: 1.75rem;
  }

  .badge-icon-large {
    font-size: 3rem;
  }

  .state-indicator {
    padding: 1.25rem;
  }

  .state-icon {
    font-size: 2.5rem;
  }

  .state-text {
    font-size: 1.125rem;
  }

  .action-button {
    padding: 1.25rem;
    font-size: 1.125rem;
  }

  .info-message p {
    font-size: 0.875rem;
  }
}

/* Responsive Petits écrans (< 400px) */
@media (max-width: 400px) {
  .page-container {
    padding: 0.75rem;
  }

  .top-bar {
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .back-button,
  .user-badge,
  .connection-status {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }

  .content-box {
    padding: 1.5rem 1.25rem;
    border-radius: 1.5rem;
  }

  .user-badge-large {
    margin-bottom: 1.5rem;
  }

  .user-badge-large h1 {
    font-size: 1.5rem;
  }

  .badge-icon-large {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
  }

  .state-indicator {
    padding: 1rem;
    border-width: 2px;
    margin-bottom: 1.5rem;
  }

  .state-icon {
    font-size: 2.25rem;
    margin-bottom: 0.5rem;
  }

  .state-text {
    font-size: 1rem;
  }

  .action-button {
    padding: 1.125rem;
    font-size: 1rem;
    margin-bottom: 1.25rem;
  }

  .info-message {
    padding: 0.875rem;
  }

  .info-message p {
    font-size: 0.8125rem;
  }
}

/* Responsive Tablette (641px - 968px) */
@media (min-width: 641px) and (max-width: 968px) {
  .main-content {
    gap: 1.75rem;
  }

  .content-box {
    padding: 2.25rem;
  }

  .user-badge-large h1 {
    font-size: 1.875rem;
  }

  .badge-icon-large {
    font-size: 3.25rem;
  }
}

/* Responsive Paysage mobile */
@media (max-width: 900px) and (orientation: landscape) {
  .page-container {
    padding: 1rem;
  }

  .top-bar {
    margin-bottom: 1rem;
  }

  .main-content {
    gap: 1.25rem;
  }

  .content-box {
    padding: 1.5rem;
  }

  .user-badge-large {
    margin-bottom: 1.25rem;
  }

  .user-badge-large h1 {
    font-size: 1.5rem;
  }

  .badge-icon-large {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
  }

  .state-indicator {
    padding: 1rem;
    margin-bottom: 1.25rem;
  }

  .state-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .state-text {
    font-size: 1.125rem;
  }

  .action-button {
    padding: 1.125rem;
    font-size: 1.125rem;
    margin-bottom: 1rem;
  }

  .info-message {
    padding: 0.875rem;
  }
}

/* Responsive Desktop (> 1024px) */
@media (min-width: 1025px) {
  .back-button:active {
    transform: translateX(-3px);
  }

  .action-button.enabled:active {
    transform: translateY(0);
  }
}

/* Safe area pour iPhone X et plus */
@supports (padding: max(0px)) {
  .page-container {
    padding-left: max(1.5rem, env(safe-area-inset-left));
    padding-right: max(1.5rem, env(safe-area-inset-right));
    padding-bottom: max(1.5rem, env(safe-area-inset-bottom));
  }
}

/* Touch optimization pour mobile */
@media (hover: none) and (pointer: coarse) {
  .back-button,
  .action-button.enabled {
    min-height: 44px; /* Zone de touch minimum recommandée */
  }
}
</style>