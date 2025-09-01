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
          <button @click="showCreateModal = true" class="btn-primary">
            Create Property
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="card">
          <div class="text-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="text-gray-500 mt-4">Loading properties...</p>
          </div>
        </div>

        <!-- Properties List -->
        <div v-else>
          <div v-if="properties.length === 0" class="card">
            <div class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">No properties</h3>
              <p class="mt-1 text-sm text-gray-500">Get started by creating your first property.</p>
              <div class="mt-6">
                <button @click="showCreateModal = true" class="btn-primary">
                  Create Property
                </button>
              </div>
            </div>
          </div>

          <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div v-for="property in properties" :key="property.id" class="card hover:shadow-lg transition-shadow duration-200">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">{{ property.name }}</h3>
                  <p class="text-sm text-gray-500 mt-1">{{ property.room_count }} rooms</p>
                </div>
                <div class="flex space-x-2">
                  <button @click="editProperty(property)" class="text-gray-400 hover:text-blue-500">
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <router-link :to="`/properties/${property.id}`" class="text-gray-400 hover:text-blue-500">
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </router-link>
                </div>
              </div>
              
              <p v-if="property.description" class="text-gray-600 text-sm mb-4">
                {{ property.description }}
              </p>
              
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span>Created {{ formatDate(property.created_at) }}</span>
                <span v-if="property.is_owner" class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                  Owner
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="card border-red-200 bg-red-50">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Create/Edit Property Modal -->
        <div v-if="showCreateModal || editingProperty" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div class="bg-white rounded-lg max-w-md w-full">
            <div class="px-6 py-4 border-b">
              <h3 class="text-lg font-medium text-gray-900">
                {{ editingProperty ? 'Edit Property' : 'Create Property' }}
              </h3>
            </div>
            
            <form @submit.prevent="editingProperty ? updateProperty() : createProperty()" class="px-6 py-4">
              <div class="mb-4">
                <label for="property-name" class="block text-sm font-medium text-gray-700 mb-2">
                  Property Name
                </label>
                <input
                  id="property-name"
                  v-model="propertyForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter property name"
                />
              </div>
              
              <div class="mb-6">
                <label for="property-description" class="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  id="property-description"
                  v-model="propertyForm.description"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter property description"
                ></textarea>
              </div>
              
              <div class="flex justify-end space-x-3">
                <button
                  type="button"
                  @click="cancelPropertyForm"
                  class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="submitting"
                  class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {{ submitting ? 'Saving...' : (editingProperty ? 'Update' : 'Create') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/utils/api'

export default {
  name: 'PropertiesView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const properties = ref([])
    const loading = ref(false)
    const error = ref('')
    const showCreateModal = ref(false)
    const editingProperty = ref(null)
    const submitting = ref(false)
    
    const propertyForm = ref({
      name: '',
      description: ''
    })
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    const loadProperties = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await api.get('/properties')
        properties.value = response.data.properties
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load properties'
      } finally {
        loading.value = false
      }
    }
    
    const createProperty = async () => {
      if (!propertyForm.value.name.trim()) return
      
      submitting.value = true
      error.value = ''
      
      try {
        const response = await api.post('/properties', {
          name: propertyForm.value.name.trim(),
          description: propertyForm.value.description.trim()
        })
        
        properties.value.unshift(response.data.property)
        cancelPropertyForm()
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to create property'
      } finally {
        submitting.value = false
      }
    }
    
    const editProperty = (property) => {
      editingProperty.value = property
      propertyForm.value = {
        name: property.name,
        description: property.description || ''
      }
    }
    
    const updateProperty = async () => {
      if (!propertyForm.value.name.trim() || !editingProperty.value) return
      
      submitting.value = true
      error.value = ''
      
      try {
        const response = await api.put(`/properties/${editingProperty.value.id}`, {
          name: propertyForm.value.name.trim(),
          description: propertyForm.value.description.trim()
        })
        
        const index = properties.value.findIndex(p => p.id === editingProperty.value.id)
        if (index !== -1) {
          properties.value[index] = response.data.property
        }
        
        cancelPropertyForm()
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to update property'
      } finally {
        submitting.value = false
      }
    }
    
    const cancelPropertyForm = () => {
      showCreateModal.value = false
      editingProperty.value = null
      propertyForm.value = {
        name: '',
        description: ''
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    onMounted(() => {
      loadProperties()
    })
    
    return {
      properties,
      loading,
      error,
      showCreateModal,
      editingProperty,
      submitting,
      propertyForm,
      handleLogout,
      loadProperties,
      createProperty,
      editProperty,
      updateProperty,
      cancelPropertyForm,
      formatDate
    }
  }
}
</script>