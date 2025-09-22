<script setup>
import { onMounted, watch } from 'vue'
import { useMoviesStore } from '@/stores/movies'
import MovieCard from '@/components/movies/MovieCard.vue'
import MoviesPaginationBar from '@/components/movies/MoviesPaginationBar.vue'

const store = useMoviesStore()
onMounted(() => { store.fetchMovies(1) })
watch(() => store.page, p => { if (p) store.fetchMovies(p) })
</script>

<template>
  <v-container class="pa-6 d-flex flex-column fill-height">
    <div class="text-h5 mb-4">Movies (page {{ store.page }} / {{ store.totalPages }})</div>

    <v-alert v-if="store.hasError" type="error" variant="tonal" class="mb-4">
      {{ store.error }}
    </v-alert>
    <v-progress-linear v-if="store.loading" indeterminate color="primary" class="mb-4" />

    <v-row align="stretch">
      <v-col
        v-for="m in store.items"
        :key="m.id"
        cols="12" sm="6" md="4"
        class="d-flex"
      >
        <MovieCard :movie="m" />
      </v-col>
    </v-row>

    <v-spacer />

    <MoviesPaginationBar
      :count="store.count"
      :page="store.page"
      :totalPages="store.totalPages"
      @update:page="p => (store.page = p)"
    />
  </v-container>
</template>