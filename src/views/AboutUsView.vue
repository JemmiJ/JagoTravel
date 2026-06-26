<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <section class="bg-primary-800 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none select-none opacity-10">
        <div class="absolute top-8 left-12 w-48 h-48 rounded-full border border-white/30"></div>
        <div class="absolute bottom-4 right-16 w-72 h-72 rounded-full border border-white/20"></div>
      </div>
      <div class="container text-center py-16 relative animate-fade-in">
        <h1 class="text-4xl md:text-5xl font-display font-bold text-white mb-4">About <span class="text-gold-400">Us</span></h1>
        <p class="text-xl text-white/70 max-w-2xl mx-auto">Connecting Jamaica to the World Since 2010</p>
      </div>
    </section>

    <div class="container py-16 space-y-16">
      <BaseCard class="animate-fade-in-up">
        <h2 class="text-3xl font-display font-bold text-center mb-6 text-gray-900">Our Story</h2>
        <div class="space-y-4 text-gray-700 text-lg leading-relaxed max-w-4xl mx-auto">
          <p>Jago Travel was founded with a simple mission: to make travel accessible, enjoyable, and stress-free for everyone. Based in the heart of Jamaica, we've been serving travelers for over a decade...</p>
          <p>Our team of dedicated travel professionals brings years of experience and a passion for exploration...</p>
          <p>Whether you're planning a business trip, a family vacation, or a solo adventure, Jago Travel is your trusted partner...</p>
        </div>
      </BaseCard>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <BaseCard
          v-for="(item, idx) in missionItems"
          :key="item.title"
          class="text-center animate-fade-in-up"
          :style="{ animationDelay: `${idx * 100}ms` }"
        >
          <div class="w-14 h-14 bg-gold-50 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-gold-200">
            <component :is="item.icon" class="w-7 h-7 text-gold-600" />
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-3">{{ item.title }}</h3>
          <p class="text-gray-600">{{ item.description }}</p>
        </BaseCard>
      </div>

      <div>
        <h2 class="text-3xl font-display font-bold text-center mb-8 text-gray-900">Meet Our Team</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <BaseCard
            v-for="(member, idx) in teamMembers"
            :key="member.name"
            class="overflow-hidden p-0 group animate-fade-in-up"
            :style="{ animationDelay: `${idx * 100}ms` }"
          >
            <div class="aspect-square bg-gradient-to-br from-primary-700 to-primary-900 flex items-center justify-center overflow-hidden">
              <img
                :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(member.name)}&background=1e3a5f&color=ffd700&size=300`"
                :alt="member.name"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="p-6 text-center">
              <h3 class="text-lg font-bold text-gray-900 group-hover:text-primary-700 transition-colors">{{ member.name }}</h3>
              <p class="text-gold-600">{{ member.role }}</p>
            </div>
          </BaseCard>
        </div>
      </div>

      <BaseCard>
        <h2 class="text-3xl font-display font-bold text-center mb-8 text-gray-900">Get In Touch</h2>
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
              <button v-for="(icon, idx) in socialIcons" :key="idx" class="p-3 bg-primary-50 rounded-full hover:bg-gold-500 transition-all duration-200 hover:scale-105 group"><component :is="icon" class="w-6 h-6 text-primary-600 group-hover:text-primary-900" /></button>
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
import { Mail, Phone, Facebook, Twitter, Instagram, Linkedin, Target, Eye, Star } from 'lucide-vue-next'

const missionItems = [
  { icon: Target, title: 'Our Mission', description: 'To provide exceptional travel experiences through innovative solutions, outstanding customer service, and competitive pricing.' },
  { icon: Eye, title: 'Our Vision', description: 'To be the leading travel platform in the Caribbean, recognized for excellence in service and innovation in travel technology.' },
  { icon: Star, title: 'Our Values', description: 'Integrity, customer focus, innovation, and a commitment to making every journey memorable and hassle-free.' },
]

const teamMembers = [
  { name: 'Hayden Byfield', role: 'Project Manager' },
  { name: 'Aja Ferguson', role: 'Lead Backend Developer' },
  { name: 'Rhonaldo Foster', role: 'Software Tester' },
  { name: 'Jemoi Johnson', role: 'Lead Frontend Developer' },
]

const socialIcons = [Facebook, Twitter, Instagram, Linkedin]
</script>