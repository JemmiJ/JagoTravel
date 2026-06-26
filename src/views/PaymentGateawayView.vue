<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-16 md:py-20 max-w-lg mx-auto">
      <BaseCard>
        <div class="text-center mb-8">
          <h1 class="text-3xl font-display font-bold text-gray-900">Complete Payment</h1>
          <p class="text-gray-500 mt-2 text-sm">Secure mock payment for demo purposes</p>
        </div>

        <div v-if="loading" class="flex flex-col items-center gap-3 py-8">
          <Loader2 class="w-10 h-10 text-gold-400 animate-spin" />
          <p class="text-sm text-gray-500">Loading booking details...</p>
        </div>

        <div v-else>
          <!-- Amount display -->
          <div class="bg-primary-50 rounded-xl p-6 mb-6 text-center">
            <p class="text-sm text-gray-500 mb-1">Total Amount</p>
            <p class="text-4xl font-bold text-gold-600">
              ${{ amount.toLocaleString() }} JMD
            </p>
          </div>

          <!-- Price breakdown -->
          <div class="space-y-2 mb-6 pb-6 border-b border-gray-100">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Base Fare</span>
              <span class="text-gray-900">${{ baseFare.toLocaleString() }} JMD</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Taxes & Fees (15%)</span>
              <span class="text-gray-900">${{ taxes.toLocaleString() }} JMD</span>
            </div>
            <div class="flex justify-between text-sm font-semibold pt-2 border-t border-gray-100">
              <span class="text-gray-900">Total</span>
              <span class="text-gold-600">${{ amount.toLocaleString() }} JMD</span>
            </div>
          </div>

          <!-- Pay button -->
          <BaseButton
            size="lg"
            block
            :disabled="processing"
            @click="handlePayment"
          >
            <span v-if="processing" class="flex items-center justify-center gap-2">
              <Loader2 class="w-4 h-4 animate-spin" />
              Processing...
            </span>
            <span v-else>Pay ${{ amount.toLocaleString() }} JMD</span>
          </BaseButton>

          <p class="text-center text-xs text-gray-400 mt-4">
            You'll be redirected to your booking confirmation after payment
          </p>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Loader2 } from 'lucide-vue-next'
import axios from 'axios'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()

const bookingId = route.query.booking
const loading = ref(false)
const processing = ref(false)

// Amount passed directly from booking form in URL
const amount = ref(parseInt(route.query.amount) || 0)
const baseFare = ref(Math.round(amount.value / 1.15))
const taxes = ref(amount.value - baseFare.value)

const handlePayment = async () => {
  if (!bookingId) return
  processing.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.post('/api/mock-payment', { booking_id: bookingId }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    router.push(`/book-flight/confirmation?booking=${bookingId}`)
  } catch (e) {
    alert(e.response?.data?.error || 'Payment failed. Please try again.')
    processing.value = false
  }
}
</script>