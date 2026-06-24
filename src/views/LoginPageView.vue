<template>
  <div class="min-h-screen bg-gray-50 flex">

    <!-- Left panel - branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary-800 flex-col items-center justify-center p-12 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none opacity-10">
        <div class="absolute top-10 left-10 w-64 h-64 rounded-full border border-white/40"></div>
        <div class="absolute bottom-10 right-10 w-48 h-48 rounded-full border border-white/30"></div>
      </div>
      <div class="relative text-center">
        <div class="flex items-center justify-center gap-3 mb-8">
          <div class="w-12 h-12 bg-gold-500 rounded-xl flex items-center justify-center">
            <Plane class="w-6 h-6 text-primary-900" />
          </div>
          <span class="text-3xl font-display font-bold text-white">Jago<span class="text-gold-400">Travel</span></span>
        </div>
        <h2 class="text-2xl font-display font-semibold text-white mb-3">Fly from Jamaica<br />with confidence</h2>
        <p class="text-white/60 text-sm max-w-xs mx-auto leading-relaxed">
          Search, book and manage your flights from Jamaican international airports - all in one place.
        </p>
      </div>
    </div>

    <!-- Right panel - form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-md animate-fade-in-up">
        <div class="text-center mb-8 lg:hidden">
          <router-link to="/" class="inline-flex items-center gap-2 mb-4">
            <div class="w-9 h-9 bg-primary-700 rounded-lg flex items-center justify-center">
              <Plane class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-display font-bold text-gray-900">Jago<span class="text-primary-600">Travel</span></span>
          </router-link>
        </div>

        <h2 class="text-2xl font-display font-bold text-gray-900 mb-1">Welcome back</h2>
        <p class="text-gray-500 text-sm mb-8 font-sans">Log in to your account to continue</p>

        <BaseCard>
          <form @submit.prevent="login" class="space-y-6">
            <BaseInput v-model="email"    label="Email Address" type="email"    placeholder="you@email.com" required />
            <BaseInput v-model="password" label="Password"      type="password" placeholder="••••••••"      required />
            <div class="space-y-3">
              <BaseButton type="submit" size="lg" block>Log In</BaseButton>
              <BaseButton variant="outline" size="lg" block @click="$router.back()">Back</BaseButton>
            </div>
            <p class="text-center text-sm text-gray-500">
              Don't have an account?
              <router-link to="/signup" class="text-primary-600 hover:underline font-medium">Sign up</router-link>
            </p>
          </form>
        </BaseCard>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { Plane } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const email    = ref('')
const password = ref('')
const router   = useRouter()

const login = async () => {
  try {
    const res = await axios.post('/api/auth/login', {
      email: email.value,
      password: password.value,
    })
    localStorage.setItem('token',   res.data.token)
    localStorage.setItem('user_id', res.data.user.id)
    localStorage.setItem('username',res.data.user.username)
    localStorage.setItem('name',    res.data.user.name)
    router.push('/')
  } catch {
    alert('Login failed.')
  }
}
</script>