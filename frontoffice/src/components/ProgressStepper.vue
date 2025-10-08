<template>
  <v-stepper v-model="activeStep">
    <v-stepper-header>
      <v-stepper-step
        v-for="level in levels"
        :key="level"
        :complete="isComplete(level)"
        :step="level"
      >
        Niveau {{ level }}
      </v-stepper-step>
    </v-stepper-header>
  </v-stepper>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ progress: Array, levels: Array })
const activeStep = ref(1)

function isComplete(level) {
  return props.progress.find(p => p.level === level)?.status === 'completed'
}
</script>