/**
 * Mock 数据文件
 * 用于视频生成页面的开发和测试
 */

export interface VideoSlice {
  id: string
  sceneNumber: number
  thumbnailUrl: string
  timestamp: string
  timeInSeconds: number
}

export interface TemplateVideo {
  id: string
  name: string
  thumbnailUrl: string
  style: string
}

export interface GeneratedVideo {
  id: string
  url: string
  duration: string
  slices: VideoSlice[]
}

/**
 * Mock 视频切片数据
 * 注意：这是 mock 数据，实际使用时需要从后端 API 获取
 */
export const mockVideoSlices: VideoSlice[] = [
  {
    id: "slice-1",
    sceneNumber: 1,
    thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+1",
    timestamp: "0:00",
    timeInSeconds: 0,
  },
  {
    id: "slice-2",
    sceneNumber: 2,
    thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+2",
    timestamp: "0:15",
    timeInSeconds: 15,
  },
  {
    id: "slice-3",
    sceneNumber: 3,
    thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+3",
    timestamp: "0:30",
    timeInSeconds: 30,
  },
  {
    id: "slice-4",
    sceneNumber: 4,
    thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+4",
    timestamp: "0:45",
    timeInSeconds: 45,
  },
  {
    id: "slice-5",
    sceneNumber: 5,
    thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+5",
    timestamp: "1:00",
    timeInSeconds: 60,
  },
]

/**
 * Mock 模板视频数据
 * 注意：这是 mock 数据，实际使用时需要从后端 API 获取
 */
export const mockTemplateVideos: TemplateVideo[] = [
  {
    id: "template-1",
    name: "古风模板",
    thumbnailUrl: "https://placehold.co/200x150/10b981/ffffff?text=%E5%8F%A4%E9%A3%8E",
    style: "古风",
  },
  {
    id: "template-2",
    name: "现代模板",
    thumbnailUrl: "https://placehold.co/200x150/3b82f6/ffffff?text=%E7%8E%B0%E4%BB%A3",
    style: "现代",
  },
  {
    id: "template-3",
    name: "动漫模板",
    thumbnailUrl: "https://placehold.co/200x150/ec4899/ffffff?text=%E5%8A%A8%E6%BC%AB",
    style: "动漫",
  },
  {
    id: "template-4",
    name: "奇幻模板",
    thumbnailUrl: "https://placehold.co/200x150/8b5cf6/ffffff?text=%E5%A5%87%E5%B9%BB",
    style: "奇幻",
  },
  {
    id: "template-5",
    name: "3D卡通",
    thumbnailUrl: "https://placehold.co/200x150/f59e0b/ffffff?text=3D",
    style: "3D卡通",
  },
]

/**
 * Mock 生成的视频数据
 * 注意：这是 mock 数据，实际使用时需要从后端 API 获取
 */
export const mockGeneratedVideo: GeneratedVideo = {
  id: "video-1",
  url: "https://www.w3schools.com/html/mov_bbb.mp4",
  duration: "1:15",
  slices: mockVideoSlices,
}

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
 * 注意：这是 mock 数据，实际使用时需要从后端 API 获取
 */
export const mockTasks: Task[] = [
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
    novelPrompt: "春天的故事，一个少年与一只流浪猫的温暖相遇。在樱花盛开的季节，他们建立了深厚的友谊...",
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
    novelPrompt: "一个关于少年与猫的温馨故事，讲述了他们之间的深厚情谊和成长经历...",
    resolution: "1080p",
    aspectRatio: "16:9",
  },
  {
    id: "task-003",
    title: "星际旅行...",
    status: "failed",
    progress: 35,
    errorMessage: "图像生成 API 限流，请稍后重试",
    createdAt: "2025-10-23 12:15:00",
    novelPrompt: "在浩瀚的宇宙中，一艘星际飞船开始了它的探险之旅...",
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
    novelPrompt: "江湖侠客，快意恩仇。一段关于武林侠客的传奇故事...",
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
    novelPrompt: "2077年，霓虹灯照亮了这座赛博都市的夜晚，黑客与企业之间的较量永不停歇...",
  },
]

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
