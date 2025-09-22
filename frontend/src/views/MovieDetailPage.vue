<script setup>
import { onMounted, watch, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'
import { useActorsStore } from '@/stores/actors'

const route = useRoute()
const store = useMoviesStore()
const actorsStore = useActorsStore()

const id = computed(() => Number(route.params.id))

const reviewDialog = ref(false)
const reviewGrade = ref(5)
const saving = ref(false)
const newDescription = ref('')
const actorIds = ref([])

// NEW — snackbar
const snackbar = ref(false)          // NEW
const snackbarText = ref('')         // NEW

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

async function submitReview() {
  try {
    await store.addReview(id.value, Number(reviewGrade.value))
    snackbarText.value = 'Note ajoutée ✅'   // NEW
    snackbar.value = true                   // NEW
  } catch (_) {
    // l’alert d’erreur globale s’affiche déjà via store.error
  }
  reviewDialog.value = false
}

async function saveDescription() {
  saving.value = true
  try {
    await store.updateMovie(id.value, {
      description: newDescription.value,
      actor_ids: actorIds.value
    })
    snackbarText.value = 'Enregistré ✅'     // NEW
    snackbar.value = true                    // NEW
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
      <v-card class="mb-4">
        <v-card-title class="d-flex align-center">
          <span class="mr-4">{{ store.selected.title }}</span>
          <v-chip v-if="store.selected.average_grade != null" variant="flat" class="ml-auto">
            ⭐ {{ store.selected.average_grade.toFixed(1) }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <div class="mb-2 text-subtitle-2">Acteurs</div>

          <v-autocomplete
            v-model="actorIds"
            :items="actorsStore.selectItems"
            item-title="fullName"
            item-value="id"
            label="Sélectionner les acteurs"
            multiple
            chips
            closable-chips
            variant="outlined"
            class="mb-4"
          />

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
            Enregistrer
          </v-btn>
          <v-btn color="secondary" variant="tonal" @click="reviewDialog = true">
            Ajouter une note
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <v-spacer />

    <div class="text-caption text-medium-emphasis">App Movies — détail</div>

    <!-- NEW — Snackbar -->
    <v-snackbar v-model="snackbar" timeout="2200" location="bottom end">
      {{ snackbarText }}
    </v-snackbar>

    <!-- Dialog note -->
    <v-dialog v-model="reviewDialog" max-width="400">
      <v-card>
        <v-card-title>Ajouter une note</v-card-title>
        <v-card-text>
          <v-select label="Note" :items="[1,2,3,4,5]" v-model="reviewGrade" variant="outlined" />
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