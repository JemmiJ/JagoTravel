<template>
  <nav class="bg-primary-700 shadow-md sticky top-0 z-50">
    <div class="container flex items-center justify-between h-16">
      <router-link to="/" class="text-2xl font-display text-white">
        JagoTravel
      </router-link>

      <div class="flex items-center gap-4">
        <div v-if="isAuthenticated" class="hidden sm:block text-white font-medium">
          {{ user.name || 'User' }}
        </div>
        <div v-else class="hidden sm:flex gap-3 text-white">
          <router-link to="/login" class="hover:underline">Login</router-link>
          <router-link to="/signup" class="hover:underline">Sign Up</router-link>
        </div>

        <button
          @click="toggleDropdown"
          class="text-white focus:outline-none focus:ring-2 focus:ring-white rounded p-1"
          aria-label="Toggle menu"
        >
          <MenuIcon class="w-6 h-6" />
        </button>
      </div>
    </div>

    <div
      v-show="showDropdown"
      class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl py-2 border border-gray-100 z-50 origin-top-right transition-all duration-200"
      :class="showDropdown ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
    >
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors"
        active-class="text-primary-600 font-semibold"
        @click="closeDropdown"
      >
        <span class="flex items-center gap-3">
          <component :is="item.icon" class="w-5 h-5" />
          {{ item.label }}
        </span>
      </router-link>

      <div v-if="isAuthenticated" class="border-t border-gray-100 mt-1 pt-1">
        <button
          @click="handleLogout"
          class="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-gray-50 transition-colors flex items-center gap-3"
        >
          <LogOutIcon class="w-5 h-5" />
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Menu, LogOut, Plane, Info, Globe, Gift, Bus, User, BookOpen, Settings, Award } from 'lucide-vue-next'

const router = useRouter()
const showDropdown = ref(false)
const user = ref({ name: '' })

const isAuthenticated = computed(() => !!localStorage.getItem('user_id'))

onMounted(() => {
  const storedName = localStorage.getItem('name')
  user.value.name = storedName || 'User'
})

const menuItems = [
  { label: 'Book a Flight', path: '/flight-search', icon: Plane },
  { label: 'Flight Information', path: '/flight-info', icon: Info },
  { label: 'Country Information', path: '/country-info', icon: Globe },
  { label: 'Packages & Deals', path: '/flight-packages', icon: Gift },
  { label: 'Shuttle Service', path: '/shuttle-service', icon: Bus },
  { label: 'My Bookings', path: '/profile/my-bookings', icon: BookOpen },
  { label: 'Profile', path: '/profile', icon: User },
  { label: 'Loyalty Points', path: '/profile/loyalty-points', icon: Award },
  { label: 'Settings', path: '/profile/settings', icon: Settings },
]

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function closeDropdown() {
  showDropdown.value = false
}

function handleLogout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('name')
  router.push('/')
}
</script>