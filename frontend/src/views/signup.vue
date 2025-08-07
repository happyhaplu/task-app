<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="handleSignup">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const handleSignup = async () => {
  try {
    await axios.post('http://localhost:8000/signup', {
      email: email.value,
      password: password.value
    })
    router.push('/login')
  } catch (err) {
    error.value = 'Signup failed. Try a different email.'
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
}
</style>
