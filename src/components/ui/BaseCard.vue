<template>
  <div
    class="bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-200 p-6 md:p-8"
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