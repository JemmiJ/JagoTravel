<template>
  <footer class="bg-primary-900 text-white/60">
    <div class="container py-10 flex flex-col items-center text-center gap-3">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 bg-gold-500 rounded-lg flex items-center justify-center flex-shrink-0">
          <Plane class="w-4 h-4 text-primary-900" />
        </div>
        <span class="text-lg font-display font-bold text-white tracking-wide">
          Jago<span class="text-gold-400">Travel</span>
        </span>
      </div>
      <p class="text-sm max-w-md">Connecting Jamaica to the World — making travel accessible, enjoyable, and stress-free.</p>
      <p class="text-xs">&copy; {{ year }} JagoTravel. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
import { Plane } from 'lucide-vue-next'

const year = new Date().getFullYear()
</script>
