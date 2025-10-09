<script setup>
import { ref } from 'vue'

const props = defineProps({
  enigma: {
    type: Object,
    required: true
  }
})

const showDetails = ref(true)

function toggleDetails() {
  showDetails.value = !showDetails.value
}
</script>

<template>
  <div class="schema-sekhmet">
    <!-- En-tête -->
    <div class="enigma-header">
      <div class="header-icon">🏺</div>
      <div class="header-content">
        <h1>{{ enigma.title }}</h1>
        <p class="subtitle">Vous êtes le guide - Utilisateur 1</p>
      </div>
    </div>

    <!-- L'énigme -->
    <div class="riddle-box">
      <div class="riddle-icon">📜</div>
      <p class="riddle-text">{{ enigma.riddle }}</p>
    </div>

    <!-- Instructions -->
    <div class="instructions">
      <h3>🎯 Votre rôle</h3>
      <div class="instruction-content">
        <div class="instruction-item">
          <span class="step-icon">👁️</span>
          <p>Vous avez les <strong>schémas des divinités</strong> avec leurs caractéristiques</p>
        </div>
        <div class="instruction-item">
          <span class="step-icon">💬</span>
          <p>Guidez l'<strong>Utilisateur 2</strong> via le chat en décrivant les éléments distinctifs</p>
        </div>
        <div class="instruction-item">
          <span class="step-icon">🤝</span>
          <p>User 2 observe les sculptures réelles et <strong>valide la réponse</strong></p>
        </div>
      </div>
    </div>

    <!-- Schémas des divinités -->
    <div class="schemas-section">
      <div class="section-header">
        <h3>📋 Schémas des divinités égyptiennes</h3>
        <button @click="toggleDetails" class="toggle-btn">
          {{ showDetails ? '👁️ Masquer' : '👁️ Afficher' }} les détails
        </button>
      </div>

      <div class="schemas-grid">
        <div
          v-for="divinity in enigma.divinities"
          :key="divinity.id"
          class="schema-card"
        >
          <div class="card-header">
            <h4>{{ divinity.name }}</h4>
            <span class="hieroglyphics">{{ divinity.name_hieroglyphics }}</span>
          </div>

          <!-- Image du schéma -->
          <div class="schema-image-container">
            <img
              :src="divinity.image_url"
              :alt="divinity.name"
              class="schema-image"
            />
          </div>

          <p class="card-description">{{ divinity.description }}</p>

          <!-- Caractéristiques détaillées -->
          <div v-if="showDetails" class="card-features">
            <p class="features-title">✨ Éléments distinctifs :</p>
            <ul>
              <li v-for="(feature, index) in divinity.distinctive_features" :key="index">
                {{ feature }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Aide -->
    <div class="help-box">
      <details>
        <summary>💡 Comment guider efficacement ?</summary>
        <div class="help-content">
          <p><strong>Conseils pour guider User 2 :</strong></p>
          <ul>
            <li>Décrivez la <strong>forme de la tête</strong> (lionne, chacal, scarabée...)</li>
            <li>Mentionnez les <strong>attributs</strong> (disque solaire, sceptre...)</li>
            <li>Parlez de la <strong>posture</strong> et des <strong>vêtements</strong></li>
            <li>Donnez des indices progressifs sans révéler directement le nom</li>
          </ul>
          <p class="help-example">
            <strong>Exemple :</strong> "Cherche une statue avec une tête de félin,
            elle doit avoir quelque chose de rond et rouge au-dessus de la tête"
          </p>
        </div>
      </details>
    </div>
  </div>
</template>

<style scoped>
.schema-sekhmet {
  background: white;
  border-radius: 2rem;
  padding: 2.5rem;
  max-width: 1400px;
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
  color: #d97706;
  font-weight: 600;
  font-size: 1.125rem;
}

/* Énigme */
.riddle-box {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 3px solid #f59e0b;
  border-radius: 1.5rem;
  padding: 2rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.riddle-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.riddle-text {
  font-size: 1.25rem;
  font-style: italic;
  color: #78350f;
  line-height: 1.8;
  margin: 0;
  font-weight: 500;
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

.instruction-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.instruction-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: white;
  padding: 1.25rem;
  border-radius: 0.75rem;
  border-left: 4px solid #d97706;
}

.step-icon {
  font-size: 1.75rem;
  flex-shrink: 0;
}

.instruction-item p {
  margin: 0;
  color: #475569;
  line-height: 1.7;
  font-size: 1rem;
}

/* Schémas */
.schemas-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
}

.toggle-btn {
  padding: 0.75rem 1.5rem;
  background: #f1f5f9;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  color: #475569;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-btn:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
}

.schemas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.schema-card {
  background: white;
  border: 3px solid #e2e8f0;
  border-radius: 1.25rem;
  padding: 1.5rem;
  transition: all 0.3s;
}

.schema-card:hover {
  border-color: #d97706;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(217, 119, 6, 0.2);
}

.schema-card.highlight {
  border-color: #22c55e;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.card-header {
  margin-bottom: 1rem;
  text-align: center;
}

.card-header h4 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.375rem;
  font-weight: 700;
}

.hieroglyphics {
  font-size: 1.75rem;
  color: #d97706;
  font-weight: bold;
}

.schema-image-container {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 250px;
}

.schema-image {
  max-width: 100%;
  max-height: 250px;
  object-fit: contain;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.card-description {
  text-align: center;
  color: #64748b;
  font-style: italic;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.card-features {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 0.75rem;
  padding: 1.25rem;
  margin-top: 1rem;
}

.features-title {
  margin: 0 0 0.75rem 0;
  font-weight: 700;
  color: #78350f;
  font-size: 0.95rem;
}

.card-features ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #92400e;
  font-size: 0.875rem;
  line-height: 1.9;
}

.card-features li {
  margin-bottom: 0.5rem;
}

/* Aide */
.help-box {
  background: #eff6ff;
  border: 2px solid #3b82f6;
  border-radius: 1rem;
  overflow: hidden;
}

.help-box summary {
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #1e40af;
  list-style: none;
  transition: all 0.3s;
  font-size: 1.05rem;
}

.help-box summary::-webkit-details-marker {
  display: none;
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
  line-height: 1.9;
}

.help-content li {
  margin-bottom: 0.5rem;
}

.help-example {
  background: #fef3c7;
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #f59e0b;
  margin: 0 !important;
}

/* Responsive */
@media (max-width: 968px) {
  .schema-sekhmet {
    padding: 1.5rem;
  }

  .enigma-header {
    flex-direction: column;
    text-align: center;
  }

  .header-icon {
    font-size: 3rem;
  }

  .header-content h1 {
    font-size: 1.75rem;
  }

  .riddle-box {
    flex-direction: column;
    text-align: center;
  }

  .schemas-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
  }

  .toggle-btn {
    width: 100%;
  }
}
</style>