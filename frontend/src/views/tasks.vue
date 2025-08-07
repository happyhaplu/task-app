<template>
  <div class="container">
    <h2 class="title">📝 Task Dashboard</h2>
    <p class="subtitle">Organize your tasks with style and simplicity.</p>

    <!-- Task Creation Form -->
    <form @submit.prevent="createTask" class="task-form">
      <input
        v-model="newTaskDescription"
        type="text"
        placeholder="Enter a new task..."
        required
        class="task-input"
      />
      <button type="submit" class="task-button">Add Task</button>
    </form>

    <!-- Task List -->
    <div v-if="tasks.length" class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task-card">
        <input
          type="checkbox"
          v-model="task.completed"
          @change="updateTask(task)"
          class="checkbox"
        />

        <div class="task-content">
          <template v-if="editingTaskId === task.id">
            <input
              v-model="editedDescription"
              type="text"
              class="edit-input"
            />
            <div class="edit-actions">
              <button @click="saveEdit(task)" class="save-button">Save</button>
              <button @click="cancelEdit" class="cancel-button">Cancel</button>
            </div>
          </template>
          <template v-else>
            <span :class="{ completed: task.completed }" class="task-text">
              {{ task.description }}
            </span>
            <div class="task-actions">
              <button @click="startEdit(task)" class="edit-button">Edit</button>
              <button @click="deleteTask(task.id)" class="delete-button">Delete</button>
            </div>
          </template>
        </div>
      </div>
    </div>
    <p v-else class="empty-message">🎉 No tasks yet. Add one above!</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Task {
  id: number
  description: string
  completed: boolean
  user_id: number
}

const tasks = ref<Task[]>([])
const newTaskDescription = ref("")
const editingTaskId = ref<number | null>(null)
const editedDescription = ref("")

const fetchTasks = async () => {
  const token = localStorage.getItem("token")
  const response = await fetch("http://localhost:8000/tasks", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  if (response.ok) {
    const data: Task[] = await response.json()
    tasks.value = data
  } else {
    console.error("Failed to fetch tasks")
  }
}

const createTask = async () => {
  const token = localStorage.getItem("token")
  const response = await fetch("http://localhost:8000/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      description: newTaskDescription.value,
      completed: false,
    }),
  })
  if (response.ok) {
    const newTask: Task = await response.json()
    tasks.value.push(newTask)
    newTaskDescription.value = ""
  } else {
    console.error("Failed to create task")
  }
}

const updateTask = async (task: Task) => {
  const token = localStorage.getItem("token")
  const response = await fetch(`http://localhost:8000/tasks/${task.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      description: task.description,
      completed: task.completed,
    }),
  })
  if (!response.ok) {
    console.error("Failed to update task")
  }
}

const startEdit = (task: Task) => {
  editingTaskId.value = task.id
  editedDescription.value = task.description
}

const cancelEdit = () => {
  editingTaskId.value = null
  editedDescription.value = ""
}

const saveEdit = async (task: Task) => {
  task.description = editedDescription.value
  await updateTask(task)
  editingTaskId.value = null
  editedDescription.value = ""
}

const deleteTask = async (taskId: number) => {
  const token = localStorage.getItem("token")
  const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  if (response.ok) {
    tasks.value = tasks.value.filter(task => task.id !== taskId)
  } else {
    console.error("Failed to delete task")
  }
}

onMounted(fetchTasks)
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 40px auto;
  padding: 24px;
  background: #fdfdfd;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', sans-serif;
}

.title {
  font-size: 28px;
  margin-bottom: 4px;
  color: #333;
}

.subtitle {
  font-size: 16px;
  margin-bottom: 20px;
  color: #666;
}

.task-form {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.task-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.task-button {
  padding: 10px 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.task-button:hover {
  background-color: #4338ca;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  display: flex;
  align-items: center;
  background: white;
  padding: 12px 16px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.task-card:hover {
  transform: scale(1.01);
}

.checkbox {
  margin-right: 12px;
  transform: scale(1.2);
}

.task-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.task-text {
  font-size: 16px;
  color: #333;
}

.completed {
  text-decoration: line-through;
  color: #999;
}

.task-actions button,
.edit-actions button {
  margin-left: 8px;
  padding: 6px 10px;
  font-size: 13px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-button {
  background-color: #3b82f6;
  color: white;
}

.edit-button:hover {
  background-color: #2563eb;
}

.delete-button {
  background-color: #ef4444;
  color: white;
}

.delete-button:hover {
  background-color: #dc2626;
}

.save-button {
  background-color: #10b981;
  color: white;
}

.save-button:hover {
  background-color: #059669;
}

.cancel-button {
  background-color: #9ca3af;
  color: white;
}

.cancel-button:hover {
  background-color: #6b7280;
}

.edit-input {
  flex: 1;
  padding: 6px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-right: 10px;
}

.empty-message {
  text-align: center;
  color: #888;
  margin-top: 20px;
}
</style>
