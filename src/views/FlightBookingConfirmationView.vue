<template>
  <div class="min-h-screen bg-gradient-to-b from-primary-50/30 to-white">
    <NavigationBar />
    <div class="container py-16 max-w-3xl">
      <div v-if="loading" class="flex flex-col items-center justify-center gap-3 py-12">
        <Loader2 class="w-12 h-12 text-gold-400 animate-spin" />
        <p class="text-sm text-gray-500">Loading your booking...</p>
      </div>

      <div v-else-if="bookingData" class="text-center mb-12 animate-fade-in-up">
        <div class="w-24 h-24 bg-success rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle class="w-16 h-16 text-white" />
        </div>
        <h1 class="text-4xl font-display font-bold text-gray-900 mb-4">Your Flight is Booked!</h1>
        <p class="text-xl text-gray-600">Get ready for your journey</p>
      </div>

      <div v-if="bookingData" class="space-y-6 animate-fade-in-up">
        <BaseCard>
          <div class="text-center mb-6">
            <p class="text-sm text-gray-600">Booking Reference</p>
            <div class="flex items-center justify-center gap-2">
              <p class="text-3xl font-bold text-gold-600">{{ bookingData.booking_reference }}</p>
              <button @click="copyRef" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <Copy class="w-5 h-5 text-gray-600" />
              </button>
            </div>
          </div>

          <div class="bg-primary-50 rounded-xl p-6 mb-6">
            <h2 class="font-display font-bold text-gray-900 mb-4">Flight Summary</h2>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600">Route</span>
                <span class="font-medium text-gray-900">{{ bookingData.flight_data?.route || 'N/A' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Date</span>
                <span class="font-medium text-gray-900">{{ formatDate(bookingData.flight_data?.departure) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Passenger</span>
                <span class="font-medium text-gray-900">{{ bookingData.passenger_name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Email</span>
                <span class="font-medium text-gray-900">{{ bookingData.email }}</span>
              </div>
            </div>
          </div>

          <div class="bg-green-50 rounded-xl p-6 mb-6">
            <div class="flex justify-between items-center">
              <span class="text-gray-600">Amount Paid</span>
              <span class="text-2xl font-bold text-success">${{ bookingData.total_price.toLocaleString() }} JMD</span>
            </div>
          </div>

          <div class="mb-6">
            <h2 class="font-display font-bold text-gray-900 mb-4">Next Steps</h2>
            <div v-for="(step, idx) in nextSteps" :key="idx" class="flex items-start gap-3 mb-2">
              <CheckCircle v-if="idx === 0" class="w-5 h-5 text-success mt-0.5 flex-shrink-0" />
              <div v-else class="w-5 h-5 border-2 border-gray-300 rounded-full mt-0.5 flex-shrink-0"></div>
              <p class="text-gray-700">{{ step }}</p>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <router-link to="/profile/my-bookings" class="flex-1">
              <BaseButton variant="primary" size="md" block>View My Bookings</BaseButton>
            </router-link>
            <BaseButton variant="outline" size="md" block>
              <Download class="w-5 h-5 mr-2" /> Download Receipt
            </BaseButton>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { CheckCircle, Copy, Download, Loader2 } from 'lucide-vue-next'
import axios from 'axios'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const bookingId = route.query.booking
const loading = ref(false)
const bookingData = ref(null)

const nextSteps = [
  'Confirmation email sent',
  'Check-in opens 24 hours before departure',
  'Arrive at airport 2 hours early',
]

const copyRef = () => {
  if (bookingData.value?.booking_reference) {
    navigator.clipboard.writeText(bookingData.value.booking_reference)
  }
}

const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString([], { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(async () => {
  if (!bookingId) {
    alert('No booking reference found.')
    return
  }
  loading.value = true
  try {
    const resp = await axios.get(`/api/bookings/${bookingId}`, { withCredentials: true })
    bookingData.value = resp.data
  } catch (error) {
    console.error('Failed to load booking', error)
    alert('Could not load booking details. Please try again.')
  } finally {
    loading.value = false
  }
})
</script>