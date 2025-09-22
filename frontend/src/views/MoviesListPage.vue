<script setup>
import { onMounted, watch } from 'vue'
import { useMoviesStore } from '@/stores/movies'

const store = useMoviesStore()

// Charger la première page au montage
onMounted(() => {
  store.fetchMovies(1)
})

// Recharger quand on change de page
watch(() => store.page, (p) => {
  if (p) store.fetchMovies(p)
})
</script>

<template>
  <v-container class="pa-6">
    <div class="text-h5 mb-4">Movies (page {{ store.page }}/{{ store.totalPages }})</div>

    <!-- Affichage erreur -->
    <v-alert v-if="store.hasError" type="error" variant="tonal" class="mb-4">
      {{ store.error }}
    </v-alert>

    <!-- Spinner de chargement -->
    <v-progress-linear
      v-if="store.loading"
      indeterminate
      color="primary"
      class="mb-4"
    />

    <!-- Liste des films -->
    <v-row>
      <v-col
        v-for="m in store.items"
        :key="m.id"
        cols="12" sm="6" md="4"
      >
        <v-card>
          <v-card-title>{{ m.title }}</v-card-title>
          <v-card-subtitle>
            Moyenne: {{ m.average_grade ? m.average_grade.toFixed(1) : '—' }}
          </v-card-subtitle>
          <v-card-text>
            {{ m.description || 'Pas de description.' }}
          </v-card-text>
          <v-card-actions>
            <v-btn :to="`/movies/${m.id}`" color="primary" variant="tonal">Voir</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Pagination -->
    <div class="d-flex justify-center mt-4">
      <v-pagination
        v-model="store.page"
        :length="store.totalPages"
        color="primary"
      />
    </div>
  </v-container>
</template>