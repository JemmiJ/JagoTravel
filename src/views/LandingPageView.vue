<template>
  <div class="bg-gradient-to-b from-primary-50/30 to-white">
    <NavigationBar />

    <!-- Hero with green gradient -->
    <section class="container text-center py-16 md:py-24">
      <div class="inline-block px-8 py-3 bg-gradient-to-r from-primary-600 to-primary-800 rounded-full text-white text-sm font-semibold mb-6">
        ✈️ Travel with confidence
      </div>
      <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
        Welcome to Jago Travel
      </h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        Your journey begins here. Explore, book, and travel with ease.
      </p>
    </section>

    <!-- Why Choose -->
    <section class="container py-12">
      <BaseCard class="max-w-4xl mx-auto">
        <h2 class="text-2xl font-semibold text-center mb-8">Why Choose Jago Travel?</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title" class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <component :is="feature.icon" class="w-8 h-8 text-primary-600" />
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
            <p class="text-sm text-gray-600">{{ feature.desc }}</p>
          </div>
        </div>
      </BaseCard>
    </section>

    <!-- Cards Grid with green gradients -->
    <section class="container py-12">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          v-for="card in cards"
          :key="card.title"
          :to="card.link"
          class="group relative bg-gradient-to-br rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 p-6 text-white"
          :class="card.color"
        >
          <component :is="card.icon" class="w-12 h-12 mb-4 group-hover:scale-110 transition-transform" />
          <h3 class="text-xl font-semibold mb-2">{{ card.title }}</h3>
          <p class="text-white/90">{{ card.description }}</p>
          <span class="absolute bottom-4 right-4 text-white/50 text-sm font-medium">→</span>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { Plane, DollarSign, Bell, Car, Info, Globe, Gift, Bus } from 'lucide-vue-next'

const features = [
  { icon: DollarSign, title: 'Total Cost Transparency', desc: 'See all fees upfront with no hidden charges' },
  { icon: Bell, title: 'Trip Autopilot', desc: 'Automated reminders and travel guidance' },
  { icon: Car, title: 'Ground Transport', desc: 'Seamless airport transfers and shuttle services' },
]

const cards = [
  { title: 'Book Now', description: 'Search and book flights to your dream destinations', icon: Plane, link: '/flight-search', color: 'from-primary-500 to-primary-700' },
  { title: 'About Us', description: 'Learn more about Jago Travel and our mission', icon: Info, link: '/aboutus', color: 'from-green-600 to-green-800' },
  { title: 'Flight Info', description: 'Get information about your flight requirements', icon: Plane, link: '/flight-info', color: 'from-teal-600 to-teal-800' },
  { title: 'Country Info', description: 'Discover visa, passport and travel requirements', icon: Globe, link: '/country-info', color: 'from-emerald-600 to-emerald-800' },
  { title: 'Packages & Deals', description: 'Explore our exclusive packages and special offers', icon: Gift, link: '/flight-packages', color: 'from-amber-600 to-amber-800' },
  { title: 'Shuttle Service', description: 'Book convenient airport shuttle services', icon: Bus, link: '/shuttle-service', color: 'from-indigo-600 to-indigo-800' },
]
</script>