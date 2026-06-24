<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container py-16 md:py-20">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div class="lg:col-span-1">
          <SidebarNav :items="sidebarItems" />
        </div>
        <div class="lg:col-span-3 animate-fade-in-up">
          <h1 class="text-3xl font-display font-bold text-gray-900 mb-8">Settings</h1>

          <div class="space-y-6">
            <BaseCard>
              <div class="flex items-center gap-3 mb-6">
                <Bell class="w-6 h-6 text-primary-500" />
                <h2 class="text-xl font-display font-bold text-gray-900">Notifications</h2>
              </div>
              <div class="space-y-4">
                <label v-for="(setting, key) in notificationSettings" :key="key" class="flex items-center justify-between cursor-pointer">
                  <div>
                    <p class="font-medium text-gray-900">{{ setting.label }}</p>
                    <p class="text-sm text-gray-600">{{ setting.description }}</p>
                  </div>
                  <input type="checkbox" v-model="setting.value" class="w-5 h-5 text-gold-500 rounded focus:ring-gold-500" />
                </label>
              </div>
            </BaseCard>

            <BaseCard>
              <div class="flex items-center gap-3 mb-6">
                <Globe class="w-6 h-6 text-primary-500" />
                <h2 class="text-xl font-display font-bold text-gray-900">Preferences</h2>
              </div>
              <div class="space-y-4">
                <BaseSelect
                  v-model="currency"
                  label="Currency"
                  :options="currencyOptions.map(c => ({ value: c, label: c }))"
                />
                <BaseSelect
                  v-model="language"
                  label="Language"
                  :options="languageOptions.map(l => ({ value: l, label: l }))"
                />
              </div>
            </BaseCard>

            <BaseCard>
              <div class="flex items-center gap-3 mb-6">
                <Lock class="w-6 h-6 text-primary-500" />
                <h2 class="text-xl font-display font-bold text-gray-900">Security</h2>
              </div>
              <div class="space-y-4">
                <button class="w-full text-left px-4 py-3 border border-gray-300 rounded-lg hover:border-gold-400 hover:bg-primary-50 transition-colors duration-200">
                  <p class="font-medium text-gray-900">Change Password</p>
                  <p class="text-sm text-gray-600">Update your password to keep your account secure</p>
                </button>
                <button class="w-full text-left px-4 py-3 border border-gray-300 rounded-lg hover:border-gold-400 hover:bg-primary-50 transition-colors duration-200">
                  <p class="font-medium text-gray-900">Two-Factor Authentication</p>
                  <p class="text-sm text-gray-600">Add an extra layer of security to your account</p>
                </button>
              </div>
            </BaseCard>

            <div class="flex justify-end">
              <BaseButton type="submit">Save All Changes</BaseButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Calendar, User, Award, Settings as SettingsIcon, Bell, Lock, Globe } from 'lucide-vue-next'
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SidebarNav from '@/components/layout/sideNavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { getToken } from '@/utils/auth'

const router = useRouter()
if (!getToken()) router.push('/login')

const sidebarItems = [
  { label: 'My Bookings', path: '/profile/my-bookings', icon: 'Calendar' },
  { label: 'Profile', path: '/profile', icon: 'User' },
  { label: 'Loyalty Points', path: '/profile/loyalty-points', icon: 'Award' },
  { label: 'Settings', path: '/profile/settings', icon: 'SettingsIcon' },
]

const currency = ref('JMD')
const language = ref('English')
const currencyOptions = ['JMD', 'USD', 'EUR', 'GBP']
const languageOptions = ['English', 'Spanish', 'French']

const notificationSettings = reactive({
  email: { label: 'Email Notifications', description: 'Receive booking confirmations and updates via email', value: true },
  sms: { label: 'SMS Notifications', description: 'Receive flight reminders and updates via SMS', value: true },
  promotional: { label: 'Promotional Emails', description: 'Receive special offers and deals', value: false },
})
</script>