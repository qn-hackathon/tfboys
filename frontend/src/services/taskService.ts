import api from './api'
import type { Task, CreateTaskRequest, CreateTaskResponse } from '../types/task'

export const taskService = {
  createTask: async (data: CreateTaskRequest): Promise<CreateTaskResponse> => {
    const response = await api.post('/tasks', data)
    return response.data
  },

  getTask: async (taskId: string): Promise<Task> => {
    const response = await api.get(`/tasks/${taskId}`)
    return response.data
  },

  listTasks: async (): Promise<Task[]> => {
    const response = await api.get('/tasks')
    return response.data
  },

  deleteTask: async (taskId: string): Promise<void> => {
    await api.delete(`/tasks/${taskId}`)
  },
}
