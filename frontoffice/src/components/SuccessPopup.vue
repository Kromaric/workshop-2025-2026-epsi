<script setup>
import { ref } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'continue'])

function handleContinue() {
  emit('continue')
}

function handleClose() {
  emit('close')
}
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="popup-overlay" @click.self="handleClose">
      <div class="popup-container">
        <!-- Animation de succès -->
        <div class="success-animation">
          <div class="success-checkmark">
            <div class="check-icon">
              <span class="icon-line line-tip"></span>
              <span class="icon-line line-long"></span>
              <div class="icon-circle"></div>
              <div class="icon-fix"></div>
            </div>
          </div>
        </div>

        <!-- Titre -->
        <h2 class="popup-title">🎉 Énigme Résolue !</h2>
        <p class="popup-subtitle">Bravo ! Vous avez découvert le code des natures mortes</p>

        <!-- Portrait -->
        <div class="artist-portrait">
          <div class="portrait-frame">
            <span class="portrait-icon">🎨</span>
          </div>
        </div>

        <!-- Informations sur Chardin -->
        <div class="artist-info">
          <h3 class="artist-name">Jean Siméon Chardin</h3>
          <p class="artist-dates">Paris, 1699 - 1779</p>

          <div class="info-content">
            <p class="bio-intro">
              <strong>Maître français de la nature morte</strong>
            </p>

            <div class="info-section">
              <h4>🖼️ Son art</h4>
              <p>
                Chardin est célèbre pour ses natures mortes d'une simplicité trompeuse.
                Il transforme des objets du quotidien en compositions poétiques,
                jouant avec la lumière et les textures pour créer une atmosphère contemplative unique.
              </p>
            </div>

            <div class="info-section">
              <h4>✨ Son génie</h4>
              <p>
                Contrairement aux peintres de son époque qui privilégiaient les scènes historiques,
                Chardin a élevé l'humble nature morte au rang d'art majeur. Ses œuvres capturent
                la beauté silencieuse des choses simples : fruits, ustensiles, gibier.
              </p>
            </div>

            <div class="info-section">
              <h4>🏛️ Au Louvre</h4>
              <p>
                Le Musée du Louvre conserve la plus importante collection de ses œuvres,
                témoignant de son talent exceptionnel à immortaliser l'instant et la matière.
              </p>
            </div>

            <div class="fun-fact">
              <span class="fact-icon">💡</span>
              <div class="fact-content">
                <strong>Le saviez-vous ?</strong>
                <p>
                  Chardin peignait si lentement qu'il mettait parfois des mois à terminer
                  une seule nature morte. Cette patience lui permettait de capturer chaque
                  nuance de lumière avec une précision inégalée !
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Boutons -->
        <div class="popup-actions">
          <button @click="handleContinue" class="continue-btn">
            <span>Continuer l'aventure</span>
            <span class="btn-arrow">→</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
  overflow-y: auto;
}

.popup-container {
  background: white;
  border-radius: 2rem;
  padding: 3rem 2.5rem;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animation de succès */
.success-animation {
  text-align: center;
  margin-bottom: 2rem;
}

.success-checkmark {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  position: relative;
}

.check-icon {
  width: 80px;
  height: 80px;
  position: relative;
  border-radius: 50%;
  box-sizing: content-box;
  border: 4px solid #22c55e;
  background-color: #f0fdf4;
}

.icon-line {
  height: 5px;
  background-color: #22c55e;
  display: block;
  border-radius: 2px;
  position: absolute;
  z-index: 10;
}

.icon-line.line-tip {
  top: 46px;
  left: 14px;
  width: 25px;
  transform: rotate(45deg);
  animation: checkmark-tip 0.75s;
}

.icon-line.line-long {
  top: 38px;
  right: 8px;
  width: 47px;
  transform: rotate(-45deg);
  animation: checkmark-long 0.75s;
}

@keyframes checkmark-tip {
  0% {
    width: 0;
    left: 1px;
    top: 19px;
  }
  54% {
    width: 0;
    left: 1px;
    top: 19px;
  }
  70% {
    width: 50px;
    left: -8px;
    top: 37px;
  }
  84% {
    width: 17px;
    left: 21px;
    top: 48px;
  }
  100% {
    width: 25px;
    left: 14px;
    top: 46px;
  }
}

@keyframes checkmark-long {
  0% {
    width: 0;
    right: 46px;
    top: 54px;
  }
  65% {
    width: 0;
    right: 46px;
    top: 54px;
  }
  84% {
    width: 55px;
    right: 0px;
    top: 35px;
  }
  100% {
    width: 47px;
    right: 8px;
    top: 38px;
  }
}

/* Titre */
.popup-title {
  text-align: center;
  font-size: 2.5rem;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-weight: 800;
}

.popup-subtitle {
  text-align: center;
  color: #64748b;
  font-size: 1.125rem;
  margin: 0 0 2rem 0;
}

/* Portrait */
.artist-portrait {
  text-align: center;
  margin-bottom: 2rem;
}

.portrait-frame {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
}

.portrait-icon {
  font-size: 4rem;
}

/* Informations artiste */
.artist-info {
  background: #f8fafc;
  border-radius: 1.5rem;
  padding: 2rem;
  margin-bottom: 2rem;
}

.artist-name {
  text-align: center;
  font-size: 1.75rem;
  color: #8b5cf6;
  margin: 0 0 0.25rem 0;
  font-weight: 700;
}

.artist-dates {
  text-align: center;
  color: #64748b;
  font-size: 1rem;
  margin: 0 0 1.5rem 0;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.bio-intro {
  text-align: center;
  font-size: 1.125rem;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.info-section h4 {
  color: #1e293b;
  font-size: 1.125rem;
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-section p {
  color: #475569;
  line-height: 1.7;
  margin: 0;
  font-size: 0.95rem;
}

.fun-fact {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #fbbf24;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
}

.fact-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.fact-content strong {
  display: block;
  color: #78350f;
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.fact-content p {
  color: #92400e;
  line-height: 1.6;
  margin: 0;
  font-size: 0.95rem;
}

/* Boutons */
.popup-actions {
  display: flex;
  gap: 1rem;
}

.continue-btn {
  flex: 1;
  padding: 1.25rem 2rem;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: white;
  border: none;
  border-radius: 1rem;
  font-size: 1.125rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.continue-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
}

.btn-arrow {
  font-size: 1.5rem;
  transition: transform 0.3s;
}

.continue-btn:hover .btn-arrow {
  transform: translateX(5px);
}

/* Animations de transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Scrollbar personnalisée */
.popup-container::-webkit-scrollbar {
  width: 8px;
}

.popup-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.popup-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.popup-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Responsive */
@media (max-width: 640px) {
  .popup-container {
    padding: 2rem 1.5rem;
  }

  .popup-title {
    font-size: 2rem;
  }

  .artist-name {
    font-size: 1.5rem;
  }

  .info-section h4 {
    font-size: 1rem;
  }

  .info-section p,
  .fact-content p {
    font-size: 0.875rem;
  }
}

/* Responsive Mobile */
@media (max-width: 640px) {
  .popup-overlay {
    padding: 0.5rem;
  }

  .popup-container {
    padding: 2rem 1.5rem;
    border-radius: 1.5rem;
    max-height: 95vh;
  }

  .success-checkmark {
    width: 60px;
    height: 60px;
  }

  .check-icon {
    width: 60px;
    height: 60px;
  }

  .icon-line.line-tip {
    width: 18px;
    top: 35px;
    left: 11px;
  }

  .icon-line.line-long {
    width: 35px;
    top: 29px;
    right: 6px;
  }

  .popup-title {
    font-size: 2rem;
  }

  .popup-subtitle {
    font-size: 1rem;
  }

  .portrait-frame {
    width: 100px;
    height: 100px;
  }

  .portrait-icon {
    font-size: 3rem;
  }

  .artist-info {
    padding: 1.5rem;
  }

  .artist-name {
    font-size: 1.5rem;
  }

  .artist-dates {
    font-size: 0.95rem;
  }

  .info-content {
    gap: 1.25rem;
  }

  .bio-intro {
    font-size: 1rem;
  }

  .info-section h4 {
    font-size: 1rem;
  }

  .info-section p {
    font-size: 0.875rem;
  }

  .fun-fact {
    padding: 1.25rem;
    flex-direction: column;
    text-align: center;
  }

  .fact-icon {
    font-size: 1.75rem;
  }

  .fact-content strong {
    font-size: 1rem;
  }

  .fact-content p {
    font-size: 0.875rem;
  }

  .continue-btn {
    padding: 1.125rem 1.5rem;
    font-size: 1rem;
  }
}

/* Responsive Petits écrans (< 400px) */
@media (max-width: 400px) {
  .popup-container {
    padding: 1.5rem 1rem;
  }

  .popup-title {
    font-size: 1.75rem;
  }

  .popup-subtitle {
    font-size: 0.95rem;
  }

  .artist-name {
    font-size: 1.375rem;
  }

  .info-section h4 {
    font-size: 0.95rem;
  }

  .info-section p,
  .fact-content p {
    font-size: 0.8125rem;
  }
}

/* Responsive Tablette (641px - 1024px) */
@media (min-width: 641px) and (max-width: 1024px) {
  .popup-container {
    max-width: 650px;
    padding: 2.75rem 2.25rem;
  }
}

/* Responsive Paysage mobile */
@media (max-width: 900px) and (orientation: landscape) {
  .popup-container {
    max-height: 85vh;
  }

  .success-animation {
    margin-bottom: 1rem;
  }

  .popup-title {
    font-size: 1.75rem;
    margin-bottom: 0.25rem;
  }

  .popup-subtitle {
    margin-bottom: 1rem;
  }

  .artist-portrait {
    margin-bottom: 1rem;
  }

  .portrait-frame {
    width: 80px;
    height: 80px;
  }

  .portrait-icon {
    font-size: 2.5rem;
  }

  .artist-info {
    padding: 1.5rem;
  }

  .info-content {
    gap: 1rem;
  }
}
</style>