<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/dashboard" class="text-xl font-semibold text-gray-900">RoomieFlow</router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/dashboard" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </router-link>
            <router-link to="/bookings" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Bookings
            </router-link>
            <button @click="handleLogout" class="text-gray-500 hover:text-gray-700 text-sm">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center mb-8">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">Properties</h2>
            <p class="text-gray-600">Manage your accommodation properties</p>
          </div>
          <button class="btn-primary">Create Property</button>
        </div>

        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Your Properties</h3>
          <div class="text-center py-12">
            <p class="text-gray-500">No properties found</p>
            <p class="text-sm text-gray-400 mt-2">Create your first property to get started</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'PropertiesView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      handleLogout
    }
  }
}
</script>