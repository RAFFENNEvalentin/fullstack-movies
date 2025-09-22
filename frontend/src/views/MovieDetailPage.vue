<script setup>
import { onMounted, watch, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'

const route = useRoute()
const store = useMoviesStore()

const id = computed(() => Number(route.params.id))

// Dialog "Add review"
const reviewDialog = ref(false)
const reviewGrade = ref(5)

const saving = ref(false)
const newDescription = ref('')

async function load() {
  await store.fetchMovie(id.value)
  newDescription.value = store.selected?.description || ''
}

onMounted(load)
watch(() => route.params.id, load)

async function submitReview() {
  try {
    await store.addReview(id.value, Number(reviewGrade.value))
    reviewDialog.value = false
  } catch (_) { /* handled in store */ }
}

async function saveDescription() {
  saving.value = true
  try {
    await store.updateMovie(id.value, { description: newDescription.value })
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

    <v-alert v-if="store.hasError" type="error" variant="tonal" class="mb-4">
      {{ store.error }}
    </v-alert>

    <v-progress-linear v-if="store.loading" indeterminate color="primary" class="mb-4" />

    <template v-if="store.selected">
      <v-card class="mb-4">
        <v-card-title class="d-flex align-center">
          <span class="mr-4">{{ store.selected.title }}</span>
          <v-chip v-if="store.selected.average_grade != null" variant="flat" class="ml-auto">
            ⭐ {{ store.selected.average_grade.toFixed(1) }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <div class="mb-2 text-subtitle-2">Acteurs</div>
          <div class="mb-4">
            <v-chip
              v-for="a in store.selected.actors || []"
              :key="a.id"
              class="mr-2 mb-2"
              size="small"
              variant="tonal"
            >
              {{ a.first_name }} {{ a.last_name }}
            </v-chip>
            <span v-if="!store.selected.actors?.length" class="text-disabled">Aucun acteur</span>
          </div>

          <div class="mb-2 text-subtitle-2">Description</div>
          <v-textarea
            v-model="newDescription"
            rows="4"
            auto-grow
            variant="outlined"
            placeholder="Ajouter une description"
          />
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn :loading="saving" color="primary" @click="saveDescription">
            Enregistrer la description
          </v-btn>
          <v-btn color="secondary" variant="tonal" @click="reviewDialog = true">
            Ajouter une note
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <v-spacer />

    <!-- Footer neutre -->
    <div class="text-caption text-medium-emphasis">
      App Movies — détail
    </div>

    <!-- Dialog ajout review -->
    <v-dialog v-model="reviewDialog" max-width="400">
      <v-card>
        <v-card-title>Ajouter une note</v-card-title>
        <v-card-text>
          <v-select
            label="Note"
            :items="[1,2,3,4,5]"
            v-model="reviewGrade"
            variant="outlined"
          />
          <div class="text-caption text-medium-emphasis mt-2">
            La note doit être entre 1 et 5 (validée côté serveur).
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="reviewDialog = false">Annuler</v-btn>
          <v-btn color="primary" @click="submitReview">Valider</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>