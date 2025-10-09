<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  playerId: {
    type: String,
    default: 'team'
  }
})

const emit = defineEmits(['submit-answer'])

const userCode = ref('')
const isSubmitting = ref(false)

const isCodeValid = computed(() => {
  return /^\d{4}$/.test(userCode.value)
})

function handleInput(event) {
  userCode.value = event.target.value.replace(/\D/g, '').slice(0, 4)
}

function submitCode() {
  if (!isCodeValid.value || isSubmitting.value) return

  isSubmitting.value = true

  emit('submit-answer', {
    code: userCode.value
  })

  setTimeout(() => {
    isSubmitting.value = false
  }, 2000)
}

function handleKeyPress(event) {
  if (event.key === 'Enter' && isCodeValid.value) {
    submitCode()
  }
}
</script>

<template>
  <div class="enigma-container">
    <!-- Titre -->
    <div class="enigma-header">
      <h1>🎨 Le Code des Natures Mortes</h1>
      <p class="artist">Jean Siméon Chardin (1699-1779)</p>
    </div>

    <!-- Instructions -->
    <div class="instructions">
      <p class="main-instruction">
        Observez attentivement les <strong>4 natures mortes</strong> exposées devant vous.
      </p>

      <div class="instruction-list">
        <div class="instruction-item">
          <span>Bienvenue dans la salle dédiée à Jean Siméon Chardin, un peintre français du XVIIIè siècle.</span>
        </div>
        <div class="instruction-item">
          <span>Avant de vous pencher sur ses œuvres voici un fait étonnant sur lui: Dans ses plus belles années,
            Jean Siméon Charbin était végétarien et avait une étrange habitude, il mangeait ses plats seulement
            dans leur ordre alphabétique...</span>
        </div>
      </div>

      <p class="hint">💡 Chaque nombre forme un chiffre du code à 4 chiffres</p>
    </div>

    <!-- Saisie du code -->
    <div class="code-section">
      <label for="code" class="code-label">Entrez le code :</label>

      <div class="code-input-wrapper">
        <input
          id="code"
          v-model="userCode"
          @input="handleInput"
          @keypress="handleKeyPress"
          type="text"
          inputmode="numeric"
          maxlength="4"
          placeholder="____"
          class="code-input"
          :disabled="isSubmitting"
          autofocus
        />

        <div class="code-display">
          <span
            v-for="i in 4"
            :key="i"
            class="digit"
            :class="{ filled: userCode.length >= i }"
          >
            {{ userCode[i - 1] || '_' }}
          </span>
        </div>
      </div>

      <button
        @click="submitCode"
        :disabled="!isCodeValid || isSubmitting"
        class="submit-btn"
        :class="{ ready: isCodeValid && !isSubmitting }"
      >
        <span v-if="isSubmitting">⏳ Vérification...</span>
        <span v-else-if="!isCodeValid">Entrez 4 chiffres</span>
        <span v-else>Valider</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.enigma-container {
  background: white;
  border-radius: 1.5rem;
  padding: 2.5rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

/* En-tête */
.enigma-header {
  text-align: center;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f1f5f9;
}

.enigma-header h1 {
  margin: 0 0 0.75rem 0;
  font-size: 2rem;
  color: #1e293b;
}

.artist {
  margin: 0;
  font-size: 1rem;
  color: #8b5cf6;
  font-weight: 600;
}

/* Instructions */
.instructions {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
}

.main-instruction {
  text-align: center;
  font-size: 1.125rem;
  color: #475569;
  margin: 0 0 1.5rem 0;
  line-height: 1.6;
}

.instruction-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.instruction-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.instruction-item span:last-child {
  color: #475569;
  line-height: 1.5;
}

.hint {
  text-align: center;
  background: #fef3c7;
  padding: 1rem;
  border-radius: 0.75rem;
  margin: 0;
  color: #78350f;
  font-weight: 600;
}

/* Code */
.code-section {
  text-align: center;
}

.code-label {
  display: block;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.code-input-wrapper {
  position: relative;
  margin-bottom: 1.5rem;
}

.code-input {
  width: 100%;
  padding: 1.5rem;
  font-size: 3rem;
  text-align: center;
  letter-spacing: 2rem;
  border: 3px solid #e2e8f0;
  border-radius: 1rem;
  color: transparent;
  caret-color: #8b5cf6;
  transition: all 0.3s;
}

.code-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.code-input:disabled {
  background: #f1f5f9;
  cursor: not-allowed;
}

.code-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 1.5rem;
  pointer-events: none;
}

.digit {
  width: 70px;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 3px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 3rem;
  font-weight: 700;
  color: #cbd5e1;
  transition: all 0.3s;
}

.digit.filled {
  border-color: #8b5cf6;
  color: #8b5cf6;
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  transform: scale(1.05);
}

/* Bouton */
.submit-btn {
  width: 100%;
  padding: 1.25rem;
  font-size: 1.25rem;
  font-weight: 700;
  border: none;
  border-radius: 1rem;
  cursor: not-allowed;
  background: #cbd5e1;
  color: #94a3b8;
  transition: all 0.3s;
}

.submit-btn.ready {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  cursor: pointer;
}

.submit-btn.ready:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
}

.submit-btn.ready:active {
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 640px) {
  .enigma-container {
    padding: 1.5rem;
  }

  .enigma-header h1 {
    font-size: 1.5rem;
  }

  .code-input {
    font-size: 2rem;
    letter-spacing: 1rem;
  }

  .code-display {
    gap: 0.75rem;
  }

  .digit {
    width: 50px;
    height: 70px;
    font-size: 2rem;
  }
}
</style>
