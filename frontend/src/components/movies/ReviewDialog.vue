<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue', 'submit'])

const open = ref(props.modelValue)
watch(() => props.modelValue, v => (open.value = v))
watch(open, v => emit('update:modelValue', v))

const grade = ref(5)
</script>

<template>
  <v-dialog v-model="open" max-width="400">
    <v-card>
      <v-card-title>Ajouter une note</v-card-title>
      <v-card-text>
        <v-select label="Note" :items="[1,2,3,4,5]" v-model="grade" variant="outlined" />
        <div class="text-caption text-medium-emphasis mt-2">
          La note doit être entre 1 et 5 (validée côté serveur).
        </div>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn variant="text" @click="open = false">Annuler</v-btn>
        <v-btn color="primary" @click="emit('submit', Number(grade))">Valider</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>