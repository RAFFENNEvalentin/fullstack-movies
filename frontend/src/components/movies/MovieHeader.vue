<script setup>
const props = defineProps({
  title: { type: String, required: true },
  average: { type: Number, default: null }
})
</script>

<template>
  <v-card-title class="d-flex align-center">
    <span class="mr-4">{{ title }}</span>
    <v-chip v-if="average != null" variant="flat" class="ml-auto">
      ⭐ {{ average.toFixed(1) }}
    </v-chip>
  </v-card-title>
</template>