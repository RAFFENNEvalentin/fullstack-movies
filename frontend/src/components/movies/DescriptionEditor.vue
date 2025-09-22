<script setup>
const props = defineProps({
  modelValue: { type: String, default: '' },
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue', 'save'])
</script>

<template>
  <div>
    <div class="mb-2 text-subtitle-2">Description</div>
    <v-textarea
      :model-value="modelValue"
      @update:modelValue="(v) => emit('update:modelValue', v)"
      rows="4"
      auto-grow
      variant="outlined"
      placeholder="Ajouter une description"
    />
    <div class="d-flex justify-end mt-2">
      <v-btn :loading="loading" color="primary" @click="emit('save')">
        Enregistrer
      </v-btn>
    </div>
  </div>
</template>