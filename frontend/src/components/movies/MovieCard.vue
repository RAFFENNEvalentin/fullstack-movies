<script setup>
const props = defineProps({
  movie: { type: Object, required: true } // seul endroit où "movie" est requis
})
</script>

<template>
  <v-card class="flex-grow-1 d-flex flex-column">
    <v-card-title>{{ movie.title }}</v-card-title>
    <v-card-subtitle>
      Moyenne: {{ movie.average_grade != null ? movie.average_grade.toFixed(1) : '—' }}
    </v-card-subtitle>
    <v-card-text class="text-body-2">
      {{ movie.description || 'Pas de description.' }}
    </v-card-text>
    <div class="mt-auto">
      <v-card-actions>
        <v-btn :to="`/movies/${movie.id}`" color="primary" variant="tonal">Voir</v-btn>
      </v-card-actions>
    </div>
  </v-card>
</template>