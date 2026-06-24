<template>
  <aside class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 animate-fade-in-up">
    <nav class="space-y-1">
      <router-link
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 border-l-4"
        :class="[
          $route.path === item.path
            ? 'bg-primary-800 text-gold-400 border-gold-500'
            : 'text-gray-700 border-transparent hover:bg-primary-50 hover:text-primary-700',
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