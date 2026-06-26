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

          <!-- Loading state -->
          <div v-if="loading" class="flex justify-center py-12">
            <Loader2 class="w-12 h-12 text-primary-500 animate-spin" />
          </div>

          <BaseCard v-else>
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
                <BaseButton variant="outline" type="button" @click="resetForm">Cancel</BaseButton>
                <BaseButton type="submit" :disabled="saving">
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </BaseButton>
              </div>
            </form>
          </BaseCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { User, Loader2 } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SidebarNav from '@/components/layout/sideNavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { getToken } from '@/utils/auth'

const router = useRouter()
const token = getToken()
if (!token) router.push('/login')

const loading = ref(true)
const saving = ref(false)

const form = reactive({
  fullName: '',
  email: '',
  phone: '',
  parish: 'Kingston',
  passportNumber: '',
})

const sidebarItems = [
  { label: 'My Bookings', path: '/profile/my-bookings', icon: 'Calendar' },
  { label: 'Profile', path: '/profile', icon: 'User' },
  { label: 'Loyalty Points', path: '/profile/loyalty-points', icon: 'Award' },
  { label: 'Settings', path: '/profile/settings', icon: 'Settings' },
]

const parishes = [
  'Kingston', 'St. Andrew', 'St. Catherine', 'Clarendon', 'Manchester',
  'St. Elizabeth', 'Westmoreland', 'Hanover', 'St. James', 'Trelawny',
  'St. Ann', 'St. Mary', 'Portland', 'St. Thomas',
]

const fetchUser = async () => {
  try {
    const res = await axios.get('/api/user', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const user = res.data
    form.fullName = user.name || ''
    form.email = user.email || ''
    form.phone = user.phoneNumber || ''
  } catch (error) {
    console.error('Failed to load profile:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchUser)

function resetForm() {
  loading.value = true
  fetchUser()
}

const handleSubmit = async () => {
  saving.value = true
  try {
    await axios.put(
      '/api/user',
      {
        name: form.fullName,
        email: form.email,
        phoneNumber: form.phone,
      },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Update failed:', error)
    const msg = error.response?.data?.error || 'Could not update profile.'
    alert(msg)
  } finally {
    saving.value = false
  }
}
</script>