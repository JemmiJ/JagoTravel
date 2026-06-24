<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />

    <section class="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16">
      <div class="container text-center">
        <Globe class="w-16 h-16 mx-auto mb-4" />
        <h1 class="text-4xl font-bold mb-4">Country Information</h1>
        <p class="text-xl text-primary-100">Learn about visa requirements, travel tips, and what to expect</p>
      </div>
    </section>

    <div class="container py-12 space-y-8">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-3">Select a Destination</label>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <button
            v-for="country in countries"
            :key="country.id"
            @click="selectedCountry = country.id"
            class="p-4 rounded-xl border-2 transition-all"
            :class="selectedCountry === country.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200 bg-white hover:border-primary-300'"
          >
            <div class="text-4xl mb-2">{{ country.flag }}</div>
            <p class="font-semibold text-gray-900">{{ country.name }}</p>
          </button>
        </div>
      </div>

      <BaseCard v-if="currentCountry" class="overflow-hidden p-0">
        <div class="bg-gradient-to-r from-primary-600 to-primary-800 text-white p-6">
          <div class="flex items-center gap-4">
            <span class="text-6xl">{{ currentCountry.flag }}</span>
            <div>
              <h2 class="text-3xl font-bold">{{ currentCountry.name }}</h2>
              <p class="text-primary-100">Travel Guide & Requirements</p>
            </div>
          </div>
        </div>
        <div class="p-6 md:p-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-6">
              <div v-for="(item, key) in infoItems" :key="key" class="flex items-start gap-3">
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

      <div class="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl shadow-lg p-8 text-center text-white">
        <h2 class="text-2xl font-bold mb-3">Ready to Book Your Flight?</h2>
        <p class="text-primary-100 mb-6">Start planning your trip to {{ currentCountry?.name }} today</p>
        <router-link to="/flight-search">
          <BaseButton variant="ghost" class="bg-white text-primary-600 hover:bg-gray-100">Search Flights</BaseButton>
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
    visa: 'Passengers must have a valid visa issued by the USA.Immediate family members of nationals of Colombia, Cuba, Ecuador, El Salvador, Guatemala, Haiti, Honduras, Nicaragua and Venezuela traveling under the Family Reunification Parole (FRP) or of nationals of Ukraine traveling under "United for Ukraine" status process do not need a visa if they: - have an approved Advance Travel Authorization (ATA) issued by U.S. Customs and Border Protection (CBP) to seek parole; and - have a valid passport; and - travel together with the national of Colombia, Cuba, Ecuador, El Salvador, Guatemala, Haiti, Honduras, Nicaragua, Ukraine or Venezuela or contact the U.S   Customs and Border Protection (CBP). Immediate family members may be of any nationality and are limited to spouse or common-law partner and unmarried children under the age of 21. Passengers can check the status of their ATA at https://my.uscis.gov/ .',
    passport: 'Passport must be valid for at least 6 months beyond stay. Passports issued to nationals of Jamaica must be valid for the duration of stay. Passengers who have been in Congo (Dem. Rep.), Uganda or South Sudan in the last 21 days are not allowed to enter.',
    currency: 'US Dollar (USD)',
    language: 'English',
    timezone: 'EST/EDT (UTC-5/-4)',
    climate: 'Varies by region - temperate to tropical',
    vaccines: 'Yellow Fever Vaccination Information',
    customs: 'Declare items over $800, no fresh food',
    tips: 'Tipping 15-20% is customary in restaurants',
  },
  {
    id: 'Aus',
    name: 'Australia',
    flag: '🇦🇺',
    visa: 'Jamaican citizens require a AU visitor visa',
    passport: 'Passport must be valid for duration of stay',
    currency: 'Australian Dollar (AUD)',
    language: 'English',
    timezone: 'AEST (UTC+10)',
    climate: 'Average temperature',
    vaccines: 'Yellow Fever Vaccination Information',
    customs: 'Declare items over AUD390, restrictions on food',
    tips: 'Tipping 10-15% in restaurants if service not included',
  },
  {
    id: 'china',
    name: 'China',
    flag: '🇨🇳',
    visa: 'Passengers must have a valid visa issued by China (Peoples Rep.)',
    passport: 'Travel documents must be valid for the duration of stay. Passengers with a visa must have travel documents valid upon arrival.',
    currency: 'Chinese Yuan (CNY)',
    language: 'Mandarin',
    timezone: 'China Standard Time(CST) - UTC +8',
    climate: 'annual temperature is above 68 °F',
    vaccines: 'Yellow Fever Vaccination Information',
    customs: 'Declare items over CNY$800, restrictions on food and plants',
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