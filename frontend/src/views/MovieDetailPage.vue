<script setup>
import { onMounted, watch, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'
import { useActorsStore } from '@/stores/actors'   // NEW

const route = useRoute()
const store = useMoviesStore()
const actorsStore = useActorsStore()               // NEW

const id = computed(() => Number(route.params.id))

const reviewDialog = ref(false)
const reviewGrade = ref(5)
const saving = ref(false)
const newDescription = ref('')
const actorIds = ref([])                           // NEW

async function load() {
  await Promise.all([
    actorsStore.items.length ? Promise.resolve() : actorsStore.fetchActors(), // NEW
    store.fetchMovie(id.value),
  ])
  newDescription.value = store.selected?.description || ''
  actorIds.value = (store.selected?.actors || []).map(a => a.id)             // NEW
}

onMounted(load)
watch(() => route.params.id, load)

async function submitReview() {
  try { await store.addReview(id.value, Number(reviewGrade.value)) }
  catch (_) {}
  reviewDialog.value = false
}

async function saveDescription() {
  saving.value = true
  try {
    await store.updateMovie(id.value, {
      description: newDescription.value,
      actor_ids: actorIds.value                       // NEW
    })
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <v-container class="pa-6 d-flex flex-column fill-height">
    <!-- ... header / alerts / loader identiques ... -->

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

          <!-- Multiselect avec items préformatés depuis le store -->
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

    <!-- Dialog note inchangé -->
  </v-container>
</template>