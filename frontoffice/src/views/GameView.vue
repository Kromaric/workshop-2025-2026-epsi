<template>
  <v-container>
    <h1>Vue globale du jeu</h1>
    <v-btn color="primary" @click="startAllTimers">
        Démarrer les timers pour toutes les équipes
    </v-btn>


    <v-row>
      <v-col
        v-for="team in teams"
        :key="team.id"
        cols="12"
        md="6"
      >
        <TeamDashboard :team-id="team.id" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import TeamDashboard from '../components/TeamDashboard.vue'

// Liste des équipes à suivre
const teams = ref([
  { id: 1 },
  { id: 2 }
])

async function startAllTimers() {
  for (const team of teams.value) {
    await axios.post(`/teams/${team.id}/start_timer`, null, {
      params: { duration_seconds: 300 }
    })
  }
}

</script>