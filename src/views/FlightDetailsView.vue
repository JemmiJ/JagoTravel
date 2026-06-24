<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-8">
      <router-link to="/flight-search/results" class="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 mb-6">
        <ArrowLeft class="w-4 h-4" /> Back to Results
      </router-link>

      <div v-if="loading" class="flex justify-center py-20">
        <Loader2 class="w-12 h-12 text-primary-500 animate-spin" />
      </div>

      <div v-else-if="flight" class="max-w-4xl mx-auto">
        <BaseCard class="overflow-hidden">
          <!-- Header -->
          <div class="bg-primary-500 text-white p-6 -m-6 mb-6">
            <div class="flex items-center gap-3">
              <Plane class="w-8 h-8" />
              <div>
                <h1 class="text-2xl font-bold">{{ flight.airline }}</h1>
                <p class="text-primary-100">Flight {{ flight.flight_number }}</p>
              </div>
            </div>
          </div>

          <!-- Itinerary -->
          <div class="space-y-8">
            <div class="flex items-center justify-between">
              <div class="text-center">
                <p class="text-sm text-gray-600">Departure</p>
                <p class="text-3xl font-bold text-primary-500">{{ formatTime(flight.departure) }}</p>
                <p class="text-lg font-semibold text-gray-900 mt-2">{{ query.origin || 'Origin' }}</p>
              </div>
              <div class="flex flex-col items-center px-8">
                <Plane class="w-6 h-6 text-gray-400 mb-2" />
                <div class="w-64 h-0.5 bg-gray-300 relative">
                  <div class="absolute left-0 w-2 h-2 bg-primary-500 rounded-full -top-0.5"></div>
                  <div class="absolute right-0 w-2 h-2 bg-primary-500 rounded-full -top-0.5"></div>
                </div>
                <p class="text-sm text-gray-600 mt-2">Duration: {{ flight.duration }}</p>
              </div>
              <div class="text-center">
                <p class="text-sm text-gray-600">Arrival</p>
                <p class="text-3xl font-bold text-primary-500">{{ formatTime(flight.arrival) }}</p>
                <p class="text-lg font-semibold text-gray-900 mt-2">{{ query.destination || 'Destination' }}</p>
              </div>
            </div>

            <!-- Price breakdown -->
            <div class="bg-primary-50 rounded-xl p-6">
              <h3 class="font-semibold text-gray-900 mb-4">Price Breakdown</h3>
              <div class="space-y-2">
                <div class="flex justify-between text-gray-700">
                  <span>Base Fare</span>
                  <span>${{ flight.price.toLocaleString() }} JMD</span>
                </div>
                <div class="flex justify-between text-gray-700">
                  <span>Taxes & Fees</span>
                  <span>${{ Math.round(flight.price * 0.15).toLocaleString() }} JMD</span>
                </div>
                <div class="flex justify-between text-gray-700">
                  <span>Baggage Fee</span>
                  <span>$3,500 JMD</span>
                </div>
                <div class="border-t border-gray-300 pt-3 mt-3">
                  <div class="flex justify-between items-center">
                    <span class="font-semibold text-gray-900">TOTAL</span>
                    <span class="text-3xl font-bold text-primary-500">
                      ${{ (flight.price + Math.round(flight.price * 0.15) + 3500).toLocaleString() }} JMD
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Baggage -->
            <div class="bg-blue-50 rounded-xl p-6 flex items-start gap-3">
              <Briefcase class="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h3 class="font-semibold text-gray-900">Baggage Allowance</h3>
                <p class="text-gray-700">1 checked bag (23kg) • 1 carry-on (10kg)</p>
              </div>
            </div>

            <BaseButton size="lg" block @click="bookFlight">Book This Flight</BaseButton>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plane, ArrowLeft, Briefcase, Loader2 } from 'lucide-vue-next'
import axios from 'axios'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { getToken } from '@/utils/auth'

const route = useRoute()
const router = useRouter()
const flightId = route.params.flightId
const query = computed(() => route.query)
const flight = ref(null)
const loading = ref(false)
const isAuthenticated = computed(() => !!getToken())

const formatTime = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const fetchDetails = async () => {
  loading.value = true
  try {
    const resp = await axios.get(`/api/flights/${flightId}`)
    flight.value = resp.data
  } catch (error) {
    console.error('Error fetching flight details:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchDetails)

const bookFlight = () => {
  if (!isAuthenticated.value) {
    router.push('/login')
  } else {
    router.push(`/book-flight?flight=${flightId}`)
  }
}
</script>