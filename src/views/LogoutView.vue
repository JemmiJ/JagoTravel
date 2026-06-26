<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary-50/30 to-white">
    <div class="text-center animate-fade-in">
      <div class="w-16 h-16 bg-primary-800 rounded-full flex items-center justify-center mx-auto mb-4">
        <Loader2 class="w-8 h-8 text-gold-400 animate-spin" />
      </div>
      <h2 class="text-xl font-display font-semibold text-gray-900">Logging out...</h2>
    </div>
  </div>
</template>
<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Loader2 } from 'lucide-vue-next'
import { getToken } from '../utils/auth'

const router = useRouter()

onMounted(async () => {
  try {
    await axios.post('/api/auth/logout', {}, {
      headers: { authorization: `Bearer ${getToken()}` }
    })
  } catch (e) {
    console.warn('Logout request failed, proceeding anyway')
  }
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
  localStorage.removeItem('name')
  localStorage.removeItem('email')
  localStorage.removeItem('phone')
  window.location.href = '/'
})
</script>