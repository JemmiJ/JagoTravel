<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="text-center">
      <h2 class="text-xl font-semibold mb-4">Logging out...</h2>
    </div>
  </div>
</template>
<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
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
  localStorage.removeItem('name')
  router.push('/')
})
</script>