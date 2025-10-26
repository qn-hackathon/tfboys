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

export interface Task {
  id: string
  title: string
  status: TaskStatus
  progress: number
  currentStage?: string
  createdAt: string
  errorMessage?: string
  video?: Video
  processedScenes?: number
  totalScenes?: number
  estimatedTimeRemaining?: string
}

const mockTasks: Task[] = [
  {
    id: "task-001",
    title: "春天的故事...",
    status: "generating_images",
    progress: 60,
    currentStage: "图像生成中",
    createdAt: "2025-10-25 10:30:00",
    processedScenes: 6,
    totalScenes: 10,
    estimatedTimeRemaining: "2 分钟",
  },
  {
    id: "task-002",
    title: "少年与猫...",
    status: "completed",
    progress: 100,
    createdAt: "2025-10-23 14:30:00",
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
    id: "task-003",
    title: "星际旅行...",
    status: "failed",
    progress: 35,
    errorMessage: "图像生成 API 限流,请稍后重试",
    createdAt: "2025-10-23 12:15:00",
  },
  {
    id: "task-004",
    title: "古风江湖侠客传...",
    status: "completed",
    progress: 100,
    createdAt: "2025-10-22 16:20:00",
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
    id: "task-005",
    title: "未来都市赛博朋克...",
    status: "analyzing",
    progress: 15,
    currentStage: "文本分析中",
    createdAt: "2025-10-25 11:00:00",
  },
]

export const getTasks = async (): Promise<ApiResponse<Task[]>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))

  return {
    code: 0,
    message: "获取任务列表成功",
    data: mockTasks,
  }
}

export const getTaskById = async (
  taskId: string
): Promise<ApiResponse<Task>> => {
  await new Promise((resolve) => setTimeout(resolve, 200))

  const task = mockTasks.find((t) => t.id === taskId)

  if (!task) {
    return {
      code: 40004,
      message: "任务不存在",
    }
  }

  return {
    code: 0,
    message: "获取任务详情成功",
    data: task,
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
