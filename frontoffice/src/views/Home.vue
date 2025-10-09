<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const teamName = ref('')
const errorMessage = ref('')

function selectUser(userId) {
  // Vérifier qu'un nom d'équipe est saisi
  if (!teamName.value.trim()) {
    errorMessage.value = 'Veuillez entrer un nom d\'équipe'
    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
    return
  }

  // Nettoyer le nom pour créer un ID valide
  const cleanTeamName = teamName.value.trim()
  const teamId = 'team_' + cleanTeamName.toLowerCase()
    .replace(/[^a-z0-9]/g, '_')
    .replace(/_+/g, '_')
    .substring(0, 20)

  // Stocker dans localStorage
  localStorage.setItem('teamId', teamId)
  localStorage.setItem('teamName', cleanTeamName)

  // Rediriger vers la page du joueur
  router.push(`/${userId}`)
}
</script>

<template>
  <div class="home-container">
    <div class="welcome-box">
      <h1>🎯 Bienvenue</h1>
      <p class="subtitle">Escape Game au Musée</p>
      <p class="description">Entrez le nom de votre équipe et choisissez votre rôle</p>

      <!-- Saisie du nom d'équipe -->
      <div class="team-input-section">
        <label for="team-name" class="input-label">
          🏆 Nom de votre équipe
        </label>
        <input
          id="team-name"
          v-model="teamName"
          type="text"
          placeholder="Ex: Les Détectives, Équipe A..."
          class="team-input"
          maxlength="30"
          @keypress.enter="selectUser('team1')"
        />
        <p class="input-hint">Chaque équipe peut jouer indépendamment avec son propre nom</p>
      </div>

      <!-- Message d'erreur -->
      <transition name="fade">
        <div v-if="errorMessage" class="error-banner">
          ⚠️ {{ errorMessage }}
        </div>
      </transition>

      <div class="button-grid">
        <button
          @click="selectUser('team1')"
          class="user-button user1-button"
        >
          <div class="button-icon">👥</div>
          <div class="button-label">Équipe 1</div>
          <div class="button-subtitle">Résoudre les énigmes</div>
        </button>

        <button
          @click="selectUser('team2')"
          class="user-button user2-button"
        >
          <div class="button-icon">👥</div>
          <div class="button-label">Équipe 2</div>
          <div class="button-subtitle">Collaborer en équipe</div>
        </button>
      </div>

      <div class="info-box">
        <p>💡 <strong>Comment ça marche ?</strong></p>
        <p>Deux joueurs travaillent ensemble pour résoudre des énigmes basées sur les œuvres du musée</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.welcome-box {
  background: white;
  border-radius: 2rem;
  padding: 2.5rem;
  max-width: 600px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

h1 {
  text-align: center;
  color: #1e293b;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.subtitle {
  text-align: center;
  color: #8b5cf6;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.description {
  text-align: center;
  color: #64748b;
  font-size: 1rem;
  margin: 0 0 2rem 0;
}

/* Section de saisie du nom d'équipe */
.team-input-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 1.5rem;
  border-radius: 1rem;
  margin-bottom: 1.5rem;
  border: 2px solid #cbd5e1;
}

.input-label {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.75rem;
  text-align: center;
}

.team-input {
  width: 100%;
  padding: 1rem 1.25rem;
  font-size: 1.125rem;
  border: 2px solid #cbd5e1;
  border-radius: 0.75rem;
  text-align: center;
  font-weight: 600;
  transition: all 0.3s;
  background: white;
}

.team-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  transform: translateY(-2px);
}

.team-input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.input-hint {
  margin: 0.75rem 0 0 0;
  font-size: 0.875rem;
  color: #64748b;
  text-align: center;
  line-height: 1.4;
}

/* Message d'erreur */
.error-banner {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
  border: 2px solid #fca5a5;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.button-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.user-button {
  padding: 2rem 1rem;
  border: none;
  border-radius: 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.user1-button {
  background: linear-gradient(135deg, #667eea 0%, #4f46e5 100%);
}

.user1-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.user2-button {
  background: linear-gradient(135deg, #f093fb 0%, #a855f7 100%);
}

.user2-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4);
}

.button-icon {
  font-size: 3rem;
}

.button-label {
  font-size: 1.25rem;
  font-weight: 700;
}

.button-subtitle {
  font-size: 0.875rem;
  opacity: 0.9;
  font-weight: 400;
}

.info-box {
  background: #f1f5f9;
  padding: 1.5rem;
  border-radius: 1rem;
  text-align: center;
}

.info-box p {
  margin: 0.5rem 0;
  color: #475569;
  font-size: 0.95rem;
  line-height: 1.6;
}

.info-box strong {
  color: #1e293b;
}

/* Responsive Mobile */
@media (max-width: 640px) {
  .home-container {
    padding: 1rem;
  }

  .welcome-box {
    padding: 2rem 1.5rem;
    border-radius: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1.125rem;
  }

  .description {
    font-size: 0.95rem;
  }

  .team-input-section {
    padding: 1.25rem;
  }

  .team-input {
    font-size: 1rem;
    padding: 0.875rem 1rem;
  }

  .button-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .user-button {
    padding: 1.75rem 1rem;
  }

  .button-icon {
    font-size: 2.5rem;
  }

  .button-label {
    font-size: 1.125rem;
  }

  .button-subtitle {
    font-size: 0.8125rem;
  }

  .info-box {
    padding: 1.25rem;
  }

  .info-box p {
    font-size: 0.875rem;
  }
}

/* Responsive Petits écrans (< 400px) */
@media (max-width: 400px) {
  .welcome-box {
    padding: 1.5rem 1rem;
  }

  h1 {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .user-button {
    padding: 1.5rem 0.75rem;
  }

  .button-icon {
    font-size: 2rem;
  }

  .button-label {
    font-size: 1rem;
  }
}

/* Responsive Tablette (641px - 1024px) */
@media (min-width: 641px) and (max-width: 1024px) {
  .welcome-box {
    max-width: 550px;
    padding: 2.5rem 2rem;
  }

  .button-grid {
    gap: 1.5rem;
  }

  .user-button {
    padding: 2rem 1.25rem;
  }
}

/* Responsive Grand écran (> 1024px) */
@media (min-width: 1025px) {
  .welcome-box {
    max-width: 650px;
  }

  .user-button:active {
    transform: translateY(-3px);
  }
}
</style>
