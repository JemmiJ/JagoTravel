<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50/30 to-white flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center gap-2 mb-4">
          <Plane class="w-10 h-10 text-primary-500" />
          <span class="text-3xl font-display text-gray-900">JagoTravel</span>
        </router-link>
        <h2 class="text-2xl font-bold text-gray-900">Welcome Back</h2>
        <p class="text-gray-600 mt-2">Log in to your account to continue</p>
      </div>

      <BaseCard>
        <form @submit.prevent="login" class="space-y-6">
          <BaseInput v-model="email" label="Email Address" type="email" placeholder="someone@email.com" required />
          <BaseInput v-model="password" label="Password" type="password" placeholder="••••••••" required />
          <div class="space-y-3">
            <BaseButton type="submit" size="lg" block>Login</BaseButton>
            <BaseButton variant="outline" size="lg" block @click="$router.back()">Back</BaseButton>
          </div>
          <p class="text-center text-sm text-gray-600">
            Don't have an account?
            <router-link to="/signup" class="text-primary-500 hover:underline font-medium">Sign up</router-link>
          </p>
        </form>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { Plane } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const email = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('/api/auth/login', {
      email: email.value,
      password: password.value,
    })
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user_id', res.data.user.id)
    localStorage.setItem('username', res.data.user.username)
    localStorage.setItem('name', res.data.user.name)
    router.push('/')
  } catch {
    alert('Login failed.')
  }
}
</script>