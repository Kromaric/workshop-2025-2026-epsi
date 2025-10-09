<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  playerId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['validate-answer'])

// Hiéroglyphes disponibles h3-h6-h5-h10
const hieroglyphs = [
  { id: 'h1', symbol: '𓋴', name: 'Hiéroglyphe 1' },
  { id: 'h2', symbol: '𓊵', name: 'Hiéroglyphe 2' },
  { id: 'h3', symbol: '𓌂', name: 'Hiéroglyphe 3' },
  { id: 'h4', symbol: '𓐍', name: 'Hiéroglyphe 4' },
  { id: 'h5', symbol: '𓏏', name: 'Hiéroglyphe 5' },
  { id: 'h6', symbol: '𓅓', name: 'Hiéroglyphe 6' },
  { id: 'h7', symbol: '𓏤', name: 'Hiéroglyphe 7' },
  { id: 'h8', symbol: '𓆓', name: 'Hiéroglyphe 8' },
  { id: 'h9', symbol: '𓇋', name: 'Hiéroglyphe 9' },
  { id: 'h10', symbol: '𓆗', name: 'Hiéroglyphe 10' },
  { id: 'h11', symbol: '𓂋', name: 'Hiéroglyphe 11' },
  { id: 'h12', symbol: '𓅱', name: 'Hiéroglyphe 12' }
]

const inputValue = ref([])
const isConfirming = ref(false)

const displayValue = computed(() => {
  return inputValue.value.map(h => h.symbol).join('')
})

const canValidate = computed(() => {
  return inputValue.value.length > 0 && props.playerId === 'user2'
})

function addHieroglyph(hieroglyph) {
  inputValue.value.push(hieroglyph)
}

function removeLastHieroglyph() {
  inputValue.value.pop()
}

function clearInput() {
  inputValue.value = []
}

function confirmSelection() {
  if (canValidate.value) {
    isConfirming.value = true
  }
}

function validateAnswer() {
  const hieroglyphSequence = inputValue.value.map(h => h.id).join('-')
  emit('validate-answer', {
    hieroglyph_code: hieroglyphSequence
  })
}

function cancelConfirmation() {
  isConfirming.value = false
}
</script>

<template>
  <div class="hieroglyph-keyboard">
    <!-- En-tête -->
    <div class="enigma-header">
      <div class="header-icon">𓁹</div>
      <div class="header-content">
        <h1>La Fille de Rê</h1>
        <p class="subtitle">Énigme collaborative - Utilisateur 2</p>
      </div>
    </div>

    <!-- Instructions -->
    <div class="instructions">
      <h3>🎯 Votre mission</h3>
      <div class="instruction-list">
        <div class="instruction-item">
          <span class="step-number">1</span>
          <p>Vous êtes dans la salle des divinités égyptiennes</p>
        </div>
        <div class="instruction-item">
          <span class="step-number">2</span>
          <p>L'Utilisateur 1 vous guide pour identifier la déesse Sekhmet</p>
        </div>
        <div class="instruction-item">
          <span class="step-number">3</span>
          <p>Une fois identifiée, écrivez son nom en hiéroglyphes</p>
        </div>
        <div class="instruction-item">
          <span class="step-number">4</span>
          <p>Utilisez le clavier hiéroglyphique ci-dessous</p>
        </div>
      </div>
    </div>

    <!-- Contexte -->
    <div class="context-box">
      <div class="context-icon">💡</div>
      <div class="context-content">
        <p><strong>Indice :</strong> User 1 a accès au nom de Sekhmet en hiéroglyphes</p>
        <p><strong>Communication :</strong> Utilisez le chat pour qu'il vous décrive les symboles un par un</p>
        <p>Vous devez reproduire exactement la même séquence de hiéroglyphes</p>
      </div>
    </div>


    <!-- Zone d'affichage -->
    <div class="display-section">
      <h3>📝 Votre réponse en hiéroglyphes</h3>
      <div class="hieroglyph-display">
        <div v-if="inputValue.length === 0" class="placeholder">
          Cliquez sur les hiéroglyphes pour composer le nom
        </div>
        <div v-else class="hieroglyph-sequence">
          {{ displayValue }}
        </div>
      </div>
      <div class="display-actions">
        <button
          @click="removeLastHieroglyph"
          :disabled="inputValue.length === 0"
          class="delete-btn"
        >
          ⌫ Effacer
        </button>
        <button
          @click="clearInput"
          :disabled="inputValue.length === 0"
          class="clear-btn"
        >
          🗑️ Tout effacer
        </button>
      </div>
    </div>

    <!-- Clavier hiéroglyphique -->
    <div class="keyboard-section">
      <h3>⌨️ Clavier hiéroglyphique</h3>
      <div class="keyboard-grid">
        <button
          v-for="hieroglyph in hieroglyphs"
          :key="hieroglyph.id"
          @click="addHieroglyph(hieroglyph)"
          class="hieroglyph-key"
        >
          <span class="key-symbol">{{ hieroglyph.symbol }}</span>
        </button>
      </div>
    </div>

    <!-- Actions de validation -->
    <div class="actions">
      <button
        v-if="!isConfirming"
        @click="confirmSelection"
        :disabled="!canValidate"
        class="confirm-btn"
        :class="{ ready: canValidate }"
      >
        <span v-if="inputValue.length === 0">Écrivez le nom en hiéroglyphes</span>
        <span v-else>Valider ma réponse ({{ inputValue.length }} hiéroglyphes)</span>
      </button>

      <div v-else class="confirmation-box">
        <p class="confirmation-text">
          Êtes-vous sûr(e) de votre réponse ?
        </p>
        <div class="confirmation-display">
          {{ displayValue }}
        </div>
        <div class="confirmation-actions">
          <button @click="validateAnswer" class="validate-final-btn">
            ✅ Oui, valider
          </button>
          <button @click="cancelConfirmation" class="cancel-btn">
            ❌ Annuler
          </button>
        </div>
      </div>
    </div>

    <!-- Aide -->
    <div class="help-box">
      <details>
        <summary>❓ Comment utiliser les hiéroglyphes ?</summary>
        <div class="help-content">
          <p><strong>Instructions :</strong></p>
          <ul>
            <li>Cliquez sur les hiéroglyphes dans l'ordre pour composer le nom</li>
            <li>Le nom "SEKHMET" nécessite 4 hiéroglyphes</li>
            <li>Utilisez "⌫ Effacer" pour retirer le dernier hiéroglyphe</li>
            <li>Utilisez "🗑️ Tout effacer" pour recommencer</li>
          </ul>
          <p class="help-note">💬 Communiquez avec l'Utilisateur 1 pour confirmer la bonne divinité !</p>
        </div>
      </details>
    </div>
  </div>
</template>

<style scoped>
.hieroglyph-keyboard {
  background: white;
  border-radius: 2rem;
  padding: 2.5rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

/* En-tête */
.enigma-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #f1f5f9;
}

.header-icon {
  font-size: 4rem;
}

.header-content h1 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 2rem;
}

.subtitle {
  margin: 0;
  color: #a855f7;
  font-weight: 600;
}

/* Instructions */
.instructions {
  background: #f8fafc;
  border-radius: 1.25rem;
  padding: 2rem;
  margin-bottom: 2rem;
}

.instructions h3 {
  margin: 0 0 1.5rem 0;
  color: #1e293b;
}

.instruction-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.instruction-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 0.75rem;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #a855f7 0%, #f093fb 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  flex-shrink: 0;
}

.instruction-item p {
  margin: 0;
  color: #475569;
  line-height: 1.6;
}

/* Contexte */
.context-box {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 3px solid #f59e0b;
  border-radius: 1.25rem;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.context-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.context-content p {
  margin: 0.5rem 0;
  color: #78350f;
  line-height: 1.6;
}

/* Zone d'affichage */
.display-section {
  margin-bottom: 2rem;
}

.display-section h3 {
  margin: 0 0 1rem 0;
  color: #1e293b;
}

.hieroglyph-display {
  background: #f8fafc;
  border: 3px solid #cbd5e1;
  border-radius: 1rem;
  padding: 2rem;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.placeholder {
  color: #94a3b8;
  font-style: italic;
  text-align: center;
}

.hieroglyph-sequence {
  font-size: 3rem;
  letter-spacing: 0.5rem;
  color: #1e293b;
}

.display-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.delete-btn,
.clear-btn {
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #475569;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.delete-btn:disabled,
.clear-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.delete-btn:not(:disabled):hover {
  background: #fef2f2;
  border-color: #ef4444;
  color: #dc2626;
}

.clear-btn:not(:disabled):hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* Clavier */
.keyboard-section {
  margin-bottom: 2rem;
}

.keyboard-section h3 {
  margin: 0 0 1.5rem 0;
  color: #1e293b;
}

.keyboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
}

.hieroglyph-key {
  background: white;
  border: 3px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.hieroglyph-key:hover {
  border-color: #a855f7;
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.3);
}

.key-symbol {
  font-size: 2.5rem;
  color: #1e293b;
}

.key-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
}

/* Actions */
.actions {
  margin-bottom: 2rem;
}

.confirm-btn {
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
}

.confirm-btn.ready {
  cursor: pointer;
  background: linear-gradient(135deg, #a855f7 0%, #f093fb 100%);
  color: white;
}

.confirm-btn.ready:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(168, 85, 247, 0.4);
}

.confirmation-box {
  background: #fef3c7;
  border: 3px solid #f59e0b;
  border-radius: 1rem;
  padding: 2rem;
}

.confirmation-text {
  text-align: center;
  color: #78350f;
  font-size: 1.125rem;
  margin: 0 0 1rem 0;
}

.confirmation-display {
  font-size: 3rem;
  text-align: center;
  color: #1e293b;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
}

.confirmation-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.validate-final-btn {
  padding: 1rem;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.validate-final-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
}

.cancel-btn {
  padding: 1rem;
  background: white;
  color: #475569;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* Aide */
.help-box {
  background: #eff6ff;
  border: 2px solid #3b82f6;
  border-radius: 1rem;
  overflow: hidden;
}

.help-box summary {
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #1e40af;
  list-style: none;
  transition: all 0.3s;
}

.help-box summary:hover {
  background: #dbeafe;
}

.help-content {
  padding: 1.5rem;
  background: white;
  border-top: 1px solid #93c5fd;
}

.help-content p {
  margin: 0 0 1rem 0;
  color: #1e40af;
  font-weight: 600;
}

.help-content ul {
  margin: 0 0 1rem 0;
  padding-left: 1.5rem;
  color: #1e40af;
  line-height: 1.8;
}

.help-note {
  background: #fef3c7;
  padding: 1rem;
  border-radius: 0.5rem;
  color: #78350f !important;
  font-weight: 500 !important;
}

/* Responsive */
@media (max-width: 640px) {
  .hieroglyph-keyboard {
    padding: 1.5rem;
  }

  .enigma-header {
    flex-direction: column;
    text-align: center;
  }

  .header-icon {
    font-size: 3rem;
  }

  .hieroglyph-sequence {
    font-size: 2rem;
  }

  .keyboard-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .confirmation-actions {
    grid-template-columns: 1fr;
  }
}
</style>
