<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <section class="bg-gradient-to-br from-primary-700 via-primary-800 to-green-900 text-white py-16">
      <div class="container text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">About Us</h1>
        <p class="text-xl text-primary-100 max-w-2xl mx-auto">Connecting Jamaica to the World Since 2010</p>
      </div>
    </section>

    <div class="container py-16 space-y-16">
      <BaseCard>
        <h2 class="text-3xl font-bold text-center mb-6">Our Story</h2>
        <div class="space-y-4 text-gray-700 text-lg leading-relaxed max-w-4xl mx-auto">
          <p>Jago Travel was founded with a simple mission: to make travel accessible, enjoyable, and stress-free for everyone. Based in the heart of Jamaica, we've been serving travelers for over a decade...</p>
          <p>Our team of dedicated travel professionals brings years of experience and a passion for exploration...</p>
          <p>Whether you're planning a business trip, a family vacation, or a solo adventure, Jago Travel is your trusted partner...</p>
        </div>
      </BaseCard>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <BaseCard v-for="item in missionItems" :key="item.title" class="text-center">
          <div class="text-4xl mb-4">{{ item.icon }}</div>
          <h3 class="text-xl font-bold text-gray-900 mb-3">{{ item.title }}</h3>
          <p class="text-gray-600">{{ item.description }}</p>
        </BaseCard>
      </div>

      <div>
        <h2 class="text-3xl font-bold text-center mb-8">Meet Our Team</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <BaseCard v-for="member in teamMembers" :key="member.name" class="overflow-hidden p-0">
            <div class="aspect-square bg-gradient-to-br from-primary-100 to-green-100 flex items-center justify-center">
              <span class="text-6xl">👤</span>
            </div>
            <div class="p-6 text-center">
              <h3 class="text-lg font-bold text-gray-900">{{ member.name }}</h3>
              <p class="text-primary-600">{{ member.role }}</p>
            </div>
          </BaseCard>
        </div>
      </div>

      <BaseCard>
        <h2 class="text-3xl font-bold text-center mb-8">Get In Touch</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 class="font-bold text-gray-900 mb-4">Contact Information</h3>
            <div class="space-y-4">
              <div class="flex items-center gap-3"><Mail class="w-5 h-5 text-primary-500" /><span class="text-gray-700">info@jagotravel.com</span></div>
              <div class="flex items-center gap-3"><Phone class="w-5 h-5 text-primary-500" /><span class="text-gray-700">+1 (876) 555-0123</span></div>
              <div class="flex items-start gap-3"><Phone class="w-5 h-5 text-primary-500 mt-1" /><div class="text-gray-700"><p class="font-semibold">Business Hours:</p><p>Monday - Friday: 8:00 AM - 6:00 PM</p><p>Saturday: 9:00 AM - 3:00 PM</p><p>Sunday: Closed</p></div></div>
            </div>
          </div>
          <div>
            <h3 class="font-bold text-gray-900 mb-4">Follow Us</h3>
            <div class="flex gap-4">
              <button v-for="(icon, idx) in socialIcons" :key="idx" class="p-3 bg-primary-100 rounded-full hover:bg-primary-200 transition"><component :is="icon" class="w-6 h-6 text-primary-500" /></button>
            </div>
          </div>
        </div>
        <div class="border-t border-gray-200 pt-8 mt-8">
          <h3 class="font-bold text-gray-900 mb-4">Office Location</h3>
          <p class="text-gray-700">123 Waterfront Drive<br />Kingston, Jamaica<br />West Indies</p>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { Mail, Phone, Facebook, Twitter, Instagram, Linkedin } from 'lucide-vue-next'

const missionItems = [
  { icon: '🎯', title: 'Our Mission', description: 'To provide exceptional travel experiences through innovative solutions, outstanding customer service, and competitive pricing.' },
  { icon: '👁️', title: 'Our Vision', description: 'To be the leading travel platform in the Caribbean, recognized for excellence in service and innovation in travel technology.' },
  { icon: '⭐', title: 'Our Values', description: 'Integrity, customer focus, innovation, and a commitment to making every journey memorable and hassle-free.' },
]

const teamMembers = [
  { name: 'Hayden Byfield', role: 'Project Manager' },
  { name: 'Aja Ferguson', role: 'Lead Backend Developer' },
  { name: 'Rhonaldo Foster', role: 'Software Tester' },
  { name: 'Jemoi Johnson', role: 'Lead Frontend Developer' },
]

const socialIcons = [Facebook, Twitter, Instagram, Linkedin]
</script>