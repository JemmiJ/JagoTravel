<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import Footer from '@/components/layout/Footer.vue'
import '@/assets/main.css'
</script>

<template>
  <main>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <Footer />
  </main>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>