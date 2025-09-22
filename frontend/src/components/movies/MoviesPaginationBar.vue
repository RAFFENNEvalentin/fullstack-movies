<script setup>
const props = defineProps({
  count: { type: Number, required: true },
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true }
})
const emit = defineEmits(['update:page'])
</script>

<template>
  <div class="d-flex justify-space-between align-center mt-4">
    <div class="text-caption">
      Total: {{ count }} films — page {{ page }} / {{ totalPages }}
    </div>

    <v-pagination
      v-if="totalPages > 1"
      :model-value="page"
      @update:modelValue="p => emit('update:page', p)"
      :length="totalPages"
      :total-visible="7"
      density="comfortable"
      color="primary"
    />
  </div>
</template>