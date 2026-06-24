<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />

    <section class="bg-primary-800 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none select-none opacity-10">
        <div class="absolute top-8 left-12 w-48 h-48 rounded-full border border-white/30"></div>
        <div class="absolute bottom-4 right-16 w-72 h-72 rounded-full border border-white/20"></div>
      </div>
      <div class="container text-center py-16 relative animate-fade-in">
        <Bus class="w-16 h-16 mx-auto mb-4 text-gold-400" />
        <h1 class="text-4xl md:text-5xl font-display font-bold text-white mb-4">Shuttle Service</h1>
        <p class="text-xl text-white/70">Reliable airport transfers and ground transportation</p>
      </div>
    </section>

    <div class="container py-16 md:py-20 space-y-16">
      <BaseCard>
        <h2 class="text-2xl font-display font-bold text-gray-900 mb-6">Book Your Shuttle</h2>
        <form @submit.prevent="handleSearch" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <BaseSelect
              v-model="pickupLocation"
              label="Pickup Location"
              :options="locations.map(l => ({ value: l, label: l }))"
              placeholder="Select pickup location"
            />
            <BaseSelect
              v-model="dropoffLocation"
              label="Drop-off Location"
              :options="locations.map(l => ({ value: l, label: l }))"
              placeholder="Select drop-off location"
            />
            <BaseInput v-model="date" label="Date & Time" type="datetime-local" />
            <BaseSelect
              v-model="passengers"
              label="Passengers"
              :options="[1,2,3,4,5,6,7,8].map(n => ({ value: n, label: `${n} ${n === 1 ? 'Passenger' : 'Passengers'}` }))"
            />
          </div>
          <BaseButton type="submit" size="lg" block>Search Available Shuttles</BaseButton>
        </form>
      </BaseCard>

      <div>
        <h2 class="text-2xl font-display font-bold text-gray-900 mb-8">Available Shuttle Options</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <BaseCard
            v-for="(shuttle, idx) in shuttleOptions"
            :key="shuttle.name"
            class="overflow-hidden p-0 animate-fade-in-up"
            :style="{ animationDelay: `${idx * 100}ms` }"
          >
            <div class="bg-primary-800 text-white p-6 text-center">
              <component :is="shuttle.icon" class="w-12 h-12 text-gold-400 mx-auto mb-3" />
              <h3 class="text-xl font-display font-bold">{{ shuttle.name }}</h3>
              <p class="text-white/70 text-sm">{{ shuttle.type }}</p>
            </div>
            <div class="p-6 md:p-8 space-y-3">
              <div class="flex items-center gap-2 text-gray-700">
                <Clock class="w-5 h-5 text-primary-500" />
                <span>{{ shuttle.duration }}</span>
              </div>
              <div class="flex items-center gap-2 text-gray-700">
                <Users class="w-5 h-5 text-primary-500" />
                <span>{{ shuttle.capacity }}</span>
              </div>
              <div class="flex items-center gap-2 text-gray-700">
                <DollarSign class="w-5 h-5 text-primary-500" />
                <span class="text-2xl font-bold text-gold-600">${{ shuttle.price.toLocaleString() }}</span>
                <span class="text-sm text-gray-600">JMD</span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-700 mb-2">Features:</p>
                <ul class="space-y-1">
                  <li v-for="(feature, i) in shuttle.features" :key="i" class="text-sm text-gray-600 flex items-center gap-2">
                    <span class="w-1.5 h-1.5 bg-primary-500 rounded-full"></span>
                    {{ feature }}
                  </li>
                </ul>
              </div>
              <BaseButton size="md" block>Book Now</BaseButton>
            </div>
          </BaseCard>
        </div>
      </div>

      <div class="bg-primary-800 rounded-2xl shadow-lg p-8 text-white text-center animate-fade-in-up">
        <h2 class="text-2xl font-display font-bold mb-6">Why Choose Our Shuttle Service?</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="item in whyItems" :key="item.title" class="group">
            <div class="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-3 transition-colors group-hover:bg-gold-500/20">
              <component :is="item.icon" class="w-8 h-8 text-gold-400" />
            </div>
            <h3 class="font-semibold mb-2">{{ item.title }}</h3>
            <p class="text-white/70 text-sm">{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { Bus, MapPin, Clock, DollarSign, Users, Calendar, Car, Caravan } from 'lucide-vue-next'

const pickupLocation = ref('')
const dropoffLocation = ref('')
const date = ref('')
const passengers = ref(1)

const locations = [
  'Norman Manley International Airport (KIN)',
  'Sangster International Airport (MBJ)',
  'Kingston - New Kingston',
  'Kingston - Downtown',
  'Montego Bay - Hip Strip',
  'Ocho Rios',
  'Negril',
  'Port Antonio',
]

const shuttleOptions = [
  {
    name: 'Airport Express',
    type: 'Shared Shuttle',
    price: 2500,
    duration: '45-60 mins',
    capacity: 'Up to 12 passengers',
    features: ['Air conditioned', 'WiFi', 'Luggage storage'],
    icon: Bus,
  },
  {
    name: 'Premium Private Transfer',
    type: 'Private Car',
    price: 8000,
    duration: '35-45 mins',
    capacity: 'Up to 4 passengers',
    features: ['Air conditioned', 'WiFi', 'Refreshments', 'Professional driver'],
    icon: Car,
  },
  {
    name: 'Luxury Van Service',
    type: 'Private Van',
    price: 12000,
    duration: '35-45 mins',
    capacity: 'Up to 8 passengers',
    features: ['Air conditioned', 'WiFi', 'Refreshments', 'Extra luggage space'],
    icon: Caravan,
  },
]

const whyItems = [
  { icon: Clock, title: 'On-Time Guarantee', desc: 'We track your flight and adjust pickup times accordingly' },
  { icon: Users, title: 'Professional Drivers', desc: 'Licensed, insured, and courteous drivers' },
  { icon: DollarSign, title: 'Best Rates', desc: 'Competitive pricing with no hidden fees' },
]

function handleSearch() {
  alert('Search functionality would show available shuttles for your criteria.')
}
</script>