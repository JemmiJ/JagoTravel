<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />

    <section class="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16">
      <div class="container text-center">
        <Plane class="w-16 h-16 mx-auto mb-4" />
        <h1 class="text-4xl font-bold mb-4">Flight Information</h1>
        <p class="text-xl text-primary-100">Everything you need to know before you fly</p>
      </div>
    </section>

    <!--<div class="container py-12 space-y-12">
      <div class="max-w-2xl mx-auto">
        <div class="relative">
          <Search class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search for flight information..."
            class="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-md"
          />
        </div>
      </div>-->

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <BaseCard v-for="info in filteredInfo" :key="info.title">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <component :is="info.icon" class="w-6 h-6 text-primary-500" />
            </div>
            <h2 class="text-xl font-semibold text-gray-900">{{ info.title }}</h2>
          </div>
          <ul class="space-y-3">
            <li v-for="(item, idx) in info.content" :key="idx" class="flex items-start gap-2">
              <span class="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 flex-shrink-0"></span>
              <span class="text-gray-700">{{ item }}</span>
            </li>
          </ul>
        </BaseCard>
      </div>

      <BaseCard>
        <h2 class="text-2xl font-bold text-gray-900 mb-8">Frequently Asked Questions</h2>
        <div v-for="(faq, idx) in faqs" :key="idx" class="border-b border-gray-200 pb-6 last:border-b-0 last:pb-0">
          <h3 class="font-semibold text-gray-900 mb-2">{{ faq.question }}</h3>
          <p class="text-gray-700">{{ faq.answer }}</p>
        </div>
      </BaseCard>

      <div class="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl shadow-lg p-8 text-center text-white">
        <h2 class="text-2xl font-bold mb-3">Need More Help?</h2>
        <p class="text-primary-100 mb-6">Our customer support team is available 24/7 to assist you</p>
        <BaseButton variant="ghost" class="bg-white text-primary-600 hover:bg-gray-100">Contact Support</BaseButton>
      </div>
    </div>
  <!--</div>-->
</template>

<script setup>
import { ref, computed } from 'vue'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Search, Plane, Briefcase, CreditCard, FileText, Clock } from 'lucide-vue-next'

const searchQuery = ref('')

const flightInfo = [
  {
    title: 'Check-In Requirements',
    icon: Clock,
    content: [
      'Online check-in opens 24 hours before departure',
      'Airport check-in opens 3 hours before international flights',
      'Boarding gates close 30 minutes before departure',
      'Arrive at least 2 hours early for international flights',
    ],
  },
  {
    title: 'Baggage Allowance',
    icon: Briefcase,
    content: [
      'Carry-on: 1 bag up to 10kg (55cm x 40cm x 23cm)',
      'Checked baggage: 1 bag up to 23kg for economy class',
      'Additional baggage fees apply for extra or overweight items',
      'Liquids in carry-on must be in containers of 100ml or less',
    ],
  },
  {
    title: 'Travel Documents',
    icon: FileText,
    content: [
      'Valid passport required (at least 6 months validity)',
      'Visa requirements vary by destination country',
      'Print or have digital copy of boarding pass ready',
      'Bring government-issued photo ID for domestic flights',
    ],
  },
  {
    title: 'Payment Methods',
    icon: CreditCard,
    content: [
      'We accept Visa, Mastercard, and American Express',
      'Payments are processed securely through airline partners',
      'Full payment required at time of booking',
      'Refunds processed according to airline policies',
    ],
  },
]

const faqs = [
  {
    question: 'Can I change my flight after booking?',
    answer: 'Yes, flight changes are subject to airline policies and change fees. Contact customer support for assistance.',
  },
  {
    question: 'What items are prohibited in carry-on luggage?',
    answer: 'Sharp objects, liquids over 100ml, firearms, and explosives are prohibited. Check TSA guidelines for full list.',
  },
  {
    question: 'Do I need travel insurance?',
    answer: 'While not mandatory, we highly recommend travel insurance for trip cancellation, medical emergencies, and lost baggage.',
  },
  {
    question: 'What if my flight is delayed or cancelled?',
    answer: 'Airlines will rebook you on the next available flight. You may be entitled to compensation depending on the circumstances.',
  },
]

const filteredInfo = computed(() => {
  if (!searchQuery.value) return flightInfo
  const q = searchQuery.value.toLowerCase()
  return flightInfo.filter(info =>
    info.title.toLowerCase().includes(q) ||
    info.content.some(item => item.toLowerCase().includes(q))
  )
})
</script>