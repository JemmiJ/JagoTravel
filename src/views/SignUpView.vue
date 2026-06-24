<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50/30 to-white flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center gap-2 mb-4">
          <Plane class="w-10 h-10 text-primary-500" />
          <span class="text-3xl font-display text-gray-900">JagoTravel</span>
        </router-link>
        <h2 class="text-2xl font-bold text-gray-900">Create Account</h2>
        <p class="text-gray-600 mt-2">Join us and start your journey</p>
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
            <BaseButton type="submit" size="lg" block>Sign Up</BaseButton>
            <BaseButton variant="outline" size="lg" block @click="$router.back()">Back</BaseButton>
          </div>
          <p class="text-center text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="text-primary-500 hover:underline font-medium">Log in</router-link>
          </p>
        </form>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plane } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const formData = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  address: '',
  phoneNumber: '',
})

const router = useRouter()

function signup() {
  const form_data = new FormData()
  Object.keys(formData.value).forEach(key => form_data.append(key, formData.value[key]))

  fetch('/api/signup', {
    method: 'POST',
    body: form_data,
  })
    .then(res => {
      if (!res.ok) throw new Error('Failed to signup')
      return res.json()
    })
    .then(() => {
      formData.value = { name: '', username: '', email: '', password: '', address: '', phoneNumber: '' }
      router.push('/login')
    })
    .catch(error => console.error('Error:', error))
}
</script>