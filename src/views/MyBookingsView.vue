<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-16 md:py-20">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div class="lg:col-span-1">
          <SidebarNav :items="sidebarItems" />
        </div>
        <div class="lg:col-span-3 animate-fade-in-up">
          <h1 class="text-3xl font-display font-bold text-gray-900 mb-8">My Bookings</h1>

          <div v-if="loading" class="flex flex-col items-center justify-center gap-3 py-12">
            <Loader2 class="w-12 h-12 text-gold-400 animate-spin" />
            <p class="text-sm text-gray-500">Loading your bookings...</p>
          </div>

          <div v-else-if="bookings.length === 0" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-12 text-center">
            <div class="w-16 h-16 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <Plane class="w-8 h-8 text-primary-500" />
            </div>
            <h3 class="text-lg font-display font-bold text-gray-900 mb-1">No bookings yet</h3>
            <p class="text-gray-600 mb-6 font-sans">Your upcoming flights will show up here once you book one.</p>
            <router-link to="/flight-search" class="btn btn-primary btn-md">Search Flights</router-link>
          </div>

          <div v-else class="space-y-6">
            <BaseCard
              v-for="(booking, idx) in bookings"
              :key="booking.id"
              class="hover:shadow-lg transition-shadow duration-200 animate-fade-in-up"
              :style="{ animationDelay: `${idx * 75}ms` }"
            >
              <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-primary-800 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Plane class="w-6 h-6 text-gold-400" />
                  </div>
                  <div>
                    <div class="flex items-center gap-3 flex-wrap">
                      <h3 class="text-xl font-semibold text-gray-900">{{ booking.flight_data?.route || 'N/A' }}</h3>
                      <span class="px-3 py-1 rounded-full text-xs font-semibold" :class="statusClass(booking.status)">
                        {{ booking.status }}
                      </span>
                    </div>
                    <p class="text-gray-600 text-sm">{{ booking.created_at ? formatDate(booking.created_at) : 'N/A' }}</p>
                    <p class="text-sm text-gray-500">Booking ref: <span class="font-medium">{{ booking.booking_reference }}</span></p>
                    <p class="text-sm text-gray-500">{{ booking.passenger_name }}</p>
                  </div>
                </div>
                <div class="flex flex-wrap gap-3">
                  <BaseButton variant="primary" size="sm">View Details</BaseButton>
                  <BaseButton v-if="booking.status === 'pending'" variant="warning" size="sm">Complete Payment</BaseButton>
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { Plane, Loader2 } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SidebarNav from '@/components/layout/sideNavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { getToken } from '@/utils/auth'

const router = useRouter()
const token = getToken()
if (!token) router.push('/login')

const loading = ref(false)
const bookings = ref([])

const sidebarItems = [
  { label: 'My Bookings', path: '/profile/my-bookings', icon: 'Calendar' },
  { label: 'Profile', path: '/profile', icon: 'User' },
  { label: 'Loyalty Points', path: '/profile/loyalty-points', icon: 'Award' },
  { label: 'Settings', path: '/profile/settings', icon: 'Settings' },
]

const fetchBookings = async () => {
  loading.value = true
  try {
    const resp = await axios.get('/api/bookings', { withCredentials: true })
    bookings.value = resp.data
  } catch (error) {
    console.error('Error fetching bookings:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchBookings)

const statusClass = (status) => {
  const map = {
    paid: 'bg-green-100 text-green-700',
    pending: 'bg-amber-100 text-amber-700',
    cancelled: 'bg-gray-100 text-gray-700',
  }
  return map[status] || 'bg-gray-100 text-gray-700'
}

const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString([], { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>