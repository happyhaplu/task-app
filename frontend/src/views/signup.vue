<template>
  <div class="signup-container">
    <div class="signup-card">
      <img
        src="https://media.licdn.com/dms/image/v2/D4D0BAQFp7rU9XBuykQ/company-logo_200_200/company-logo_200_200/0/1707218870736?e=2147483647&v=beta&t=ntCyzkNz4u9dbbqGxrULui2nCKp_AdX5UCcpTnATSpg"
        alt="Company Logo"
        class="signup-logo"
      />
      <h2 class="signup-title">📝 Sign Up</h2>
      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="signup-button">Sign Up</button>
      </form>
      <p v-if="error" class="error-message">{{ error }}</p>
      <p class="login-link">
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </div>
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
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f3f4f6;
  font-family: 'Segoe UI', sans-serif;
}

.signup-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.signup-logo {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-bottom: 16px;
  border-radius: 50%;
}

.signup-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 6px;
  font-weight: 500;
  color: #555;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.signup-button {
  padding: 12px;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.signup-button:hover {
  background-color: #059669;
}

.error-message {
  margin-top: 12px;
  color: #dc2626;
  font-size: 14px;
}

.login-link {
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}

.login-link a {
  color: #10b981;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
