<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white shadow rounded">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-4">
        <label class="block mb-1 font-medium">Email</label>
        <input v-model="email" type="email" class="w-full p-2 border rounded" required />
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-medium">Password</label>
        <input v-model="password" type="password" class="w-full p-2 border rounded" required />
      </div>
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Login
      </button>
    </form>
    <p class="mt-4 text-sm">
      Don't have an account?
      <router-link to="/signup" class="text-blue-600 hover:underline">Sign up</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { loginUser } from '../services/api'

const email = ref('')
const password = ref('')
const router = useRouter()
const auth = useAuthStore()

const handleLogin = async () => {
  try {
    const response = await loginUser(email.value, password.value)
    if (response.access_token) {
      auth.setToken(response.access_token)
      router.push('/tasks')
    } else {
      alert('Invalid credentials')
    }
  } catch (error) {
    console.error(error)
    alert('Login failed')
  }
}
</script>
