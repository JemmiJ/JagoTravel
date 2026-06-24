<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div class="lg:col-span-1">
          <SidebarNav :items="sidebarItems" />
        </div>
        <div class="lg:col-span-3">
          <h1 class="text-3xl font-bold text-gray-900 mb-8">My Bookings</h1>

          <div v-if="loading" class="flex justify-center py-12">
            <Loader2 class="w-12 h-12 text-primary-500 animate-spin" />
          </div>

          <div v-else-if="bookings.length === 0" class="text-center py-12 text-gray-600">
            You have no bookings yet.
          </div>

          <div v-else class="space-y-6">
            <BaseCard v-for="booking in bookings" :key="booking.id">
              <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Plane class="w-6 h-6 text-primary-500" />
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