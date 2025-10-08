<template>
  <v-card class="mb-4">
    <v-card-title>Temps restant : {{ remaining }} secondes</v-card-title>
  </v-card>
</template>

<script setup>
defineProps({ remaining: Number })
</script>