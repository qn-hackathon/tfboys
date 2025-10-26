import { ApiResponse } from "./user"

export interface VideoSlice {
  id: string
  sceneNumber: number
  thumbnailUrl: string
  timestamp: string
  timeInSeconds: number
}

export interface Video {
  thumbnailUrl: string
  videoUrl: string
  style: "古风" | "现代" | "动漫" | "奇幻" | "3D卡通"
  resolution: "1080p" | "720p" | "4K"
  duration: string
  description: string
  keywords: string[]
  slices: VideoSlice[]
  novelPrompt: string
  aspectRatio: string
  fileSize: string
  totalScenes: number
  createdAt: string
}

export interface VideoTemplate {
  id: string
  name: string
  video: Video
}

export interface VideoGenerationParams {
  templateId: string
  novelText: string
  voiceType?: "女声" | "男声" | "童声"
}

export interface VideoGenerationResponse {
  taskId: string
  status: "pending" | "processing" | "completed" | "failed"
}

export interface VideoStatusResponse {
  taskId: string
  status: "pending" | "processing" | "completed" | "failed"
  progress: number
  video?: Video
}

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

const mockVideoTemplates: VideoTemplate[] = [
  {
    id: "template-001",
    name: "古风江湖夜行",
    video: {
      thumbnailUrl:
        "https://placehold.co/400x225/10b981/ffffff?text=%E5%8F%A4%E9%A3%8E%E6%B1%9F%E6%B9%96",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "古风",
      resolution: "1080p",
      duration: "2:45",
      description: "月光下的江湖侠客,行走于青石板街道,展现古典武侠之美",
      keywords: ["侠客", "月夜", "武侠", "古典"],
      novelPrompt:
        "月光如水,洒在青石板铺就的小巷。一位白衣少年手持长剑,眉目如画。他缓缓走过,衣袂飘飘,宛如谪仙。忽然,一阵琴音从远处传来,婉转悠扬。",
      aspectRatio: "16:9",
      fileSize: "52.3 MB",
      totalScenes: 8,
      createdAt: "2025-10-20 14:30:00",
      slices: [
        {
          id: "template-001-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "template-001-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:20",
          timeInSeconds: 20,
        },
        {
          id: "template-001-slice-3",
          sceneNumber: 3,
          thumbnailUrl:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF3",
          timestamp: "0:40",
          timeInSeconds: 40,
        },
      ],
    },
  },
  {
    id: "template-002",
    name: "现代都市夜景",
    video: {
      thumbnailUrl:
        "https://placehold.co/400x225/3b82f6/ffffff?text=%E7%8E%B0%E4%BB%A3%E9%83%BD%E5%B8%82",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "现代",
      resolution: "4K",
      duration: "3:12",
      description: "繁华都市的霓虹灯下,讲述现代人的故事",
      keywords: ["都市", "霓虹", "现代", "夜景"],
      novelPrompt:
        "都市的夜晚灯火通明,摩天大楼林立。一个年轻人背着双肩包,匆匆走在人潮涌动的街头。他抬头看向天空,高楼之间只能看到一小片星空。",
      aspectRatio: "16:9",
      fileSize: "89.5 MB",
      totalScenes: 10,
      createdAt: "2025-10-21 09:15:00",
      slices: [
        {
          id: "template-002-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/3b82f6/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "template-002-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/3b82f6/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:25",
          timeInSeconds: 25,
        },
      ],
    },
  },
  {
    id: "template-003",
    name: "动漫校园物语",
    video: {
      thumbnailUrl:
        "https://placehold.co/400x225/ec4899/ffffff?text=%E5%8A%A8%E6%BC%AB%E6%A0%A1%E5%9B%AD",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "动漫",
      resolution: "1080p",
      duration: "2:30",
      description: "樱花飘落的校园,少女们的青春物语",
      keywords: ["校园", "樱花", "青春", "动漫"],
      novelPrompt:
        "樱花飘落的季节,校园里传来欢快的笑声。一个扎着双马尾的少女,抱着一摞书本跑过走廊。突然,她脚下一滑,书本散落一地。正当她手忙脚乱时,一只温暖的手伸了过来。",
      aspectRatio: "16:9",
      fileSize: "45.8 MB",
      totalScenes: 9,
      createdAt: "2025-10-22 11:20:00",
      slices: [
        {
          id: "template-003-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "template-003-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:18",
          timeInSeconds: 18,
        },
        {
          id: "template-003-slice-3",
          sceneNumber: 3,
          thumbnailUrl:
            "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF3",
          timestamp: "0:36",
          timeInSeconds: 36,
        },
      ],
    },
  },
  {
    id: "template-004",
    name: "奇幻魔法森林",
    video: {
      thumbnailUrl:
        "https://placehold.co/400x225/8b5cf6/ffffff?text=%E5%A5%87%E5%B9%BB%E9%AD%94%E6%B3%95",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "奇幻",
      resolution: "1080p",
      duration: "3:00",
      description: "魔法森林深处,魔法师与精灵的奇幻冒险",
      keywords: ["魔法", "森林", "精灵", "奇幻"],
      novelPrompt:
        "魔法森林深处,古老的魔法阵闪烁着神秘的光芒。一位穿着紫色法袍的魔法师,手持法杖,口中念念有词。突然,一道耀眼的光柱冲天而起,照亮了整片森林。精灵们纷纷现身,围绕在魔法师周围。",
      aspectRatio: "16:9",
      fileSize: "58.2 MB",
      totalScenes: 11,
      createdAt: "2025-10-23 15:45:00",
      slices: [
        {
          id: "template-004-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "template-004-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:20",
          timeInSeconds: 20,
        },
      ],
    },
  },
  {
    id: "template-005",
    name: "3D卡通冒险",
    video: {
      thumbnailUrl: "https://placehold.co/400x225/f59e0b/ffffff?text=3D%E5%86%92%E9%99%A9",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "3D卡通",
      resolution: "720p",
      duration: "2:15",
      description: "彩虹岛上小兔子的可爱冒险故事",
      keywords: ["卡通", "冒险", "可爱", "童趣"],
      novelPrompt:
        "彩虹岛上,小兔子蹦蹦跳跳地寻找着胡萝卜。它圆圆的眼睛四处张望,长长的耳朵竖得高高的。忽然,它发现了一片胡萝卜地,开心地跳了起来。可是,胡萝卜地被一道篱笆围着,怎么办呢?",
      aspectRatio: "16:9",
      fileSize: "38.5 MB",
      totalScenes: 7,
      createdAt: "2025-10-24 10:30:00",
      slices: [
        {
          id: "template-005-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "template-005-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:18",
          timeInSeconds: 18,
        },
        {
          id: "template-005-slice-3",
          sceneNumber: 3,
          thumbnailUrl:
            "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF3",
          timestamp: "0:36",
          timeInSeconds: 36,
        },
      ],
    },
  },
  {
    id: "template-006",
    name: "赛博朋克未来",
    video: {
      thumbnailUrl:
        "https://placehold.co/400x225/06b6d4/ffffff?text=%E8%B5%9B%E5%8D%9A%E6%9C%AA%E6%9D%A5",
      videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      style: "现代",
      resolution: "4K",
      duration: "3:30",
      description: "2077年赛博都市,黑客与企业的较量",
      keywords: ["科幻", "赛博朋克", "未来", "黑客"],
      novelPrompt:
        "2077年,霓虹灯照亮了这座赛博都市的夜晚,黑客与企业之间的较量永不停歇。高楼大厦之间,数据流如瀑布般倾泻而下,照亮了整个天空。",
      aspectRatio: "16:9",
      fileSize: "95.7 MB",
      totalScenes: 12,
      createdAt: "2025-10-24 16:00:00",
      slices: [
        {
          id: "template-006-slice-1",
          sceneNumber: 1,
          thumbnailUrl:
            "https://placehold.co/160x90/06b6d4/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          timeInSeconds: 0,
        },
        {
          id: "template-006-slice-2",
          sceneNumber: 2,
          thumbnailUrl:
            "https://placehold.co/160x90/06b6d4/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:22",
          timeInSeconds: 22,
        },
      ],
    },
  },
]

export const getVideoTemplates = async (): Promise<
  ApiResponse<VideoTemplate[]>
> => {
  await new Promise((resolve) => setTimeout(resolve, 300))

  return {
    code: 0,
    message: "获取视频模板成功",
    data: mockVideoTemplates,
  }
}

export const generateVideo = async (
  _params: VideoGenerationParams
): Promise<ApiResponse<VideoGenerationResponse>> => {
  await new Promise((resolve) => setTimeout(resolve, 500))

  return {
    code: 0,
    message: "视频生成任务已创建",
    data: {
      taskId: `task-${Date.now()}`,
      status: "pending",
    },
  }
}

export const getVideoStatus = async (
  taskId: string
): Promise<ApiResponse<VideoStatusResponse>> => {
  await new Promise((resolve) => setTimeout(resolve, 300))

  const mockProgress = Math.min(100, Math.floor(Math.random() * 100))
  const isCompleted = mockProgress === 100

  return {
    code: 0,
    message: "获取视频状态成功",
    data: {
      taskId,
      status: isCompleted ? "completed" : "processing",
      progress: mockProgress,
      video: isCompleted
        ? {
            thumbnailUrl:
              "https://placehold.co/400x225/10b981/ffffff?text=%E5%B7%B2%E5%AE%8C%E6%88%90",
            videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
            style: "古风",
            resolution: "1080p",
            duration: "2:30",
            description: "生成的视频",
            keywords: ["生成", "视频"],
            slices: mockVideoSlices,
            novelPrompt: "生成的视频内容...",
            aspectRatio: "16:9",
            fileSize: "45.6 MB",
            totalScenes: 5,
            createdAt: new Date().toISOString(),
          }
        : undefined,
    },
  }
}
