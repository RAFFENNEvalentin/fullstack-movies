<script setup>
const props = defineProps({
  items: { type: Array, default: () => [] },      // [{ id, fullName }]
  modelValue: { type: Array, default: () => [] }  // [ids]
})
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div>
    <div class="mb-2 text-subtitle-2">Acteurs</div>
    <v-autocomplete
      :model-value="modelValue"
      @update:modelValue="(v) => emit('update:modelValue', v)"
      :items="items"
      item-title="fullName"
      item-value="id"
      label="Sélectionner les acteurs"
      multiple
      chips
      closable-chips
      variant="outlined"
      class="mb-4"
    />
  </div>
</template>