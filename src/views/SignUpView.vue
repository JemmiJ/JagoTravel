<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50/30 to-white flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md animate-fade-in-up">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center gap-2 mb-4 group">
          <div class="w-10 h-10 bg-gold-500 rounded-xl flex items-center justify-center transition-transform group-hover:scale-105">
            <Plane class="w-5 h-5 text-primary-900" />
          </div>
          <span class="text-3xl font-display font-bold text-gray-900">Jago<span class="text-primary-600">Travel</span></span>
        </router-link>
        <h2 class="text-2xl font-display font-bold text-gray-900">Create Account</h2>
        <p class="text-gray-600 mt-2 font-sans">Join us and start your journey</p>
      </div>

      <BaseCard>
        <form @submit.prevent="signup" class="space-y-6">
          <BaseInput v-model="formData.name" label="Full Name" placeholder="FirstName LastName" required />
          <BaseInput v-model="formData.username" label="Username" placeholder="Username" required />
          <BaseInput v-model="formData.email" label="Email Address" type="email" placeholder="someone@email.com" required />
          <BaseInput v-model="formData.password" label="Password" type="password" placeholder="••••••••" required />
          <BaseInput v-model="formData.address" label="Address" placeholder="Address" required />
          <BaseInput v-model="formData.phoneNumber" label="Phone Number" placeholder="(876) 111-1111" required />
          <div class="space-y-3">
            <BaseButton type="submit" size="lg" block :disabled="loading">
              {{ loading ? 'Creating Account...' : 'Sign Up' }}
            </BaseButton>
            <BaseButton variant="outline" size="lg" block type="button" @click="$router.back()">Back</BaseButton>
          </div>
          <p class="text-center text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="text-primary-600 hover:underline font-medium">Log in</router-link>
          </p>
        </form>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Plane } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const loading = ref(false)

const formData = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  address: '',
  phoneNumber: '',
})

async function signup() {
  loading.value = true
  const form_data = new FormData()
  Object.keys(formData.value).forEach(key => form_data.append(key, formData.value[key]))

  try {
    await axios.post('/api/signup', form_data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    formData.value = { name: '', username: '', email: '', password: '', address: '', phoneNumber: '' }
    router.push('/login')
  } catch (error) {
    console.error('Signup failed:', error)
    const message = error.response?.data?.error || 'An error occurred during signup. Please try again.'
    alert(message)
  } finally {
    loading.value = false
  }
}
</script>