<template>
  <div
    class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 p-6 md:p-8"
    :class="[className]"
  >
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  className: { type: String, default: '' },
})
</script>