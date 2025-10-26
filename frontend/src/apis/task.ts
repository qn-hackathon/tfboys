import { ApiResponse } from "./user"
import { Video } from "./video"

export type TaskStatus =
  | "pending"
  | "analyzing"
  | "generating_images"
  | "generating_audio"
  | "synthesizing_video"
  | "completed"
  | "failed"
  | "cancelled"

export interface TaskProgress {
  current_stage?: string
  total_scenes?: number
  processed_scenes?: number
  percentage: number
  current_scene?: number
}

export interface TaskError {
  code: number
  message: string
  retry_able?: boolean
}

export interface TaskResult {
  video_url: string
  duration: number
  scenes_count: number
  thumbnail_url: string
}

export interface Task {
  task_id: string
  status: TaskStatus
  progress?: TaskProgress
  created_at: string
  updated_at?: string
  completed_at?: string
  estimated_time?: number
  error?: TaskError
  result?: TaskResult
  title?: string
  video?: Video
}

export interface CreateTaskParams {
  novel_text: string
  options?: {
    video_style?: string
    voice_type?: string
    video_resolution?: string
  }
}

export interface GetTasksParams {
  page?: number
  page_size?: number
  status?: TaskStatus
}

const mockTasks: Task[] = [
  {
    task_id: "task-001",
    title: "春天的故事...",
    status: "generating_images",
    progress: {
      current_stage: "generating_images",
      total_scenes: 10,
      processed_scenes: 6,
      percentage: 60,
    },
    created_at: "2025-10-25T10:30:00Z",
    updated_at: "2025-10-25T10:35:00Z",
  },
  {
    task_id: "task-002",
    title: "少年与猫...",
    status: "completed",
    progress: {
      percentage: 100,
    },
    created_at: "2025-10-23T14:30:00Z",
    completed_at: "2025-10-23T14:40:00Z",
    result: {
      video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
      duration: 150,
      scenes_count: 10,
      thumbnail_url: "https://placehold.co/160x120/10b981/ffffff?text=%E5%B7%B2%E5%AE%8C%E6%88%90",
    },
    video: {
      thumbnailUrl:
        "https://placehold.co/160x120/10b981/ffffff?text=%E5%B7%B2%E5%AE%8C%E6%88%90",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "古风",
      resolution: "1080p",
      duration: "2:30",
      description: "一个关于少年与猫的温馨故事",
      keywords: ["温馨", "友谊", "成长"],
      slices: [
        {
          id: "task-002-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "task-002-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:15",
          timeInSeconds: 15,
        },
      ],
      novelPrompt: "一个关于少年与猫的温馨故事,讲述了他们之间的深厚情谊和成长经历...",
      aspectRatio: "16:9",
      fileSize: "45.6 MB",
      totalScenes: 10,
      createdAt: "2025-10-23 14:30:00",
    },
  },
  {
    task_id: "task-003",
    title: "星际旅行...",
    status: "failed",
    progress: {
      percentage: 35,
    },
    created_at: "2025-10-23T12:15:00Z",
    error: {
      code: 50001,
      message: "图像生成 API 限流,请稍后重试",
      retry_able: true,
    },
  },
  {
    task_id: "task-004",
    title: "古风江湖侠客传...",
    status: "completed",
    progress: {
      percentage: 100,
    },
    created_at: "2025-10-22T16:20:00Z",
    completed_at: "2025-10-22T16:30:00Z",
    result: {
      video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
      duration: 195,
      scenes_count: 12,
      thumbnail_url: "https://placehold.co/160x120/8b5cf6/ffffff?text=%E5%8F%A4%E9%A3%8E",
    },
    video: {
      thumbnailUrl:
        "https://placehold.co/160x120/8b5cf6/ffffff?text=%E5%8F%A4%E9%A3%8E",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "古风",
      resolution: "1080p",
      duration: "3:15",
      description: "江湖侠客的传奇故事",
      keywords: ["武侠", "江湖", "侠客"],
      slices: [
        {
          id: "task-004-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "task-004-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:20",
          timeInSeconds: 20,
        },
      ],
      novelPrompt: "江湖侠客,快意恩仇。一段关于武林侠客的传奇故事...",
      aspectRatio: "16:9",
      fileSize: "62.3 MB",
      totalScenes: 12,
      createdAt: "2025-10-22 16:20:00",
    },
  },
  {
    task_id: "task-005",
    title: "未来都市赛博朋克...",
    status: "analyzing",
    progress: {
      current_stage: "analyzing",
      percentage: 15,
    },
    created_at: "2025-10-25T11:00:00Z",
  },
]

/**
 * 创建视频生成任务
 */
export const createTask = async (
  params: CreateTaskParams
): Promise<ApiResponse<Task>> => {
  // 真实请求实现（暂时注释掉）
  // const response = await fetch('/api/tasks', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify(params),
  // })
  // return await response.json()

  // 使用 mock 数据
  await new Promise((resolve) => setTimeout(resolve, 500))
  
  const newTask: Task = {
    task_id: `task_${Date.now()}`,
    status: "pending",
    created_at: new Date().toISOString(),
    estimated_time: 300,
    title: params.novel_text.slice(0, 20) + "...",
  }

  return {
    code: 0,
    message: "任务创建成功",
    data: newTask,
  }
}

/**
 * 查询任务状态
 */
export const getTaskStatus = async (
  taskId: string
): Promise<ApiResponse<Task>> => {
  // 真实请求实现（暂时注释掉）
  // const response = await fetch(`/api/tasks/${taskId}`, {
  //   method: 'GET',
  // })
  // return await response.json()

  // 使用 mock 数据
  await new Promise((resolve) => setTimeout(resolve, 200))

  const task = mockTasks.find((t) => t.task_id === taskId)

  if (!task) {
    return {
      code: 40404,
      message: "任务不存在",
    }
  }

  return {
    code: 0,
    message: "成功",
    data: task,
  }
}

/**
 * 获取任务列表
 */
export const getTasks = async (
  params?: GetTasksParams
): Promise<ApiResponse<{ total: number; page: number; page_size: number; tasks: Task[] }>> => {
  // 真实请求实现（暂时注释掉）
  // const queryParams = new URLSearchParams()
  // if (params?.page) queryParams.append('page', params.page.toString())
  // if (params?.page_size) queryParams.append('page_size', params.page_size.toString())
  // if (params?.status) queryParams.append('status', params.status)
  // 
  // const response = await fetch(`/api/tasks?${queryParams.toString()}`, {
  //   method: 'GET',
  // })
  // return await response.json()

  // 使用 mock 数据
  await new Promise((resolve) => setTimeout(resolve, 300))

  let filteredTasks = [...mockTasks]
  
  if (params?.status) {
    filteredTasks = filteredTasks.filter((t) => t.status === params.status)
  }

  const page = params?.page || 1
  const pageSize = params?.page_size || 10
  const start = (page - 1) * pageSize
  const end = start + pageSize

  return {
    code: 0,
    message: "成功",
    data: {
      total: filteredTasks.length,
      page,
      page_size: pageSize,
      tasks: filteredTasks.slice(start, end),
    },
  }
}

/**
 * 取消任务
 */
export const cancelTask = async (
  taskId: string
): Promise<ApiResponse<void>> => {
  // 真实请求实现（暂时注释掉）
  // const response = await fetch(`/api/tasks/${taskId}`, {
  //   method: 'DELETE',
  // })
  // return await response.json()

  // 使用 mock 数据
  await new Promise((resolve) => setTimeout(resolve, 200))
  
  console.log("取消任务:", taskId)

  return {
    code: 0,
    message: "任务已取消",
  }
}

export const getTaskStatusText = (status: TaskStatus): string => {
  const statusMap: Record<TaskStatus, string> = {
    pending: "等待中",
    analyzing: "文本分析中",
    generating_images: "图像生成中",
    generating_audio: "配音生成中",
    synthesizing_video: "视频合成中",
    completed: "已完成",
    failed: "失败",
    cancelled: "已取消",
  }
  return statusMap[status]
}

export const getTaskStatusVariant = (
  status: TaskStatus
): "default" | "secondary" | "destructive" | "outline" => {
  if (status === "completed") return "default"
  if (status === "failed") return "destructive"
  return "secondary"
}
