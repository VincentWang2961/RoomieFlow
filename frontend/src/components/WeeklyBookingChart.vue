<template>
  <div class="weekly-booking-chart">
    <!-- Header with week navigation -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-gray-900">Weekly Booking Schedule</h2>
      
      <div class="flex items-center space-x-4">
        <!-- Week navigation -->
        <div class="flex items-center space-x-2">
          <button 
            @click="navigateWeek(-1)"
            class="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
            title="Previous Week"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          
          <span class="text-sm font-medium text-gray-700 min-w-[200px] text-center">
            {{ formatWeekRange() }}
          </span>
          
          <button 
            @click="navigateWeek(1)"
            class="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
            title="Next Week"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
          
          <button 
            @click="goToCurrentWeek"
            class="px-3 py-1 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Today
          </button>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="text-gray-500">Loading booking data...</div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div class="text-red-800">{{ error }}</div>
    </div>

    <!-- Booking Chart -->
    <div v-else class="booking-chart">
      <!-- Chart Header -->
      <div class="grid grid-cols-8 gap-2 mb-4">
        <div class="text-sm font-medium text-gray-500 text-center">Time</div>
        <div 
          v-for="day in weekData.week_days" 
          :key="day.date"
          class="text-sm font-medium text-center"
          :class="[
            day.is_today ? 'text-primary-600 font-semibold' : 'text-gray-700'
          ]"
        >
          <div>{{ day.day_short }}</div>
          <div class="text-xs text-gray-500">{{ formatDate(day.date) }}</div>
        </div>
      </div>

      <!-- Time Sessions -->
      <div class="space-y-2">
        <div 
          v-for="session in weekData.session_types" 
          :key="session"
          class="grid grid-cols-8 gap-2"
        >
          <!-- Session label -->
          <div class="flex items-center justify-center py-3 text-sm font-medium text-gray-700 bg-gray-50 rounded-lg">
            {{ getSessionLabel(session) }}
          </div>
          
          <!-- Daily slots for this session -->
          <div 
            v-for="day in weekData.week_days" 
            :key="`${day.date}-${session}`"
            class="booking-slot min-h-[80px] border-2 border-gray-200 rounded-lg p-2 hover:border-gray-300 transition-colors cursor-pointer"
            :class="[
              day.is_today ? 'border-primary-200 bg-primary-50' : 'bg-white',
              getSlotBookings(day.date, session).length > 0 ? 'border-blue-300' : ''
            ]"
            @click="onSlotClick(day.date, session)"
          >
            <!-- Bookings in this slot -->
            <div 
              v-for="booking in getSlotBookings(day.date, session)" 
              :key="booking.id"
              class="booking-item text-xs rounded-lg p-2 mb-1 border-l-4"
              :class="getBookingClasses(booking.status)"
            >
              <div class="font-medium">{{ booking.user }}</div>
              <div class="text-gray-600">{{ booking.room_name }}</div>
              <div class="flex items-center justify-between mt-1">
                <span class="status-badge px-2 py-1 rounded-full text-xs font-medium"
                      :class="getStatusBadgeClasses(booking.status)">
                  {{ capitalizeFirst(booking.status) }}
                </span>
              </div>
            </div>
            
            <!-- Empty slot message -->
            <div v-if="getSlotBookings(day.date, session).length === 0" 
                 class="text-gray-400 text-xs text-center py-6">
              Click to book
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="mt-6 bg-gray-50 rounded-lg p-4">
      <h3 class="text-sm font-medium text-gray-700 mb-3">Status Legend</h3>
      <div class="flex flex-wrap gap-4">
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-yellow-100 border-l-4 border-yellow-400 rounded"></div>
          <span class="text-sm text-gray-600">Pending</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-green-100 border-l-4 border-green-500 rounded"></div>
          <span class="text-sm text-gray-600">Approved</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-red-100 border-l-4 border-red-500 rounded"></div>
          <span class="text-sm text-gray-600">Rejected</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 border-2 border-primary-200 bg-primary-50 rounded"></div>
          <span class="text-sm text-gray-600">Today</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import api from '@/utils/api'

export default {
  name: 'WeeklyBookingChart',
  setup() {
    const loading = ref(true)
    const error = ref('')
    const weekData = ref({
      week_start: '',
      week_days: [],
      bookings: {},
      session_types: ['morning', 'midday', 'evening'],
      session_labels: {
        'morning': 'Morning (0.5 day)',
        'midday': 'Midday (1 day)', 
        'evening': 'Evening (1 day)'
      }
    })
    
    const currentWeekStart = ref('')

    const loadWeeklyData = async (weekStart = null) => {
      loading.value = true
      error.value = ''
      
      try {
        const params = weekStart ? { week_start: weekStart } : {}
        const response = await api.get('/bookings/weekly', { params })
        
        weekData.value = response.data
        currentWeekStart.value = response.data.week_start
        
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load booking data'
        console.error('Error loading weekly booking data:', err)
      } finally {
        loading.value = false
      }
    }

    const navigateWeek = (direction) => {
      const currentDate = new Date(currentWeekStart.value)
      const newDate = new Date(currentDate.getTime() + (direction * 7 * 24 * 60 * 60 * 1000))
      const newWeekStart = newDate.toISOString().split('T')[0]
      loadWeeklyData(newWeekStart)
    }

    const goToCurrentWeek = () => {
      loadWeeklyData()
    }

    const formatWeekRange = () => {
      if (!weekData.value.week_days || weekData.value.week_days.length === 0) {
        return 'Loading...'
      }
      
      const firstDay = weekData.value.week_days[0]
      const lastDay = weekData.value.week_days[6]
      
      const startDate = new Date(firstDay.date)
      const endDate = new Date(lastDay.date)
      
      const startStr = startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      const endStr = endDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
      
      return `${startStr} - ${endStr}`
    }

    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.getDate().toString()
    }

    const getSessionLabel = (session) => {
      return weekData.value.session_labels[session] || session
    }

    const getSlotBookings = (date, session) => {
      return weekData.value.bookings[date]?.[session] || []
    }

    const getBookingClasses = (status) => {
      const baseClasses = 'booking-item'
      switch (status) {
        case 'pending':
          return `${baseClasses} bg-yellow-50 border-yellow-400 text-yellow-800`
        case 'approved':
          return `${baseClasses} bg-green-50 border-green-500 text-green-800`
        case 'rejected':
          return `${baseClasses} bg-red-50 border-red-500 text-red-800`
        default:
          return `${baseClasses} bg-gray-50 border-gray-400 text-gray-800`
      }
    }

    const getStatusBadgeClasses = (status) => {
      switch (status) {
        case 'pending':
          return 'bg-yellow-100 text-yellow-800'
        case 'approved':
          return 'bg-green-100 text-green-800'
        case 'rejected':
          return 'bg-red-100 text-red-800'
        default:
          return 'bg-gray-100 text-gray-800'
      }
    }

    const capitalizeFirst = (str) => {
      return str.charAt(0).toUpperCase() + str.slice(1)
    }

    const onSlotClick = (date, session) => {
      // TODO: Implement booking creation modal
      console.log('Slot clicked:', { date, session })
      // This will open a booking creation modal
    }

    onMounted(() => {
      loadWeeklyData()
    })

    return {
      loading,
      error,
      weekData,
      currentWeekStart,
      navigateWeek,
      goToCurrentWeek,
      formatWeekRange,
      formatDate,
      getSessionLabel,
      getSlotBookings,
      getBookingClasses,
      getStatusBadgeClasses,
      capitalizeFirst,
      onSlotClick
    }
  }
}
</script>

<style scoped>
.booking-chart {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.booking-slot {
  min-height: 80px;
  transition: all 0.2s ease;
}

.booking-slot:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.booking-item {
  transition: all 0.2s ease;
}

.booking-item:hover {
  transform: scale(1.02);
}

.status-badge {
  font-size: 0.65rem;
}

@media (max-width: 768px) {
  .weekly-booking-chart {
    overflow-x: auto;
  }
  
  .booking-chart {
    min-width: 600px;
  }
}
</style>