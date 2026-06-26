<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-16 md:py-20">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div class="lg:col-span-1">
          <SidebarNav :items="sidebarItems" />
        </div>
        <div class="lg:col-span-3 animate-fade-in-up">
          <h1 class="text-3xl font-display font-bold text-gray-900 mb-8">Loyalty Points</h1>

          <!-- Summary -->
          <div class="bg-gradient-to-br from-gold-500 to-gold-600 rounded-2xl shadow-lg p-8 text-primary-900 mb-8">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-primary-900/70 mb-2">Your Total Points</p>
                <p class="text-5xl font-bold">1,750</p>
                <div class="flex items-center gap-2 mt-4">
                  <TrendingUp class="w-5 h-5" />
                  <span class="text-primary-900/70">+450 points this month</span>
                </div>
              </div>
              <Star class="w-24 h-24 text-primary-900/20" />
            </div>
          </div>

          <!-- Tier & Earnings -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <BaseCard>
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-primary-800 rounded-full flex items-center justify-center">
                  <Award class="w-6 h-6 text-gold-400" />
                </div>
                <div>
                  <p class="text-sm text-gray-600">Member Tier</p>
                  <p class="text-xl font-semibold text-gray-900">Silver</p>
                </div>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2 mt-4">
                <div class="bg-gold-500 h-2 rounded-full" style="width: 70%"></div>
              </div>
              <p class="text-sm text-gray-600 mt-2">750 points to Gold tier</p>
            </BaseCard>
            <BaseCard>
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <Gift class="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-600">Points Earned</p>
                  <p class="text-2xl font-bold text-gold-600">2,250</p>
                </div>
              </div>
              <p class="text-sm text-gray-600 mt-4">Lifetime earnings</p>
            </BaseCard>
          </div>

          <!-- Rewards -->
          <BaseCard class="mb-8">
            <h2 class="text-xl font-display font-semibold text-gray-900 mb-6">Available Rewards</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="reward in rewards" :key="reward.title" class="border border-gray-200 rounded-xl p-6 hover:border-gold-400 hover:shadow-md transition-all duration-200">
                <div class="flex items-start justify-between mb-3">
                  <h3 class="font-semibold text-gray-900">{{ reward.title }}</h3>
                  <span class="px-3 py-1 bg-amber-100 text-amber-700 text-sm font-semibold rounded-full">{{ reward.points }} pts</span>
                </div>
                <p class="text-sm text-gray-600 mb-4">{{ reward.description }}</p>
                <BaseButton
                  :disabled="1750 < reward.points"
                  size="sm"
                  block
                >
                  {{ 1750 >= reward.points ? 'Redeem' : 'Not enough points' }}
                </BaseButton>
              </div>
            </div>
          </BaseCard>

          <!-- History -->
          <BaseCard>
            <h2 class="text-xl font-display font-bold text-gray-900 mb-6">Points History</h2>
            <div class="space-y-4">
              <div v-for="item in pointsHistory" :key="item.date" class="flex items-center justify-between py-4 border-b border-gray-200 last:border-b-0">
                <div>
                  <p class="font-medium text-gray-900">{{ item.description }}</p>
                  <p class="text-sm text-gray-600 font-sans">{{ item.date }}</p>
                </div>
                <span class="font-bold text-lg" :class="item.type === 'earned' ? 'text-green-600' : 'text-red-600'">
                  {{ item.points }}
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
import { RouterLink, useRouter } from 'vue-router'
import { Calendar, User, Award, Settings, Star, Gift, TrendingUp } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SidebarNav from '@/components/layout/sideNavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { getToken } from '@/utils/auth'

const router = useRouter()
if (!getToken()) router.push('/login')

const sidebarItems = [
  { label: 'My Bookings', path: '/profile/my-bookings', icon: 'Calendar' },
  { label: 'Profile', path: '/profile', icon: 'User' },
  { label: 'Loyalty Points', path: '/profile/loyalty-points', icon: 'Award' },
  { label: 'Settings', path: '/profile/settings', icon: 'Settings' },
]

const rewards = [
  { title: '$20 Flight Discount', points: 1000, description: 'Save $20 on your next booking' },
  { title: '$50 Flight Discount', points: 2500, description: 'Save $50 on your next booking' },
  { title: 'Priority Boarding', points: 1500, description: 'Board the plane first' },
  { title: 'Free Seat Selection', points: 800, description: 'Choose your preferred seat for free' },
]

const pointsHistory = [
  { date: 'Apr 15, 2026', description: 'Flight Booking - KIN to JFK', points: '+450', type: 'earned' },
  { date: 'Mar 10, 2026', description: 'Flight Booking - JFK to KIN', points: '+380', type: 'earned' },
  { date: 'Feb 20, 2026', description: 'Redeemed for discount', points: '-500', type: 'redeemed' },
  { date: 'Jan 15, 2026', description: 'Flight Booking - KIN to MIA', points: '+420', type: 'earned' },
]
</script>