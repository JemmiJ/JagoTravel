<template>
  <aside class="bg-white rounded-2xl shadow-md p-4">
    <nav class="space-y-1">
      <router-link
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors"
        :class="[
          $route.path === item.path
            ? 'bg-primary-500 text-white'
            : 'text-gray-700 hover:bg-gray-100',
        ]"
      >
        <component :is="item.icon" class="w-5 h-5" />
        {{ item.label }}
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
})
</script>