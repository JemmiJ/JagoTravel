<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />

    <section class="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16">
      <div class="container text-center">
        <Tag class="w-16 h-16 mx-auto mb-4" />
        <h1 class="text-4xl font-bold mb-4">Packages & Deals</h1>
        <p class="text-xl text-primary-100">Exclusive travel packages and special offers for you</p>
      </div>
    </section>

    <div class="container py-12 space-y-12">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 mb-8">Featured Packages</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <BaseCard v-for="pkg in packages" :key="pkg.title" class="overflow-hidden p-0 hover:shadow-xl transition-shadow">
            <div class="bg-gradient-to-br from-primary-500 to-primary-700 text-white p-8 text-center relative">
              <span v-if="pkg.badge" class="absolute top-4 right-4 px-3 py-1 bg-white text-primary-600 text-xs font-semibold rounded-full">
                {{ pkg.badge }}
              </span>
              <div class="text-6xl mb-4">{{ pkg.image }}</div>
              <h3 class="text-2xl font-bold">{{ pkg.title }}</h3>
              <p class="text-primary-100">{{ pkg.destination }}</p>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-gray-600">{{ pkg.duration }}</span>
                <span class="px-3 py-1 bg-green-100 text-green-700 text-sm font-semibold rounded-full">{{ pkg.discount }}</span>
              </div>
              <div class="mb-6">
                <p class="text-sm text-gray-600 mb-2">Package Includes:</p>
                <ul class="space-y-2">
                  <li v-for="(item, i) in pkg.includes" :key="i" class="flex items-center gap-2 text-sm text-gray-700">
                    <Star class="w-4 h-4 text-primary-500 fill-primary-500" />
                    {{ item }}
                  </li>
                </ul>
              </div>
              <div class="flex items-end justify-between mb-4">
                <div>
                  <p class="text-sm text-gray-500 line-through">${{ pkg.originalPrice.toLocaleString() }} JMD</p>
                  <p class="text-3xl font-bold text-primary-600">${{ pkg.price.toLocaleString() }} JMD</p>
                  <p class="text-sm text-green-600 font-medium">Save ${{ (pkg.originalPrice - pkg.price).toLocaleString() }}</p>
                </div>
              </div>
              <BaseButton size="md" block>Book This Package</BaseButton>
            </div>
          </BaseCard>
        </div>
      </div>

      <div>
        <h2 class="text-3xl font-bold text-gray-900 mb-8">Limited Time Flight Deals</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <BaseCard v-for="deal in deals" :key="deal.route">
            <div class="flex items-center gap-2 mb-4">
              <Plane class="w-5 h-5 text-primary-500" />
              <h3 class="text-lg font-semibold text-gray-900">{{ deal.route }}</h3>
            </div>
            <div class="mb-4">
              <p class="text-sm text-gray-500 line-through">${{ deal.originalPrice.toLocaleString() }} JMD</p>
              <p class="text-3xl font-bold text-primary-600">${{ deal.price.toLocaleString() }}</p>
              <p class="text-sm text-green-600 font-medium">Save ${{ deal.savings.toLocaleString() }}</p>
            </div>
            <p class="text-sm text-gray-600 mb-4">Valid until {{ deal.validUntil }}</p>
            <BaseButton variant="primary" size="md" block>View Flights</BaseButton>
          </BaseCard>
        </div>
      </div>

      <div class="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl shadow-lg p-8 text-center text-white">
        <h2 class="text-2xl font-bold mb-3">Subscribe for Exclusive Deals</h2>
        <p class="text-primary-100 mb-6">Get notified about special offers and new packages</p>
        <div class="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
          <input type="email" placeholder="Enter your email" class="flex-1 px-4 py-3 rounded-lg text-gray-900 focus:ring-2 focus:ring-white focus:outline-none" />
          <BaseButton variant="ghost" class="bg-white text-primary-600 hover:bg-gray-100">Subscribe</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Plane, Tag, Star } from 'lucide-vue-next'

const packages = [
  {
    title: 'Miami Beach Getaway',
    destination: 'Miami, Florida',
    duration: '5 Days, 4 Nights',
    price: 85000,
    originalPrice: 105000,
    discount: '20% OFF',
    includes: ['Round-trip flights', '4-star hotel', 'Airport transfers', 'Daily breakfast'],
    image: '🏖️',
    badge: 'Popular',
  },
  {
    title: 'New York City Explorer',
    destination: 'New York, USA',
    duration: '7 Days, 6 Nights',
    price: 120000,
    originalPrice: 150000,
    discount: '20% OFF',
    includes: ['Round-trip flights', 'Hotel in Manhattan', 'City tour pass', 'Airport shuttle'],
    image: '🗽',
    badge: 'Best Value',
  },
  {
    title: 'London Heritage Tour',
    destination: 'London, UK',
    duration: '10 Days, 9 Nights',
    price: 195000,
    originalPrice: 240000,
    discount: '19% OFF',
    includes: ['Round-trip flights', 'Boutique hotel', 'Museum passes', 'Oyster card'],
    image: '🇬🇧',
    badge: null,
  },
  {
    title: 'Caribbean Island Hopping',
    destination: 'Multiple Caribbean Islands',
    duration: '14 Days, 13 Nights',
    price: 165000,
    originalPrice: 200000,
    discount: '18% OFF',
    includes: ['Inter-island flights', 'Resort stays', 'Island tours', 'Water activities'],
    image: '🏝️',
    badge: 'Adventure',
  },
]

const deals = [
  {
    route: 'Kingston → Miami',
    price: 28000,
    originalPrice: 35000,
    savings: 7000,
    validUntil: 'June 30, 2026',
  },
  {
    route: 'Kingston → Toronto',
    price: 42000,
    originalPrice: 52000,
    savings: 10000,
    validUntil: 'July 15, 2026',
  },
  {
    route: 'Kingston → London',
    price: 65000,
    originalPrice: 80000,
    savings: 15000,
    validUntil: 'August 1, 2026',
  },
]
</script>