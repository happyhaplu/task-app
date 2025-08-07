<template>
  <div class="login-container">
    <div class="login-card">
      <img
        src="https://media.licdn.com/dms/image/v2/D4D0BAQFp7rU9XBuykQ/company-logo_200_200/company-logo_200_200/0/1707218870736?e=2147483647&v=beta&t=ntCyzkNz4u9dbbqGxrULui2nCKp_AdX5UCcpTnATSpg"
        alt="Company Logo"
        class="login-logo"
      />
      <h2 class="login-title">🔐 Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="login-button">Login</button>
      </form>
      <p class="signup-link">
        Don't have an account?
        <router-link to="/signup">Sign up</router-link>
      </p>
    </div>
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

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f3f4f6;
  font-family: 'Segoe UI', sans-serif;
}

.login-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-logo {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-bottom: 16px;
  border-radius: 50%;
}

.login-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.login-form {
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

.login-button {
  padding: 12px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #4338ca;
}

.signup-link {
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}

.signup-link a {
  color: #4f46e5;
  text-decoration: none;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
