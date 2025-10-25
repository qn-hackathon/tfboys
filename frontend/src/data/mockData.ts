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
