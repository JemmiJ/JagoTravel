<template>
  <nav class="bg-primary-800 sticky top-0 z-50 border-b border-gold-500/20">
    <div class="container flex items-center justify-between h-16">

      <router-link to="/" class="flex items-center gap-2.5 group">
        <div class="w-8 h-8 bg-gold-500 rounded-lg flex items-center justify-center flex-shrink-0 transition-transform duration-200 group-hover:scale-110">
          <PlaneIcon class="w-4 h-4 text-primary-900" />
        </div>
        <span class="relative text-lg font-display font-bold text-white tracking-wide">
          Jago<span class="text-gold-400">Travel</span>
          <span class="absolute left-0 -bottom-1 h-0.5 w-0 bg-gold-400 transition-all duration-300 group-hover:w-full"></span>
        </span>
      </router-link>

      <div class="flex items-center gap-4">
        <div v-if="isAuthenticated" class="hidden sm:block text-white/80 text-sm font-medium">
          {{ user.name || 'User' }}
        </div>
       <div v-else class="hidden sm:flex items-center gap-4 text-sm">
        <router-link to="/login" class="px-4 py-1.5 rounded-full border border-white/30 text-white hover:bg-white/10 transition-all duration-200 hover:scale-105 font-medium">
          Login
        </router-link>
        <router-link to="/signup" class="px-4 py-1.5 rounded-full bg-gold-500 text-primary-900 font-semibold hover:bg-gold-400 transition-all duration-200 hover:scale-105">
          Sign Up
        </router-link>
      </div>

        <button
          @click="toggleDropdown"
          class="text-white/80 hover:text-white focus:outline-none focus:ring-2 focus:ring-gold-500/50 rounded p-1 transition-all duration-200 hover:scale-105"
          aria-label="Toggle menu"
        >
          <MenuIcon class="w-6 h-6" />
        </button>
      </div>
    </div>

    <div
      v-show="showDropdown"
      class="absolute right-4 mt-1 w-56 bg-white rounded-xl shadow-xl py-1.5 border border-gray-100 z-50"
    >
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="group relative flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-colors overflow-hidden"
        active-class="text-primary-700 bg-primary-50 font-semibold"
        @click="closeDropdown"
      >
        <component :is="item.icon" class="w-4 h-4 text-primary-500 flex-shrink-0" />
        {{ item.label }}
        <span class="absolute left-4 bottom-1 h-0.5 w-0 bg-primary-500 transition-all duration-300 group-hover:w-8"></span>
      </router-link>

      <div v-if="isAuthenticated" class="border-t border-gray-100 mt-1 pt-1">
        <button
          @click="handleLogout"
          class="w-full text-left px-4 py-2.5 text-sm text-error hover:bg-error/10 transition-all duration-200 hover:scale-[1.02] flex items-center gap-3"
        >
          <LogOutIcon class="w-4 h-4" />
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

const isAuthenticated = ref(!!localStorage.getItem('user_id'))

onMounted(() => {
  const storedName = localStorage.getItem('name')
  user.value.name = storedName || 'User'
})

const menuItems = [
  { label: 'Book a Flight',       path: '/flight-search',           icon: Plane },
  { label: 'Flight Information',  path: '/flight-info',             icon: Info },
  { label: 'Country Information', path: '/country-info',            icon: Globe },
  { label: 'Packages & Deals',    path: '/flight-packages',         icon: Gift },
  { label: 'Shuttle Service',     path: '/shuttle-service',         icon: Bus },
  { label: 'My Bookings',         path: '/profile/my-bookings',     icon: BookOpen },
  { label: 'Profile',             path: '/profile',                 icon: User },
  { label: 'Loyalty Points',      path: '/profile/loyalty-points',  icon: Award },
  { label: 'Settings',            path: '/profile/settings',        icon: Settings },
]

const MenuIcon    = Menu
const LogOutIcon  = LogOut
const PlaneIcon   = Plane

function toggleDropdown() { showDropdown.value = !showDropdown.value }
function closeDropdown()  { showDropdown.value = false }

function handleLogout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
  localStorage.removeItem('name')
  localStorage.removeItem('email')
  localStorage.removeItem('phone')
  isAuthenticated.value = false
  window.location.href = '/'
}
</script>