<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">RoomieFlow</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/properties" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Properties
            </router-link>
            <router-link to="/bookings" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Bookings
            </router-link>
            <div class="relative">
              <span class="text-gray-700 text-sm">{{ user?.username || 'User' }}</span>
              <button @click="handleLogout" class="ml-3 text-gray-500 hover:text-gray-700 text-sm">
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Dashboard</h2>
          <p class="text-gray-600">Welcome to your accommodation management dashboard</p>
        </div>

        <!-- Quick Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-2">Quick Stats</h3>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Active Bookings:</span>
                <span class="text-sm font-medium">{{ stats.activeBookings }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Properties:</span>
                <span class="text-sm font-medium">{{ stats.properties }}</span>
              </div>
            </div>
          </div>

          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-2">Recent Activity</h3>
            <div class="mt-4">
              <p class="text-sm text-gray-500">No recent activity</p>
            </div>
          </div>

          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-2">Quick Actions</h3>
            <div class="mt-4 space-y-2">
              <router-link to="/properties" class="block w-full btn-primary text-center">
                Manage Properties
              </router-link>
              <router-link to="/bookings" class="block w-full btn-secondary text-center">
                View Bookings
              </router-link>
            </div>
          </div>
        </div>

        <!-- Usage Tracking -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Usage Tracking</h3>
          <UsageTracker @weekChange="handleWeekChange" />
        </div>

        <!-- Weekly Booking Chart -->
        <div class="card">
          <WeeklyBookingChart />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import WeeklyBookingChart from '@/components/WeeklyBookingChart.vue'
import UsageTracker from '@/components/UsageTracker.vue'

export default {
  name: 'DashboardView',
  components: {
    WeeklyBookingChart,
    UsageTracker
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const stats = ref({
      activeBookings: 0,
      properties: 0
    })
    
    const user = computed(() => authStore.user)
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    const handleWeekChange = (weekStart) => {
      // Can be used to sync week changes between components
      console.log('Week changed to:', weekStart)
    }
    
    onMounted(() => {
      // TODO: Load dashboard statistics
    })
    
    return {
      user,
      stats,
      handleLogout,
      handleWeekChange
    }
  }
}
</script>