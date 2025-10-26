/**
 * 任务 API - Mock 实现
 */

import { ApiResponse } from './user'

/**
 * 任务状态枚举
 */
export type TaskStatus = "pending" | "analyzing" | "generating_images" | "generating_audio" | "synthesizing_video" | "completed" | "failed"

/**
 * 任务数据接口
 */
export interface Task {
  id: string
  title: string
  status: TaskStatus
  progress: number
  currentStage?: string
  processedScenes?: number
  totalScenes?: number
  estimatedTimeRemaining?: string
  thumbnailUrl?: string
  videoUrl?: string
  duration?: string
  fileSize?: string
  createdAt: string
  errorMessage?: string
  novelPrompt?: string
  resolution?: string
  aspectRatio?: string
}

/**
 * Mock 任务数据
 */
const mockTasks: Task[] = [
  {
    id: "task-001",
    title: "春天的故事...",
    status: "generating_images",
    progress: 60,
    currentStage: "图像生成中",
    processedScenes: 6,
    totalScenes: 10,
    estimatedTimeRemaining: "2 分钟",
    createdAt: "2025-10-25 10:30:00",
    novelPrompt: "春天的故事,一个少年与一只流浪猫的温暖相遇。在樱花盛开的季节,他们建立了深厚的友谊...",
  },
  {
    id: "task-002",
    title: "少年与猫...",
    status: "completed",
    progress: 100,
    thumbnailUrl: "https://placehold.co/160x120/10b981/ffffff?text=%E5%B7%B2%E5%AE%8C%E6%88%90",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
    duration: "2:30",
    totalScenes: 10,
    fileSize: "45.6 MB",
    createdAt: "2025-10-23 14:30:00",
    novelPrompt: "一个关于少年与猫的温馨故事,讲述了他们之间的深厚情谊和成长经历...",
    resolution: "1080p",
    aspectRatio: "16:9",
  },
  {
    id: "task-003",
    title: "星际旅行...",
    status: "failed",
    progress: 35,
    errorMessage: "图像生成 API 限流,请稍后重试",
    createdAt: "2025-10-23 12:15:00",
    novelPrompt: "在浩瀚的宇宙中,一艘星际飞船开始了它的探险之旅...",
  },
  {
    id: "task-004",
    title: "古风江湖侠客传...",
    status: "completed",
    progress: 100,
    thumbnailUrl: "https://placehold.co/160x120/8b5cf6/ffffff?text=%E5%8F%A4%E9%A3%8E",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
    duration: "3:15",
    totalScenes: 12,
    fileSize: "62.3 MB",
    createdAt: "2025-10-22 16:20:00",
    novelPrompt: "江湖侠客,快意恩仇。一段关于武林侠客的传奇故事...",
    resolution: "1080p",
    aspectRatio: "16:9",
  },
  {
    id: "task-005",
    title: "未来都市赛博朋克...",
    status: "analyzing",
    progress: 15,
    currentStage: "文本分析中",
    createdAt: "2025-10-25 11:00:00",
    novelPrompt: "2077年,霓虹灯照亮了这座赛博都市的夜晚,黑客与企业之间的较量永不停歇...",
  },
]

/**
 * 获取所有任务列表
 */
export const getTasks = async (): Promise<ApiResponse<Task[]>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  return {
    code: 0,
    message: '获取任务列表成功',
    data: mockTasks,
  }
}

/**
 * 根据任务ID获取任务详情
 */
export const getTaskById = async (taskId: string): Promise<ApiResponse<Task>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  const task = mockTasks.find((t) => t.id === taskId)
  
  if (!task) {
    return {
      code: 40004,
      message: '任务不存在',
    }
  }
  
  return {
    code: 0,
    message: '获取任务详情成功',
    data: task,
  }
}

/**
 * 创建新任务
 */
export interface CreateTaskParams {
  novelText: string
  style?: string
  voiceType?: string
  resolution?: string
}

export const createTask = async (params: CreateTaskParams): Promise<ApiResponse<Task>> => {
  await new Promise((resolve) => setTimeout(resolve, 500))
  
  if (!params.novelText) {
    return {
      code: 40001,
      message: '小说内容不能为空',
    }
  }
  
  const newTask: Task = {
    id: `task-${Date.now()}`,
    title: params.novelText.substring(0, 20) + '...',
    status: 'pending',
    progress: 0,
    createdAt: new Date().toLocaleString('zh-CN'),
    novelPrompt: params.novelText,
    resolution: params.resolution || '1080p',
  }
  
  mockTasks.unshift(newTask)
  
  return {
    code: 0,
    message: '任务创建成功',
    data: newTask,
  }
}

/**
 * 删除任务
 */
export const deleteTask = async (taskId: string): Promise<ApiResponse<void>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  const index = mockTasks.findIndex((t) => t.id === taskId)
  
  if (index === -1) {
    return {
      code: 40004,
      message: '任务不存在',
    }
  }
  
  mockTasks.splice(index, 1)
  
  return {
    code: 0,
    message: '任务删除成功',
  }
}

/**
 * 获取任务状态的显示文本
 */
export function getTaskStatusText(status: TaskStatus): string {
  const statusMap: Record<TaskStatus, string> = {
    pending: "等待中",
    analyzing: "文本分析中",
    generating_images: "图像生成中",
    generating_audio: "配音生成中",
    synthesizing_video: "视频合成中",
    completed: "已完成",
    failed: "失败",
  }
  return statusMap[status]
}

/**
 * 获取任务状态的颜色类型
 */
export function getTaskStatusVariant(status: TaskStatus): "default" | "secondary" | "destructive" | "outline" {
  if (status === "completed") return "default"
  if (status === "failed") return "destructive"
  return "secondary"
}
