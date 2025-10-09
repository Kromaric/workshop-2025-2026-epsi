<script setup>
import { ref, nextTick, watch } from 'vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  currentUserId: {
    type: String,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send-message'])

const messageInput = ref('')
const chatContainer = ref(null)

function sendMessage() {
  if (messageInput.value.trim()) {
    emit('send-message', messageInput.value.trim())
    messageInput.value = ''
  }
}

function handleKeyPress(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

// Auto-scroll quand de nouveaux messages arrivent
watch(() => props.messages.length, () => {
  scrollToBottom()
})

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

function isOwnMessage(userId) {
  return userId === props.currentUserId
}
</script>

<template>
  <div class="chat-box">
    <div class="chat-header">
      <div class="chat-title">
        <span class="chat-icon">💬</span>
        <h3>Chat</h3>
      </div>
      <span class="message-count">{{ messages.length }} message{{ messages.length > 1 ? 's' : '' }}</span>
    </div>

    <div ref="chatContainer" class="chat-messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message-wrapper"
        :class="{ 'own-message': isOwnMessage(msg.user_id) }"
      >
        <div class="message-bubble">
          <div class="message-header">
            <span class="message-user">
              {{ msg.user_id === 'user1' ? '👤 User 1' : '👤 User 2' }}
            </span>
            <span class="message-time">{{ formatTime(msg.timestamp) }}</span>
          </div>
          <div class="message-text">{{ msg.text }}</div>
        </div>
      </div>

      <div v-if="messages.length === 0" class="empty-state">
        <span class="empty-icon">💭</span>
        <p>Aucun message pour le moment</p>
        <p class="empty-subtitle">Commencez la conversation !</p>
      </div>
    </div>

    <div class="chat-input-container">
      <input
        v-model="messageInput"
        @keypress="handleKeyPress"
        :disabled="disabled"
        type="text"
        placeholder="Écrivez votre message..."
        class="chat-input"
      />
      <button
        @click="sendMessage"
        :disabled="!messageInput.trim() || disabled"
        class="send-button"
      >
        <span class="send-icon">📤</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-box {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 500px;
  overflow: hidden;
}

.chat-header {
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chat-icon {
  font-size: 1.5rem;
}

.chat-title h3 {
  margin: 0;
  font-size: 1.25rem;
}

.message-count {
  font-size: 0.875rem;
  opacity: 0.9;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.message-wrapper {
  display: flex;
  margin-bottom: 0.5rem;
}

.message-wrapper.own-message {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.message-bubble {
  color: #1e293b; /* ← Texte noir par défaut */
}

.own-message .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white; /* ← Texte blanc sur fond coloré */
}

.own-message .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
  gap: 1rem;
}

.message-user {
  font-size: 0.75rem;
  font-weight: 600;
  opacity: 0.8;
}

.message-time {
  font-size: 0.625rem;
  opacity: 0.6;
}

.message-text {
  font-size: 0.875rem;
  line-height: 1.4;
  word-wrap: break-word;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #94a3b8;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.empty-state p {
  margin: 0.25rem 0;
}

.empty-subtitle {
  font-size: 0.875rem;
}

.chat-input-container {
  padding: 1rem;
  background: white;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 0.75rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  transition: all 0.3s;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-input:disabled {
  background: #f1f5f9;
  cursor: not-allowed;
}

.send-button {
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 0.75rem;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  opacity: 0.5;
}

.send-icon {
  font-size: 1.25rem;
}

/* Responsive Mobile */
@media (max-width: 640px) {
  .chat-box {
    height: 450px;
    border-radius: 1rem;
  }

  .chat-header {
    padding: 0.875rem 1.25rem;
  }

  .chat-icon {
    font-size: 1.25rem;
  }

  .chat-title h3 {
    font-size: 1.125rem;
  }

  .message-count {
    font-size: 0.8125rem;
  }

  .chat-messages {
    padding: 0.875rem;
    gap: 0.625rem;
  }

  .message-bubble {
    max-width: 85%;
    padding: 0.625rem 0.875rem;
  }

  .message-header {
    margin-bottom: 0.375rem;
    gap: 0.75rem;
  }

  .message-user {
    font-size: 0.6875rem;
  }

  .message-time {
    font-size: 0.5625rem;
  }

  .message-text {
    font-size: 0.8125rem;
  }

  .empty-state {
    padding: 2rem 0.875rem;
  }

  .empty-icon {
    font-size: 2.5rem;
  }

  .empty-state p {
    font-size: 0.875rem;
  }

  .empty-subtitle {
    font-size: 0.8125rem;
  }

  .chat-input-container {
    padding: 0.875rem;
    gap: 0.625rem;
  }

  .chat-input {
    padding: 0.625rem 0.875rem;
    font-size: 0.8125rem;
  }

  .send-button {
    padding: 0.625rem 1rem;
  }

  .send-icon {
    font-size: 1.125rem;
  }
}

/* Responsive Petits écrans (< 400px) */
@media (max-width: 400px) {
  .chat-box {
    height: 400px;
  }

  .chat-header {
    padding: 0.75rem 1rem;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .message-bubble {
    max-width: 90%;
  }

  .chat-input {
    font-size: 0.875rem;
  }
}

/* Responsive Tablette (641px - 1024px) */
@media (min-width: 641px) and (max-width: 1024px) {
  .chat-box {
    height: 550px;
  }
}

/* Responsive Paysage mobile */
@media (max-width: 900px) and (orientation: landscape) {
  .chat-box {
    height: 350px;
  }

  .empty-state {
    padding: 1.5rem 0.875rem;
  }
}
</style>