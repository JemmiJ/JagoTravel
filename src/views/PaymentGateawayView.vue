<template>
  <div class="min-h-screen bg-gradient-to-b from-primary-50/30 to-white flex items-center justify-center px-4">
    <div class="max-w-md w-full animate-fade-in-up">
      <BaseCard class="text-center p-8">
        <div class="w-20 h-20 bg-gold-500 rounded-full flex items-center justify-center mx-auto mb-6">
          <Plane class="w-10 h-10 text-primary-900" />
        </div>
        <h1 class="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">Complete Payment</h1>
        <p class="text-gray-600 mb-6">Secure payment via Stripe</p>

        <div v-if="!clientSecret" class="flex flex-col items-center justify-center gap-3 py-6">
          <Loader2 class="w-8 h-8 text-gold-400 animate-spin" />
          <p class="text-sm text-gray-500">Setting up secure payment...</p>
        </div>

        <div v-else id="payment-element" class="mb-6"></div>

        <p class="text-sm text-gray-500 mb-1 font-sans">Total Amount</p>
        <p class="text-gold-400 font-bold text-2xl mb-6">{{ totalAmount }}</p>

        <BaseButton
          @click="handlePay"
          :disabled="processing"
          size="lg"
          block
        >
          {{ processing ? 'Processing...' : `Pay $${totalAmount}` }}
        </BaseButton>
        <p class="text-sm text-gray-500 mt-4">You'll be redirected after payment</p>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plane, Loader2 } from 'lucide-vue-next'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const bookingId = route.query.booking
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)

const clientSecret = ref(null)
const processing = ref(false)
const totalAmount = ref('45,000 JMD')

onMounted(async () => {
  try {
    const resp = await axios.post('/api/create-payment-intent', { booking_id: bookingId })
    const secret = resp.data.client_secret
    clientSecret.value = secret

    const stripe = await stripePromise
    const elements = stripe.elements({ clientSecret: secret })
    const paymentElement = elements.create('payment')
    paymentElement.mount('#payment-element')
  } catch (error) {
    console.error('Payment initiation failed', error)
    alert('Could not initiate payment. Please try again.')
  }
})

const handlePay = async () => {
  processing.value = true
  const stripe = await stripePromise
  const { error } = await stripe.confirmPayment({
    elements: document.querySelector('#payment-element')._elements,
    redirect: 'if_required',
  })
  if (error) {
    alert(error.message)
    processing.value = false
  } else {
    router.push(`/book-flight/confirmation?booking=${bookingId}`)
  }
}
</script>