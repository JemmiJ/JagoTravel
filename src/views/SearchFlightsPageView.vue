<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-12">
      <div class="max-w-2xl mx-auto">
        <BaseCard>
          <h2 class="text-2xl font-bold text-center mb-6">Search Flights</h2>
          <p class="text-center text-gray-600 mb-8">Find the perfect flight for your journey</p>
          <form @submit.prevent="handleSearch" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <BaseInput v-model="origin" label="Origin" placeholder="Kingston (KIN)" required />
              <BaseInput v-model="destination" label="Destination" placeholder="New York (JFK)" required />
              <BaseInput v-model="departureDate" label="Departure Date" type="date" required />
              <BaseSelect
                v-model="passengers"
                label="Passengers"
                :options="passengerOptions"
                placeholder="Select"
              />
            </div>
            <div class="space-y-3">
              <BaseButton type="submit" size="lg" block>
                <Search class="w-5 h-5 mr-2" /> Search Flights
              </BaseButton>
              <BaseButton variant="outline" size="lg" block @click="$router.back()">
                Back
              </BaseButton>
            </div>
          </form>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const origin = ref('')
const destination = ref('')
const departureDate = ref('')
const passengers = ref(1)

const passengerOptions = [1,2,3,4,5,6,7,8,9,10].map(n => ({ value: n, label: `${n} ${n === 1 ? 'Passenger' : 'Passengers'}` }))

function handleSearch() {
  router.push({
    path: '/flight-search/results',
    query: {
      origin: origin.value,
      destination: destination.value,
      departureDate: departureDate.value,
      passengers: passengers.value,
    },
  })
}
</script>