<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-16 md:py-20">
      <router-link to="/flight-search" class="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 hover:gap-3 transition-all mb-6">
        <ArrowLeft class="w-4 h-4" /> Back to Search
      </router-link>

      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-8 animate-fade-in-up">
        <div>
          <h1 class="text-3xl md:text-4xl font-display font-bold text-gray-900">Available Flights</h1>
          <p class="text-gray-600">
            {{ query.origin }} → {{ query.destination }} • {{ query.departureDate }} • {{ query.passengers }} Passenger{{ query.passengers > 1 ? 's' : '' }}
          </p>
        </div>
        <div class="mt-4 md:mt-0">
          <BaseSelect v-model="sortBy" :options="sortOptions" label="Sort by" class="w-40" />
        </div>
      </div>

      <div v-if="loading" class="flex flex-col items-center justify-center gap-3 py-12">
        <Loader2 class="w-12 h-12 text-gold-400 animate-spin" />
        <p class="text-sm text-gray-500">Loading flights...</p>
      </div>
      <div v-else-if="flights.length === 0" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-12 text-center">
        <div class="w-16 h-16 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <SearchX class="w-8 h-8 text-primary-500" />
        </div>
        <h3 class="text-lg font-display font-bold text-gray-900 mb-1">No flights found</h3>
        <p class="text-gray-600 mb-6 font-sans">Try a different route or date to see available flights.</p>
        <router-link to="/flight-search" class="btn btn-primary btn-md">New Search</router-link>
      </div>
      <div v-else class="space-y-4">
        <BaseCard
          v-for="(flight, idx) in sortedFlights"
          :key="flight.id"
          class="cursor-pointer animate-fade-in-up"
          :style="{ animationDelay: `${idx * 75}ms` }"
          @click="goToDetails(flight.id)"
        >
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex items-center gap-4 flex-1">
              <div class="w-14 h-14 bg-primary-800 rounded-lg flex items-center justify-center flex-shrink-0">
                <Plane class="w-7 h-7 text-gold-400" />
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="font-semibold text-gray-900">{{ flight.airline }}</h3>
                  <span v-if="flight.badge" class="px-2 py-0.5 text-xs font-semibold bg-gold-100 text-gold-700 rounded-full">
                    {{ flight.badge }}
                  </span>
                </div>
                <p class="text-sm text-gray-600">{{ flight.flight_number }}</p>
              </div>
            </div>

            <div class="flex items-center gap-6 flex-1 justify-center">
              <div class="text-center">
                <p class="text-xl font-bold text-gray-900">{{ formatTime(flight.departure) }}</p>
                <p class="text-xs text-gray-600">{{ query.origin }}</p>
              </div>
              <div class="flex flex-col items-center">
                <div class="w-16 h-0.5 bg-gray-300 relative">
                  <div class="absolute left-0 w-2 h-2 bg-primary-500 rounded-full -top-0.5"></div>
                  <div class="absolute right-0 w-2 h-2 bg-primary-500 rounded-full -top-0.5"></div>
                </div>
                <p class="text-xs text-gray-600 mt-1">{{ flight.duration }}</p>
              </div>
              <div class="text-center">
                <p class="text-xl font-bold text-gray-900">{{ formatTime(flight.arrival) }}</p>
                <p class="text-xs text-gray-600">{{ query.destination }}</p>
              </div>
            </div>

            <div class="text-right">
              <p class="text-2xl font-bold text-gold-600">${{ flight.price.toLocaleString() }}</p>
              <p class="text-xs text-gray-500 mb-2">JMD</p>
              <BaseButton size="sm" @click.stop="bookNow(flight.id)">Book Now</BaseButton>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plane, ArrowLeft, Loader2, SearchX } from 'lucide-vue-next'
import axios from 'axios'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { getToken } from '@/utils/auth'

const route = useRoute()
const router = useRouter()
const query = computed(() => route.query)
const flights = ref([])
const loading = ref(false)
const sortBy = ref('price')
const isAuthenticated = computed(() => !!getToken())

const sortOptions = [
  { value: 'price', label: 'Lowest Price' },
  { value: 'duration', label: 'Shortest Duration' },
  { value: 'departure', label: 'Earliest Departure' },
]

const sortedFlights = computed(() => {
  const list = [...flights.value]
  if (sortBy.value === 'price') return list.sort((a,b) => a.price - b.price)
  if (sortBy.value === 'duration') return list.sort((a,b) => a.duration.localeCompare(b.duration))
  if (sortBy.value === 'departure') return list.sort((a,b) => a.departure.localeCompare(b.departure))
  return list
})

const fetchFlights = async () => {
  loading.value = true
  try {
    const resp = await axios.get('/api/flights', {
      params: {
        origin: query.value.origin,
        destination: query.value.destination,
        date: query.value.departureDate,
      },
    })
    flights.value = resp.data
  } catch (error) {
    console.error('Error fetching flights:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchFlights)

const formatTime = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const goToDetails = (id) => {
  router.push(`/flight-search/results/flight/${id}?origin=${query.value.origin}&destination=${query.value.destination}`)
}

const bookNow = (id) => {
  if (!isAuthenticated.value) {
    router.push('/login')
  } else {
    router.push(`/book-flight?flight=${id}&origin=${query.value.origin}&destination=${query.value.destination}`)
  }
}
</script>