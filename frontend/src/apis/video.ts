/**
 * 视频 API - Mock 实现
 */

import { ApiResponse } from './user'

/**
 * 视频切片接口
 */
export interface VideoSlice {
  id: string
  sceneNumber: number
  thumbnailUrl: string
  timestamp: string
  timeInSeconds: number
}

/**
 * 模板视频接口
 */
export interface TemplateVideo {
  id: string
  name: string
  thumbnailUrl: string
  style: string
  novelText: string
  voiceType: "女声" | "男声" | "童声"
  resolution: "1080p" | "720p"
  slices: VideoSlice[]
}

/**
 * 生成的视频接口
 */
export interface GeneratedVideo {
  id: string
  url: string
  duration: string
  slices: VideoSlice[]
}

/**
 * Mock 视频切片数据
 */
const mockVideoSlices: VideoSlice[] = [
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
 */
const mockTemplateVideos: TemplateVideo[] = [
  {
    id: "template-1",
    name: "古风模板",
    thumbnailUrl: "https://placehold.co/200x150/10b981/ffffff?text=%E5%8F%A4%E9%A3%8E",
    style: "古风",
    novelText: "月光如水,洒在青石板铺就的小巷。一位白衣少年手持长剑,眉目如画。他缓缓走过,衣袂飘飘,宛如谪仙。忽然,一阵琴音从远处传来,婉转悠扬。少年停下脚步,侧耳倾听,眼中闪过一丝忧伤。",
    voiceType: "男声",
    resolution: "1080p",
    slices: [
      {
        id: "template-1-slice-1",
        sceneNumber: 1,
        thumbnailUrl: "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        timeInSeconds: 0,
      },
      {
        id: "template-1-slice-2",
        sceneNumber: 2,
        thumbnailUrl: "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:12",
        timeInSeconds: 12,
      },
      {
        id: "template-1-slice-3",
        sceneNumber: 3,
        thumbnailUrl: "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF3",
        timestamp: "0:24",
        timeInSeconds: 24,
      },
    ],
  },
  {
    id: "template-2",
    name: "现代模板",
    thumbnailUrl: "https://placehold.co/200x150/3b82f6/ffffff?text=%E7%8E%B0%E4%BB%A3",
    style: "现代",
    novelText: "都市的夜晚灯火通明,摩天大楼林立。一个年轻人背着双肩包,匆匆走在人潮涌动的街头。他抬头看向天空,高楼之间只能看到一小片星空。耳机里传来熟悉的旋律,让他想起了远方的家。",
    voiceType: "男声",
    resolution: "1080p",
    slices: [
      {
        id: "template-2-slice-1",
        sceneNumber: 1,
        thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        timeInSeconds: 0,
      },
      {
        id: "template-2-slice-2",
        sceneNumber: 2,
        thumbnailUrl: "https://placehold.co/160x90/3b82f6/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:10",
        timeInSeconds: 10,
      },
    ],
  },
  {
    id: "template-3",
    name: "动漫模板",
    thumbnailUrl: "https://placehold.co/200x150/ec4899/ffffff?text=%E5%8A%A8%E6%BC%AB",
    style: "动漫",
    novelText: "樱花飘落的季节,校园里传来欢快的笑声。一个扎着双马尾的少女,抱着一摞书本跑过走廊。突然,她脚下一滑,书本散落一地。正当她手忙脚乱时,一只温暖的手伸了过来。",
    voiceType: "女声",
    resolution: "1080p",
    slices: [
      {
        id: "template-3-slice-1",
        sceneNumber: 1,
        thumbnailUrl: "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        timeInSeconds: 0,
      },
      {
        id: "template-3-slice-2",
        sceneNumber: 2,
        thumbnailUrl: "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:15",
        timeInSeconds: 15,
      },
      {
        id: "template-3-slice-3",
        sceneNumber: 3,
        thumbnailUrl: "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF3",
        timestamp: "0:30",
        timeInSeconds: 30,
      },
    ],
  },
  {
    id: "template-4",
    name: "奇幻模板",
    thumbnailUrl: "https://placehold.co/200x150/8b5cf6/ffffff?text=%E5%A5%87%E5%B9%BB",
    style: "奇幻",
    novelText: "魔法森林深处,古老的魔法阵闪烁着神秘的光芒。一位穿着紫色法袍的魔法师,手持法杖,口中念念有词。突然,一道耀眼的光柱冲天而起,照亮了整片森林。精灵们纷纷现身,围绕在魔法师周围。",
    voiceType: "男声",
    resolution: "1080p",
    slices: [
      {
        id: "template-4-slice-1",
        sceneNumber: 1,
        thumbnailUrl: "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        timeInSeconds: 0,
      },
      {
        id: "template-4-slice-2",
        sceneNumber: 2,
        thumbnailUrl: "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:18",
        timeInSeconds: 18,
      },
    ],
  },
  {
    id: "template-5",
    name: "3D卡通",
    thumbnailUrl: "https://placehold.co/200x150/f59e0b/ffffff?text=3D",
    style: "3D卡通",
    novelText: "彩虹岛上,小兔子蹦蹦跳跳地寻找着胡萝卜。它圆圆的眼睛四处张望,长长的耳朵竖得高高的。忽然,它发现了一片胡萝卜地,开心地跳了起来。可是,胡萝卜地被一道篱笆围着,怎么办呢?",
    voiceType: "童声",
    resolution: "720p",
    slices: [
      {
        id: "template-5-slice-1",
        sceneNumber: 1,
        thumbnailUrl: "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        timeInSeconds: 0,
      },
      {
        id: "template-5-slice-2",
        sceneNumber: 2,
        thumbnailUrl: "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:14",
        timeInSeconds: 14,
      },
      {
        id: "template-5-slice-3",
        sceneNumber: 3,
        thumbnailUrl: "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF3",
        timestamp: "0:28",
        timeInSeconds: 28,
      },
    ],
  },
]

/**
 * Mock 生成的视频数据
 */
const mockGeneratedVideo: GeneratedVideo = {
  id: "video-1",
  url: "https://www.w3schools.com/html/mov_bbb.mp4",
  duration: "1:15",
  slices: mockVideoSlices,
}

/**
 * 获取模板视频列表
 */
export const getTemplateVideos = async (): Promise<ApiResponse<TemplateVideo[]>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  return {
    code: 0,
    message: '获取模板视频列表成功',
    data: mockTemplateVideos,
  }
}

/**
 * 根据模板ID获取模板详情
 */
export const getTemplateById = async (templateId: string): Promise<ApiResponse<TemplateVideo>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  const template = mockTemplateVideos.find((t) => t.id === templateId)
  
  if (!template) {
    return {
      code: 40004,
      message: '模板不存在',
    }
  }
  
  return {
    code: 0,
    message: '获取模板详情成功',
    data: template,
  }
}

/**
 * 获取视频切片
 */
export const getVideoSlices = async (videoId: string): Promise<ApiResponse<VideoSlice[]>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  return {
    code: 0,
    message: '获取视频切片成功',
    data: mockVideoSlices,
  }
}

/**
 * 获取生成的视频详情
 */
export const getGeneratedVideo = async (videoId: string): Promise<ApiResponse<GeneratedVideo>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  
  return {
    code: 0,
    message: '获取视频详情成功',
    data: mockGeneratedVideo,
  }
}
