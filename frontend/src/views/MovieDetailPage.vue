<script setup>
import { onMounted, watch, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'
import { useActorsStore } from '@/stores/actors'
import MovieHeader from '@/components/movies/MovieHeader.vue'
import ActorsSelect from '@/components/movies/ActorsSelect.vue'
import DescriptionEditor from '@/components/movies/DescriptionEditor.vue'
import ReviewDialog from '@/components/movies/ReviewDialog.vue'

const route = useRoute()
const store = useMoviesStore()
const actorsStore = useActorsStore()

const id = computed(() => Number(route.params.id))

const reviewDialog = ref(false)
const saving = ref(false)
const newDescription = ref('')
const actorIds = ref([])

const snackbar = ref(false)
const snackbarText = ref('')

async function load() {
  await Promise.all([
    actorsStore.items.length ? Promise.resolve() : actorsStore.fetchActors(),
    store.fetchMovie(id.value),
  ])
  newDescription.value = store.selected?.description || ''
  actorIds.value = (store.selected?.actors || []).map(a => a.id)
}

onMounted(load)
watch(() => route.params.id, load)

async function handleSubmitReview(grade) {
  try {
    await store.addReview(id.value, grade)
    snackbarText.value = 'Note ajoutée ✅'
    snackbar.value = true
  } catch (_) {}
  reviewDialog.value = false
}

async function handleSave() {
  saving.value = true
  try {
    await store.updateMovie(id.value, {
      description: newDescription.value,
      actor_ids: actorIds.value
    })
    snackbarText.value = 'Enregistré ✅'
    snackbar.value = true
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <v-container class="pa-6 d-flex flex-column fill-height">
    <div class="d-flex align-center mb-4">
      <v-btn to="/movies" variant="text" prepend-icon="mdi-arrow-left">Retour</v-btn>
      <div class="text-h5 ml-2">Détail du film</div>
    </div>

    <v-alert v-if="store.hasError || actorsStore.error" type="error" variant="tonal" class="mb-4">
      {{ store.error || actorsStore.error }}
    </v-alert>

    <v-progress-linear
      v-if="store.loading || actorsStore.loading"
      indeterminate color="primary" class="mb-4"
    />

    <template v-if="store.selected">
      <!-- Wrapper centré avec largeur contrôlée -->
      <div class="mx-auto" style="max-width: 1100px; width: 100%;">
        <v-card class="pa-8 mb-8" elevation="3" rounded="lg">
          <MovieHeader
            :title="store.selected.title"
            :average="store.selected.average_grade"
          />

          <v-card-text>
            <ActorsSelect
              v-model="actorIds"
              :items="actorsStore.selectItems"
              class="mb-6"
            />

            <DescriptionEditor
              v-model="newDescription"
              :loading="saving"
              @save="handleSave"
            />
          </v-card-text>

          <v-card-actions class="justify-end">
            <v-btn color="secondary" variant="tonal" @click="reviewDialog = true">
              Ajouter une note
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </template>

    <v-spacer />

    <div class="text-caption text-medium-emphasis">App Movies — détail</div>

    <v-snackbar v-model="snackbar" timeout="2200" location="bottom end">
      {{ snackbarText }}
    </v-snackbar>

    <ReviewDialog
      v-model="reviewDialog"
      @submit="handleSubmitReview"
    />
  </v-container>
</template>