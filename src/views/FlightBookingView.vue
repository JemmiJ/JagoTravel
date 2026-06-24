<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Complete Your Booking</h1>

      <div v-if="loading" class="flex justify-center py-12">
        <Loader2 class="w-12 h-12 text-primary-500 animate-spin" />
      </div>

      <div v-else-if="flightDetails" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
          <BaseCard>
            <form @submit.prevent="handleSubmit" class="space-y-8">
              <div>
                <h2 class="text-xl font-semibold text-gray-900 mb-4">Passenger Details</h2>
                <div class="space-y-4">
                  <BaseInput v-model="userDetails.name" label="Full Name" disabled />
                  <BaseInput v-model="userDetails.email" label="Email Address" disabled />
                  <BaseInput v-model="userDetails.phone" label="Phone Number" disabled />
                </div>
              </div>

              <div>
                <h2 class="text-xl font-semibold text-gray-900 mb-4">Preferences</h2>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Seat Preference</label>
                    <div class="space-y-2">
                      <label v-for="opt in seatOptions" :key="opt.value" class="flex items-center gap-2 cursor-pointer">
                        <input type="radio" v-model="form.seatPreference" :value="opt.value" class="w-4 h-4 text-primary-500 focus:ring-primary-500" />
                        <span>{{ opt.label }}</span>
                      </label>
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Special Requests</label>
                    <div class="space-y-2">
                      <label v-for="req in specialRequests" :key="req.key" class="flex items-center gap-2 cursor-pointer">
                        <input type="checkbox" v-model="req.checked" class="w-4 h-4 text-primary-500 rounded focus:ring-primary-500" />
                        <span>{{ req.label }}</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div class="bg-blue-50 rounded-lg p-4">
                <label class="flex items-start gap-3 cursor-pointer">
                  <input type="checkbox" v-model="acceptTerms" class="w-4 h-4 text-primary-500 rounded focus:ring-primary-500 mt-0.5" />
                  <span class="text-sm text-gray-700">I accept the Terms & Conditions and Privacy Policy</span>
                </label>
              </div>

              <BaseButton type="submit" size="lg" block :disabled="!acceptTerms">
                Proceed to Payment
              </BaseButton>
            </form>
          </BaseCard>
        </div>

        <div class="lg:col-span-1">
          <BaseCard class="sticky top-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Flight Summary</h2>
            <div class="flex items-center gap-3 mb-6 pb-6 border-b border-gray-200">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <Plane class="w-6 h-6 text-primary-500" />
              </div>
              <div>
                <p class="font-semibold text-gray-900">{{ flightDetails.airline }}</p>
                <p class="text-sm text-gray-600">Flight {{ flightDetails.flight_number }}</p>
              </div>
            </div>
            <div class="space-y-3 mb-6 pb-6 border-b border-gray-200">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Route</span>
                <span class="font-medium text-gray-900">{{ query.origin }} → {{ query.destination }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Date</span>
                <span class="font-medium text-gray-900">{{ formatDate(flightDetails.departure) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Departure</span>
                <span class="font-medium text-gray-900">{{ formatTime(flightDetails.departure) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Arrival</span>
                <span class="font-medium text-gray-900">{{ formatTime(flightDetails.arrival) }}</span>
              </div>
            </div>
            <div class="bg-primary-50 rounded-lg p-4">
              <div class="flex justify-between items-center">
                <span class="font-semibold text-gray-900">TOTAL</span>
                <span class="text-2xl font-bold text-primary-500">
                  ${{ flightDetails.total ? flightDetails.total.toLocaleString() : flightDetails.price.toLocaleString() }} JMD
                </span>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Plane, Loader2 } from 'lucide-vue-next'
import axios from 'axios'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const route = useRoute()
const flightId = route.query.flight
const query = computed(() => route.query)

const loading = ref(false)
const flightDetails = ref(null)

const userDetails = reactive({
  name: '',
  email: '',
  phone: '',
})

const form = reactive({
  seatPreference: 'no-preference',
})

const acceptTerms = ref(false)

const seatOptions = [
  { value: 'window', label: 'Window' },
  { value: 'aisle', label: 'Aisle' },
  { value: 'no-preference', label: 'No Preference' },
]

const specialRequests = reactive([
  { key: 'specialMeal', label: 'Special Meal', checked: false },
  { key: 'wheelchair', label: 'Wheelchair Assistance', checked: false },
  { key: 'infant', label: 'Traveling with Infant', checked: false },
])

const fetchFlightDetails = async () => {
  if (!flightId) return
  loading.value = true
  try {
    const resp = await axios.get(`/api/flights/${flightId}`)
    flightDetails.value = resp.data
  } catch (error) {
    console.error('Error fetching flight details:', error)
    alert('Could not load flight details. Please try again.')
  } finally {
    loading.value = false
  }
}

const fetchUserDetails = () => {
  const name = localStorage.getItem('name') || 'User'
  userDetails.name = name
}

onMounted(() => {
  fetchFlightDetails()
  fetchUserDetails()
})

const formatTime = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString([], { year: 'numeric', month: 'short', day: 'numeric' })
}

const handleSubmit = async () => {
  if (!acceptTerms.value) {
    alert('You must accept the Terms & Conditions.')
    return
  }
  if (!flightDetails.value) {
    alert('Flight details not loaded. Please try again.')
    return
  }

  const totalPrice = flightDetails.value.total || flightDetails.value.price

  const payload = {
    flight_id: flightId,
    total_price: totalPrice,
    seat_preference: form.seatPreference,
    special_requests: specialRequests.filter(r => r.checked).map(r => r.key),
  }

  try {
    const resp = await axios.post('/api/bookings', payload, { withCredentials: true })
    const bookingId = resp.data.booking_id
    router.push(`/book-flight/payment?booking=${bookingId}`)
  } catch (error) {
    console.error('Booking creation failed:', error)
    alert(error.response?.data?.error || 'Something went wrong. Please try again.')
  }
}
</script>