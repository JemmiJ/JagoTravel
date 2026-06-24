<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-16 md:py-20">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div class="lg:col-span-1">
          <SidebarNav :items="sidebarItems" />
        </div>
        <div class="lg:col-span-3 animate-fade-in-up">
          <h1 class="text-3xl font-display font-bold text-gray-900 mb-8">My Profile</h1>
          <BaseCard>
            <div class="flex items-center gap-6 mb-8 pb-8 border-b border-gray-200">
              <div class="w-24 h-24 bg-primary-800 rounded-full flex items-center justify-center">
                <User class="w-12 h-12 text-gold-400" />
              </div>
              <div>
                <h2 class="text-2xl font-display font-bold text-gray-900">{{ form.fullName }}</h2>
                <p class="text-gold-600 font-medium font-sans">Jago Travel Member</p>
              </div>
            </div>
            <form @submit.prevent="handleSubmit" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <BaseInput v-model="form.fullName" label="Full Name" />
                <BaseInput v-model="form.email" label="Email Address" type="email" />
                <BaseInput v-model="form.phone" label="Phone Number" type="tel" />
                <BaseSelect v-model="form.parish" label="Parish" :options="parishes.map(p => ({ value: p, label: p }))" />
                <BaseInput v-model="form.passportNumber" label="Passport Number" />
              </div>
              <div class="flex justify-end gap-4 pt-6 border-t border-gray-200">
                <BaseButton variant="outline" @click="reset">Cancel</BaseButton>
                <BaseButton type="submit">Save Changes</BaseButton>
              </div>
            </form>
          </BaseCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { User } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SidebarNav from '@/components/layout/sideNavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
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

const form = reactive({
  fullName: 'John Doe',
  email: 'john.doe@example.com',
  phone: '+1 876 123 4567',
  parish: 'Kingston',
  passportNumber: 'JM1234567',
})

const parishes = [
  'Kingston', 'St. Andrew', 'St. Catherine', 'Clarendon', 'Manchester',
  'St. Elizabeth', 'Westmoreland', 'Hanover', 'St. James', 'Trelawny',
  'St. Ann', 'St. Mary', 'Portland', 'St. Thomas',
]

function reset() {
  Object.assign(form, {
    fullName: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 876 123 4567',
    parish: 'Kingston',
    passportNumber: 'JM1234567',
  })
}

function handleSubmit() {
  alert('Profile updated! (This is a demo)')
}
</script>