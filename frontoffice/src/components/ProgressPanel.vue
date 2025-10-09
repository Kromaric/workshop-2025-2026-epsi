<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  teamScore: {
    type: Number,
    default: 0
  },
  progress: {
    type: Array,
    default: () => []
  }
})

const totalPuzzles = 2
const solvedPuzzles = computed(() => 
  props.progress.filter(p => p.is_solved).length
)

const progressPercentage = computed(() => {
  if (totalPuzzles.value === 0) return 0
  return Math.round((solvedPuzzles.value / totalPuzzles) * 100)
})
</script>

<template>
  <div class="progress-panel">
    <div class="panel-header">
      <h3>📊 Progression de l'équipe</h3>
    </div>

    <div class="stats-grid">
      <!-- Score total -->
      <div class="stat-card score-card">
        <div class="stat-icon">🏆</div>
        <div class="stat-content">
          <div class="stat-label">Score Total</div>
          <div class="stat-value">{{ teamScore }}</div>
          <div class="stat-unit">points</div>
        </div>
      </div>

      <!-- Énigmes résolues -->
      <div class="stat-card puzzles-card">
        <div class="stat-icon">🧩</div>
        <div class="stat-content">
          <div class="stat-label">Énigmes Résolues</div>
          <div class="stat-value">{{ solvedPuzzles }} / {{ totalPuzzles }}</div>
          <div class="stat-unit">{{ progressPercentage }}%</div>
        </div>
      </div>
    </div>

    <!-- Barre de progression -->
    <div class="progress-bar-container">
      <div class="progress-label">
        <span>Progression globale</span>
        <span class="progress-percent">{{ progressPercentage }}%</span>
      </div>
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>
    </div>

    <!-- Liste des énigmes -->
    <div v-if="progress.length > 0" class="puzzles-list">
      <h4>Détails des énigmes</h4>
      <div class="puzzle-items">
        <div 
          v-for="(puzzle, index) in progress" 
          :key="index"
          class="puzzle-item"
          :class="{ solved: puzzle.is_solved }"
        >
          <div class="puzzle-icon">
            {{ puzzle.is_solved ? '✅' : '🔒' }}
          </div>
          <div class="puzzle-info">
            <div class="puzzle-name">{{ puzzle.name }}</div>
            <div class="puzzle-details">
              <span v-if="puzzle.is_solved" class="puzzle-points">
                +{{ puzzle.points_earned }} points
              </span>
              <span v-if="puzzle.attempts > 0" class="puzzle-attempts">
                {{ puzzle.attempts }} tentative{{ puzzle.attempts > 1 ? 's' : '' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message si pas d'énigmes -->
    <div v-else class="empty-puzzles">
      <span class="empty-icon">🎯</span>
      <p>Commencez à résoudre des énigmes !</p>
    </div>
  </div>
</template>

<style scoped>
.progress-panel {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.panel-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1e293b;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 2px solid #e2e8f0;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.score-card {
  border-color: #fbbf24;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.puzzles-card {
  border-color: #a78bfa;
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
}

.stat-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-unit {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
}

/* Barre de progression */
.progress-bar-container {
  margin-bottom: 2rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
}

.progress-percent {
  color: #8b5cf6;
  font-size: 1rem;
}

.progress-bar {
  height: 12px;
  background: #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%);
  transition: width 0.5s ease;
  border-radius: 6px;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Liste des énigmes */
.puzzles-list {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 1.5rem;
}

.puzzles-list h4 {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  color: #1e293b;
}

.puzzle-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.puzzle-item {
  background: white;
  border-radius: 0.75rem;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 2px solid #e2e8f0;
  transition: all 0.3s;
}

.puzzle-item.solved {
  border-color: #22c55e;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.puzzle-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.puzzle-info {
  flex: 1;
}

.puzzle-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.puzzle-details {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
}

.puzzle-points {
  color: #16a34a;
  font-weight: 600;
}

.puzzle-attempts {
  color: #64748b;
}

/* Empty state */
.empty-puzzles {
  text-align: center;
  padding: 3rem 1rem;
  color: #94a3b8;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.empty-puzzles p {
  margin: 0;
  font-size: 1rem;
}

/* Responsive Mobile */
@media (max-width: 640px) {
  .progress-panel {
    padding: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .stat-card {
    padding: 1.25rem;
  }

  .stat-icon {
    font-size: 2rem;
  }

  .stat-value {
    font-size: 1.75rem;
  }

  .puzzles-list {
    padding: 1.25rem;
  }

  .puzzle-item {
    padding: 0.875rem;
  }
}
</style>
