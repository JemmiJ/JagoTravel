<template>
  <div>
    <NavigationBar />

    <!-- Hero -->
    <section class="bg-primary-800 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none select-none opacity-10">
        <div class="absolute top-8 left-12 w-48 h-48 rounded-full border border-white/30"></div>
        <div class="absolute bottom-4 right-16 w-72 h-72 rounded-full border border-white/20"></div>
        <div class="absolute top-1/2 left-1/3 w-32 h-32 rounded-full border border-white/15"></div>
      </div>
      <div class="container py-20 md:py-28 text-center relative animate-fade-in">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-gold-500/40 text-gold-400 text-sm font-medium mb-8 bg-gold-500/10">
          <Plane class="w-4 h-4" />
          Jamaica's trusted flight booking platform
        </div>
        <h1 class="text-4xl md:text-6xl font-display font-bold text-white mb-5 leading-tight">
          Your journey starts<br class="hidden md:block" />
          <span class="text-gold-400">in Jamaica</span>
        </h1>
        <p class="text-lg text-white/65 max-w-xl mx-auto mb-10">
          Search, compare and book flights from Jamaican international airports. Manage your bookings, check in online, and travel with confidence.
        </p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <router-link to="/flight-search" class="btn btn-lg bg-gold-500 hover:bg-gold-400 text-primary-900 font-bold px-8">
            <Plane class="w-5 h-5 mr-2" /> Search Flights
          </router-link>
          <router-link to="/signup" class="btn btn-lg border border-white/30 text-white hover:bg-white/10 px-8">
            Create Account
          </router-link>
        </div>
      </div>
    </section>

    <!-- Why Choose -->
    <section class="container py-16 md:py-20">
      <h2 class="text-2xl font-display font-bold text-center text-gray-900 mb-10">Why Choose Jago Travel?</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div v-for="(feature, idx) in features" :key="feature.title"
          class="text-center bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 p-6 animate-fade-in-up"
          :style="{ animationDelay: `${idx * 100}ms` }">
          <div class="w-14 h-14 bg-primary-800 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-primary-700">
            <component :is="feature.icon" class="w-7 h-7 text-gold-400" />
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
          <p class="text-sm text-gray-500 leading-relaxed font-sans">{{ feature.desc }}</p>
        </div>
      </div>
    </section>

<!-- Cards Grid -->
    <section class="bg-gray-50 py-16 md:py-20">
      <div class="container">
        <h2 class="text-2xl font-display font-bold text-center text-gray-900 mb-10">Everything in one place</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <router-link
            v-for="(card, idx) in cards"
            :key="card.title"
            :to="card.link"
            class="group bg-primary-800 rounded-2xl shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 p-6 overflow-hidden relative border border-primary-700 animate-fade-in-up"
            :style="{ animationDelay: `${idx * 100}ms` }"
          >
            <div class="w-12 h-12 bg-primary-700 rounded-xl flex items-center justify-center mb-4 group-hover:bg-gold-500/20 transition-colors border border-primary-600">
              <component :is="card.icon" class="w-6 h-6 text-gold-400" />
            </div>
            <h3 class="font-semibold text-white mb-2 group-hover:text-gold-400 transition-colors">{{ card.title }}</h3>
            <p class="text-sm text-white/55 leading-relaxed">{{ card.description }}</p>
            <span class="inline-flex items-center gap-1 text-gold-400 text-sm font-medium mt-4 group-hover:gap-2 transition-all">
              Explore <ArrowRight class="w-4 h-4" />
            </span>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'
import { Plane, DollarSign, Bell, Car, Info, Globe, Gift, Bus, ArrowRight } from 'lucide-vue-next'

const features = [
  { icon: DollarSign, title: 'Total Cost Transparency', desc: 'See all fees upfront with no hidden charges' },
  { icon: Bell,       title: 'Trip Autopilot',          desc: 'Automated reminders and travel guidance' },
  { icon: Car,        title: 'Ground Transport',         desc: 'Seamless airport transfers and shuttle services' },
]

const cards = [
  { title: 'Book Now',        description: 'Search and book flights to your dream destinations',         icon: Plane,  link: '/flight-search'   },
  { title: 'About Us',        description: 'Learn more about Jago Travel and our mission',               icon: Info,   link: '/aboutus'          },
  { title: 'Flight Info',     description: 'Get information about your flight requirements',             icon: Plane,  link: '/flight-info'      },
  { title: 'Country Info',    description: 'Discover visa, passport and travel requirements',            icon: Globe,  link: '/country-info'     },
  { title: 'Packages & Deals',description: 'Explore our exclusive packages and special offers',         icon: Gift,   link: '/flight-packages'  },
  { title: 'Shuttle Service', description: 'Book convenient airport shuttle services',                   icon: Bus,    link: '/shuttle-service'  },
]
</script>