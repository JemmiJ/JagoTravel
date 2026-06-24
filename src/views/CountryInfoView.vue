<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />

    <section class="bg-primary-800 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none select-none opacity-10">
        <div class="absolute top-8 left-12 w-48 h-48 rounded-full border border-white/30"></div>
        <div class="absolute bottom-4 right-16 w-72 h-72 rounded-full border border-white/20"></div>
      </div>
      <div class="container text-center py-16 relative animate-fade-in">
        <Globe class="w-16 h-16 mx-auto mb-4 text-gold-400" />
        <h1 class="text-4xl md:text-5xl font-display font-bold text-white mb-4">Country Information</h1>
        <p class="text-xl text-white/70">Learn about visa requirements, travel tips, and what to expect</p>
      </div>
    </section>

    <div class="container py-16 md:py-20 space-y-16">
      <div class="animate-fade-in-up">
        <label class="block text-sm font-medium text-gray-700 mb-3">Select a Destination</label>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <button
            v-for="country in countries"
            :key="country.id"
            @click="selectedCountry = country.id"
            class="p-4 rounded-xl border-2 transition-all duration-200 hover:-translate-y-1"
            :class="selectedCountry === country.id ? 'border-gold-500 bg-primary-50' : 'border-gray-200 bg-white hover:border-gold-300'"
          >
            <div class="text-4xl mb-2">{{ country.flag }}</div>
            <p class="font-semibold text-gray-900">{{ country.name }}</p>
          </button>
        </div>
      </div>

      <BaseCard v-if="currentCountry" class="overflow-hidden p-0 animate-fade-in-up">
        <div class="bg-primary-800 text-white p-6">
          <div class="flex items-center gap-4">
            <span class="text-6xl">{{ currentCountry.flag }}</span>
            <div>
              <h2 class="text-3xl font-display font-bold">{{ currentCountry.name }}</h2>
              <p class="text-gold-400">Travel Guide & Requirements</p>
            </div>
          </div>
        </div>
        <div class="p-6 md:p-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-6">
              <div v-for="(item, key) in infoItems" :key="key" class="flex items-start gap-3 hover:translate-x-0.5 transition-transform duration-200">
                <component :is="item.icon" class="w-6 h-6 text-primary-500 mt-1" />
                <div>
                  <h3 class="font-semibold text-gray-900">{{ item.label }}</h3>
                  <p class="text-gray-700">{{ currentCountry[key] }}</p>
                </div>
              </div>
            </div>
            <div class="space-y-6">
              <div class="bg-primary-50 rounded-xl p-6">
                <h3 class="font-semibold text-gray-900">Climate & Weather</h3>
                <p class="text-gray-700 mt-2">{{ currentCountry.climate }}</p>
                <p class="text-sm text-gray-600 mt-2">Timezone: {{ currentCountry.timezone }}</p>
              </div>
              <div class="bg-blue-50 rounded-xl p-6">
                <h3 class="font-semibold text-gray-900">Health Requirements</h3>
                <p class="text-gray-700 mt-2">{{ currentCountry.vaccines }}</p>
              </div>
              <div class="bg-amber-50 rounded-xl p-6">
                <h3 class="font-semibold text-gray-900">Customs Regulations</h3>
                <p class="text-gray-700 mt-2">{{ currentCountry.customs }}</p>
              </div>
            </div>
          </div>
          <div class="mt-8 pt-8 border-t border-gray-200">
            <h3 class="font-semibold text-gray-900">Local Tips</h3>
            <p class="text-gray-700 mt-2">{{ currentCountry.tips }}</p>
          </div>
        </div>
      </BaseCard>

      <div class="bg-primary-800 rounded-2xl shadow-lg p-8 text-center text-white animate-fade-in-up">
        <h2 class="text-2xl font-display font-bold mb-3">Ready to Book Your Flight?</h2>
        <p class="text-white/70 mb-6">Start planning your trip to {{ currentCountry?.name }} today</p>
        <router-link to="/flight-search">
          <BaseButton size="lg">Search Flights</BaseButton>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Globe, FileText, DollarSign, Plane, MapPin } from 'lucide-vue-next'

const selectedCountry = ref('usa')

const countries = [
  {
    id: 'usa',
    name: 'United States',
    flag: '🇺🇸',
    visa: 'Jamaican citizens require a valid US visa',
    passport: 'Passport must be valid for at least 6 months beyond stay',
    currency: 'US Dollar (USD)',
    language: 'English',
    timezone: 'EST/EDT (UTC-5/-4)',
    climate: 'Varies by region - temperate to tropical',
    vaccines: 'No special vaccines required',
    customs: 'Declare items over $800, no fresh food',
    tips: 'Tipping 15-20% is customary in restaurants',
  },
  {
    id: 'uk',
    name: 'United Kingdom',
    flag: '🇬🇧',
    visa: 'Jamaican citizens require a UK visitor visa',
    passport: 'Passport must be valid for duration of stay',
    currency: 'British Pound (GBP)',
    language: 'English',
    timezone: 'GMT/BST (UTC+0/+1)',
    climate: 'Temperate maritime climate',
    vaccines: 'No special vaccines required',
    customs: 'Declare items over £390, restrictions on food',
    tips: 'Tipping 10-15% in restaurants if service not included',
  },
  {
    id: 'canada',
    name: 'Canada',
    flag: '🇨🇦',
    visa: 'Electronic Travel Authorization (eTA) required',
    passport: 'Passport must be valid for duration of stay plus one day',
    currency: 'Canadian Dollar (CAD)',
    language: 'English and French',
    timezone: 'Multiple zones - EST to PST',
    climate: 'Varies - cold winters, warm summers',
    vaccines: 'No special vaccines required',
    customs: 'Declare items over CAD $800, restrictions on food and plants',
    tips: 'Tipping 15-20% is customary',
  },
]

const currentCountry = computed(() => countries.find(c => c.id === selectedCountry.value) || countries[0])

const infoItems = {
  visa: { icon: FileText, label: 'Visa Requirements' },
  passport: { icon: Plane, label: 'Passport Validity' },
  currency: { icon: DollarSign, label: 'Currency' },
  language: { icon: MapPin, label: 'Language' },
}
</script>