<template>
  <div class="usage-tracker">
    <!-- Loading State -->
    <div v-if="loading" class="animate-pulse">
      <div class="h-4 bg-gray-200 rounded mb-4"></div>
      <div class="h-20 bg-gray-200 rounded mb-4"></div>
      <div class="h-4 bg-gray-200 rounded mb-2"></div>
      <div class="h-4 bg-gray-200 rounded w-3/4"></div>
    </div>

    <!-- Usage Statistics -->
    <div v-else-if="usageData" class="space-y-6">
      <!-- Warnings Section -->
      <div v-if="usageData.warnings && usageData.warnings.length > 0" class="space-y-2">
        <div v-for="warning in usageData.warnings" :key="warning.property_id" 
             :class="getWarningClasses(warning.type)"
             class="flex items-start p-3 rounded-lg border">
          <div class="flex-shrink-0">
            <svg v-if="warning.type === 'exceeded'" class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <svg v-else class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium">{{ warning.message }}</p>
          </div>
        </div>
      </div>

      <!-- Overall Status Badge -->
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-medium text-gray-900">Weekly Usage Summary</h3>
        <span :class="getStatusBadgeClasses(usageData.overall_status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
          {{ getStatusLabel(usageData.overall_status) }}
        </span>
      </div>

      <!-- Property Breakdown -->
      <div class="space-y-4">
        <div v-for="property in usageData.property_breakdown" :key="property.property_id" 
             class="bg-white p-4 rounded-lg border border-gray-200">
          
          <!-- Property Header -->
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-medium text-gray-900">{{ property.property_name }}</h4>
            <span :class="getStatusBadgeClasses(property.status)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
              {{ getStatusLabel(property.status) }}
            </span>
          </div>

          <!-- Usage Progress Bar -->
          <div class="mb-3">
            <div class="flex justify-between text-sm text-gray-600 mb-1">
              <span>{{ property.total_usage }} / {{ property.weekly_limit }} days</span>
              <span>{{ property.usage_percentage }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="h-3 rounded-full transition-all duration-300" 
                   :class="getProgressBarClasses(property.status)"
                   :style="{ width: Math.min(property.usage_percentage, 100) + '%' }">
              </div>
            </div>
          </div>

          <!-- Usage Breakdown -->
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-500">Approved:</span>
              <span class="font-medium text-green-600 ml-1">{{ property.approved_usage }} days</span>
            </div>
            <div>
              <span class="text-gray-500">Pending:</span>
              <span class="font-medium text-yellow-600 ml-1">{{ property.pending_usage }} days</span>
            </div>
            <div>
              <span class="text-gray-500">Remaining:</span>
              <span class="font-medium text-blue-600 ml-1">{{ property.remaining_days }} days</span>
            </div>
            <div>
              <span class="text-gray-500">Bookings:</span>
              <span class="font-medium text-gray-900 ml-1">{{ property.bookings.length }}</span>
            </div>
          </div>

          <!-- Recent Bookings (collapsible) -->
          <div v-if="property.bookings.length > 0" class="mt-4">
            <button @click="toggleBookings(property.property_id)" 
                    class="flex items-center text-sm text-gray-600 hover:text-gray-900">
              <svg class="h-4 w-4 mr-1 transform transition-transform duration-200"
                   :class="{ 'rotate-90': expandedBookings.has(property.property_id) }"
                   fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
              {{ expandedBookings.has(property.property_id) ? 'Hide' : 'Show' }} Recent Bookings
            </button>
            
            <div v-if="expandedBookings.has(property.property_id)" class="mt-3 space-y-2">
              <div v-for="booking in property.bookings.slice(0, 5)" :key="booking.id"
                   class="flex items-center justify-between p-2 bg-gray-50 rounded text-sm">
                <div>
                  <span class="font-medium">{{ formatDate(booking.date) }}</span>
                  <span class="text-gray-500 ml-2">{{ booking.session }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-gray-600">{{ booking.duration }}d</span>
                  <span :class="getBookingStatusClasses(booking.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                    {{ booking.status }}
                  </span>
                </div>
              </div>
              <div v-if="property.bookings.length > 5" class="text-xs text-gray-500 text-center">
                And {{ property.bookings.length - 5 }} more...
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Week Navigation -->
      <div class="flex items-center justify-center space-x-4 pt-4 border-t">
        <button @click="changeWeek(-1)" class="flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-900">
          <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Previous Week
        </button>
        
        <div class="text-sm font-medium text-gray-900">
          {{ formatWeekRange(usageData.week_start, usageData.week_end) }}
        </div>
        
        <button @click="changeWeek(1)" class="flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-900">
          Next Week
          <svg class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="p-4 border border-red-200 bg-red-50 rounded-lg">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Error loading usage data</h3>
          <p class="text-sm text-red-700 mt-1">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-8">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No usage data</h3>
      <p class="mt-1 text-sm text-gray-500">No bookings found for the selected week.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import api from '@/utils/api'

export default {
  name: 'UsageTracker',
  props: {
    weekStart: {
      type: String,
      default: null
    }
  },
  emits: ['weekChange'],
  setup(props, { emit }) {
    const usageData = ref(null)
    const loading = ref(false)
    const error = ref('')
    const expandedBookings = ref(new Set())

    const currentWeekStart = ref(props.weekStart || getCurrentWeekStart())

    function getCurrentWeekStart() {
      const today = new Date()
      const monday = new Date(today)
      monday.setDate(today.getDate() - today.getDay() + 1)
      return monday.toISOString().split('T')[0]
    }

    const loadUsageData = async (weekStart = null) => {
      loading.value = true
      error.value = ''
      
      try {
        const params = new URLSearchParams()
        if (weekStart) {
          params.append('week_start', weekStart)
        }
        
        const response = await api.get(`/usage/weekly?${params.toString()}`)
        usageData.value = response.data
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load usage data'
        usageData.value = null
      } finally {
        loading.value = false
      }
    }

    const changeWeek = (direction) => {
      const currentDate = new Date(currentWeekStart.value)
      currentDate.setDate(currentDate.getDate() + (direction * 7))
      currentWeekStart.value = currentDate.toISOString().split('T')[0]
      
      loadUsageData(currentWeekStart.value)
      emit('weekChange', currentWeekStart.value)
    }

    const toggleBookings = (propertyId) => {
      if (expandedBookings.value.has(propertyId)) {
        expandedBookings.value.delete(propertyId)
      } else {
        expandedBookings.value.add(propertyId)
      }
    }

    const getWarningClasses = (type) => {
      const baseClasses = 'border-l-4'
      switch (type) {
        case 'exceeded':
          return `${baseClasses} border-red-400 bg-red-50`
        case 'warning':
          return `${baseClasses} border-yellow-400 bg-yellow-50`
        default:
          return `${baseClasses} border-blue-400 bg-blue-50`
      }
    }

    const getStatusBadgeClasses = (status) => {
      switch (status) {
        case 'exceeded':
          return 'bg-red-100 text-red-800'
        case 'warning':
          return 'bg-yellow-100 text-yellow-800'
        case 'caution':
          return 'bg-orange-100 text-orange-800'
        default:
          return 'bg-green-100 text-green-800'
      }
    }

    const getProgressBarClasses = (status) => {
      switch (status) {
        case 'exceeded':
          return 'bg-red-500'
        case 'warning':
          return 'bg-yellow-500'
        case 'caution':
          return 'bg-orange-500'
        default:
          return 'bg-green-500'
      }
    }

    const getBookingStatusClasses = (status) => {
      switch (status) {
        case 'approved':
          return 'bg-green-100 text-green-800'
        case 'pending':
          return 'bg-yellow-100 text-yellow-800'
        case 'rejected':
          return 'bg-red-100 text-red-800'
        default:
          return 'bg-gray-100 text-gray-800'
      }
    }

    const getStatusLabel = (status) => {
      switch (status) {
        case 'exceeded':
          return 'Exceeded'
        case 'warning':
          return 'Warning'
        case 'caution':
          return 'Caution'
        default:
          return 'Normal'
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-AU', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
      })
    }

    const formatWeekRange = (startDate, endDate) => {
      const start = new Date(startDate)
      const end = new Date(endDate)
      
      return `${start.toLocaleDateString('en-AU', { 
        month: 'short', 
        day: 'numeric' 
      })} - ${end.toLocaleDateString('en-AU', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
      })}`
    }

    onMounted(() => {
      loadUsageData(currentWeekStart.value)
    })

    return {
      usageData,
      loading,
      error,
      expandedBookings,
      currentWeekStart,
      loadUsageData,
      changeWeek,
      toggleBookings,
      getWarningClasses,
      getStatusBadgeClasses,
      getProgressBarClasses,
      getBookingStatusClasses,
      getStatusLabel,
      formatDate,
      formatWeekRange
    }
  }
}
</script>

<style scoped>
.usage-tracker {
  @apply max-w-4xl mx-auto;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>