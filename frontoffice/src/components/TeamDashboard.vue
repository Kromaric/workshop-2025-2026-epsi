<template>
  <v-container>
    <h2>Équipe {{ teamId }}</h2>

    <v-alert v-if="doorOpen" type="success" class="mb-4">
      🚪 La porte est ouverte !
    </v-alert>

    <v-alert v-if="timerExpired" type="error" class="mb-4">
      ⏱ Temps écoulé !
    </v-alert>

    <TimerDisplay :remaining="remaining" />
    <ProgressStepper :progress="progress" :levels="levels" />

    <v-btn color="primary" class="mt-4" @click="solveEnigma(3)">
      Résoudre l'énigme 3
    </v-btn>

    <v-btn color="success" class="mt-2" @click="completeLevel(2)">
      Terminer le niveau 2
    </v-btn>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import TimerDisplay from './TimerDisplay.vue'
import ProgressStepper from './ProgressStepper.vue'

const teamId = 2
const remaining = ref(0)
const timerExpired = ref(false)
const doorOpen = ref(false)
const progress = ref([])
const levels = [1, 2, 3]

async function fetchProgress() {
  const res = await axios.get(`/teams/${teamId}`)
  progress.value = res.data.progress
}

async function fetchTimer() {
  try {
    const res = await axios.get(`/teams/${teamId}/timer`)
    remaining.value = res.data.remaining_seconds
    if (remaining.value === 0) timerExpired.value = true
  } catch {
    remaining.value = 0
  }
}

function setupWebSocket() {
  const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${teamId}`)
  socket.onmessage = (event) => {
    if (event.data === 'door_unlocked') doorOpen.value = true
    if (event.data === 'timer_expired') timerExpired.value = true
    if (event.data === 'level_2_unlocked') {
      progress.value.push({ level: 2, status: 'in_progress' })
    }
  }
}

async function solveEnigma(enigmaId) {
  await axios.post('/solve_enigma', { team_id: teamId, enigma_id: enigmaId })
}

async function completeLevel(level) {
  await axios.post(`/teams/${teamId}/complete_level`, null, {
    params: { level }
  })
  fetchProgress()
}

onMounted(() => {
  fetchProgress()
  fetchTimer()
  setupWebSocket()
  setInterval(fetchTimer, 1000)
})
</script>