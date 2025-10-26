import { httpClient, ApiResponse } from "./http"

export interface VideoSlice {
  id: string
  scene_number: number
  thumbnail_url: string
  timestamp: string
  time_in_seconds: number
}

export type TaskStatus =
  | "pending"
  | "analyzing"
  | "generating_images"
  | "generating_audio"
  | "synthesizing_video"
  | "completed"
  | "failed"

export interface TaskProgress {
  total_scenes: number
  processed_scenes: number
}

export interface TaskResult {
  video_url: string
  aspect_ratio: string
  file_size: string
}

export interface Task {
  task_id: string
  status: TaskStatus
  novel_text: string
  created_at: string
  progress: TaskProgress
  current_stage: string
  result?: TaskResult
  error?: string
  style?: "古风" | "现代" | "动漫" | "奇幻" | "3D卡通"
  resolution?: "1080p" | "720p" | "4K"
  duration?: string
  description?: string
  keywords?: string[]
  slices?: VideoSlice[]
  thumbnail_url?: string
  title?: string
  estimated_time_remaining?: string
}

export interface TaskTemplate {
  id: string
  name: string
  task: Task
}

export interface CreateTaskParams {
  novel_text: string
  style?: string
}

export interface CreateTaskResponse {
  task_id: string
}

const mockVideoSlices: VideoSlice[] = [
  {
    id: "slice-1",
    scene_number: 1,
    thumbnail_url: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+1",
    timestamp: "0:00",
    time_in_seconds: 0,
  },
  {
    id: "slice-2",
    scene_number: 2,
    thumbnail_url: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+2",
    timestamp: "0:15",
    time_in_seconds: 15,
  },
  {
    id: "slice-3",
    scene_number: 3,
    thumbnail_url: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+3",
    timestamp: "0:30",
    time_in_seconds: 30,
  },
  {
    id: "slice-4",
    scene_number: 4,
    thumbnail_url: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+4",
    timestamp: "0:45",
    time_in_seconds: 45,
  },
  {
    id: "slice-5",
    scene_number: 5,
    thumbnail_url: "https://placehold.co/160x90/3b82f6/ffffff?text=Scene+5",
    timestamp: "1:00",
    time_in_seconds: 60,
  },
]

const mockTaskTemplates: TaskTemplate[] = [
  {
    id: "template-001",
    name: "古风江湖夜行",
    task: {
      task_id: "template-001-task",
      status: "completed",
      novel_text:
        "月光如水,洒在青石板铺就的小巷。一位白衣少年手持长剑,眉目如画。他缓缓走过,衣袂飘飘,宛如谪仙。忽然,一阵琴音从远处传来,婉转悠扬。",
      created_at: "2025-10-20 14:30:00",
      progress: {
        total_scenes: 8,
        processed_scenes: 8,
      },
      current_stage: "已完成",
      result: {
        video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
        aspect_ratio: "16:9",
        file_size: "52.3 MB",
      },
      style: "古风",
      resolution: "1080p",
      duration: "2:45",
      description: "月光下的江湖侠客,行走于青石板街道,展现古典武侠之美",
      keywords: ["侠客", "月夜", "武侠", "古典"],
      slices: [
        {
          id: "template-001-slice-1",
          scene_number: 1,
          thumbnail_url:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          time_in_seconds: 0,
        },
        {
          id: "template-001-slice-2",
          scene_number: 2,
          thumbnail_url:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:20",
          time_in_seconds: 20,
        },
        {
          id: "template-001-slice-3",
          scene_number: 3,
          thumbnail_url:
            "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF3",
          timestamp: "0:40",
          time_in_seconds: 40,
        },
      ],
      thumbnail_url:
        "https://placehold.co/400x225/10b981/ffffff?text=%E5%8F%A4%E9%A3%8E%E6%B1%9F%E6%B9%96",
    },
  },
  {
    id: "template-002",
    name: "现代都市夜景",
    task: {
      task_id: "template-002-task",
      status: "completed",
      novel_text:
        "都市的夜晚灯火通明,摩天大楼林立。一个年轻人背着双肩包,匆匆走在人潮涌动的街头。他抬头看向天空,高楼之间只能看到一小片星空。",
      created_at: "2025-10-21 09:15:00",
      progress: {
        total_scenes: 10,
        processed_scenes: 10,
      },
      current_stage: "已完成",
      result: {
        video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
        aspect_ratio: "16:9",
        file_size: "89.5 MB",
      },
      style: "现代",
      resolution: "4K",
      duration: "3:12",
      description: "繁华都市的霓虹灯下,讲述现代人的故事",
      keywords: ["都市", "霓虹", "现代", "夜景"],
      slices: [
        {
          id: "template-002-slice-1",
          scene_number: 1,
          thumbnail_url:
            "https://placehold.co/160x90/3b82f6/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          time_in_seconds: 0,
        },
        {
          id: "template-002-slice-2",
          scene_number: 2,
          thumbnail_url:
            "https://placehold.co/160x90/3b82f6/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:25",
          time_in_seconds: 25,
        },
      ],
      thumbnail_url:
        "https://placehold.co/400x225/3b82f6/ffffff?text=%E7%8E%B0%E4%BB%A3%E9%83%BD%E5%B8%82",
    },
  },
  {
    id: "template-003",
    name: "动漫校园物语",
    task: {
      task_id: "template-003-task",
      status: "completed",
      novel_text:
        "樱花飘落的季节,校园里传来欢快的笑声。一个扎着双马尾的少女,抱着一摞书本跑过走廊。突然,她脚下一滑,书本散落一地。正当她手忙脚乱时,一只温暖的手伸了过来。",
      created_at: "2025-10-22 11:20:00",
      progress: {
        total_scenes: 9,
        processed_scenes: 9,
      },
      current_stage: "已完成",
      result: {
        video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
        aspect_ratio: "16:9",
        file_size: "45.8 MB",
      },
      style: "动漫",
      resolution: "1080p",
      duration: "2:30",
      description: "樱花飘落的校园,少女们的青春物语",
      keywords: ["校园", "樱花", "青春", "动漫"],
      slices: [
        {
          id: "template-003-slice-1",
          scene_number: 1,
          thumbnail_url:
            "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          time_in_seconds: 0,
        },
        {
          id: "template-003-slice-2",
          scene_number: 2,
          thumbnail_url:
            "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:18",
          time_in_seconds: 18,
        },
        {
          id: "template-003-slice-3",
          scene_number: 3,
          thumbnail_url:
            "https://placehold.co/160x90/ec4899/ffffff?text=%E5%9C%BA%E6%99%AF3",
          timestamp: "0:36",
          time_in_seconds: 36,
        },
      ],
      thumbnail_url:
        "https://placehold.co/400x225/ec4899/ffffff?text=%E5%8A%A8%E6%BC%AB%E6%A0%A1%E5%9B%AD",
    },
  },
  {
    id: "template-004",
    name: "奇幻魔法森林",
    task: {
      task_id: "template-004-task",
      status: "completed",
      novel_text:
        "魔法森林深处,古老的魔法阵闪烁着神秘的光芒。一位穿着紫色法袍的魔法师,手持法杖,口中念念有词。突然,一道耀眼的光柱冲天而起,照亮了整片森林。精灵们纷纷现身,围绕在魔法师周围。",
      created_at: "2025-10-23 15:45:00",
      progress: {
        total_scenes: 11,
        processed_scenes: 11,
      },
      current_stage: "已完成",
      result: {
        video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
        aspect_ratio: "16:9",
        file_size: "58.2 MB",
      },
      style: "奇幻",
      resolution: "1080p",
      duration: "3:00",
      description: "魔法森林深处,魔法师与精灵的奇幻冒险",
      keywords: ["魔法", "森林", "精灵", "奇幻"],
      slices: [
        {
          id: "template-004-slice-1",
          scene_number: 1,
          thumbnail_url:
            "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          time_in_seconds: 0,
        },
        {
          id: "template-004-slice-2",
          scene_number: 2,
          thumbnail_url:
            "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:20",
          time_in_seconds: 20,
        },
      ],
      thumbnail_url:
        "https://placehold.co/400x225/8b5cf6/ffffff?text=%E5%A5%87%E5%B9%BB%E9%AD%94%E6%B3%95",
    },
  },
  {
    id: "template-005",
    name: "3D卡通冒险",
    task: {
      task_id: "template-005-task",
      status: "completed",
      novel_text:
        "彩虹岛上,小兔子蹦蹦跳跳地寻找着胡萝卜。它圆圆的眼睛四处张望,长长的耳朵竖得高高的。忽然,它发现了一片胡萝卜地,开心地跳了起来。可是,胡萝卜地被一道篱笆围着,怎么办呢?",
      created_at: "2025-10-24 10:30:00",
      progress: {
        total_scenes: 7,
        processed_scenes: 7,
      },
      current_stage: "已完成",
      result: {
        video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
        aspect_ratio: "16:9",
        file_size: "38.5 MB",
      },
      style: "3D卡通",
      resolution: "720p",
      duration: "2:15",
      description: "彩虹岛上小兔子的可爱冒险故事",
      keywords: ["卡通", "冒险", "可爱", "童趣"],
      slices: [
        {
          id: "template-005-slice-1",
          scene_number: 1,
          thumbnail_url:
            "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          time_in_seconds: 0,
        },
        {
          id: "template-005-slice-2",
          scene_number: 2,
          thumbnail_url:
            "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:18",
          time_in_seconds: 18,
        },
        {
          id: "template-005-slice-3",
          scene_number: 3,
          thumbnail_url:
            "https://placehold.co/160x90/f59e0b/ffffff?text=%E5%9C%BA%E6%99%AF3",
          timestamp: "0:36",
          time_in_seconds: 36,
        },
      ],
      thumbnail_url: "https://placehold.co/400x225/f59e0b/ffffff?text=3D%E5%86%92%E9%99%A9",
    },
  },
  {
    id: "template-006",
    name: "赛博朋克未来",
    task: {
      task_id: "template-006-task",
      status: "completed",
      novel_text:
        "2077年,霓虹灯照亮了这座赛博都市的夜晚,黑客与企业之间的较量永不停歇。高楼大厦之间,数据流如瀑布般倾泻而下,照亮了整个天空。",
      created_at: "2025-10-24 16:00:00",
      progress: {
        total_scenes: 12,
        processed_scenes: 12,
      },
      current_stage: "已完成",
      result: {
        video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
        aspect_ratio: "16:9",
        file_size: "95.7 MB",
      },
      style: "现代",
      resolution: "4K",
      duration: "3:30",
      description: "2077年赛博都市,黑客与企业的较量",
      keywords: ["科幻", "赛博朋克", "未来", "黑客"],
      slices: [
        {
          id: "template-006-slice-1",
          scene_number: 1,
          thumbnail_url:
            "https://placehold.co/160x90/06b6d4/ffffff?text=%E5%9C%BA%E6%99%AF1",
          timestamp: "0:00",
          time_in_seconds: 0,
        },
        {
          id: "template-006-slice-2",
          scene_number: 2,
          thumbnail_url:
            "https://placehold.co/160x90/06b6d4/ffffff?text=%E5%9C%BA%E6%99%AF2",
          timestamp: "0:22",
          time_in_seconds: 22,
        },
      ],
      thumbnail_url:
        "https://placehold.co/400x225/06b6d4/ffffff?text=%E8%B5%9B%E5%8D%9A%E6%9C%AA%E6%9D%A5",
    },
  },
]

const mockTasks: Task[] = [
  {
    task_id: "task-001",
    status: "generating_images",
    novel_text: "春天的故事...",
    created_at: "2025-10-25 10:30:00",
    progress: {
      total_scenes: 10,
      processed_scenes: 6,
    },
    current_stage: "图像生成中",
    title: "春天的故事...",
    estimated_time_remaining: "2 分钟",
  },
  {
    task_id: "task-002",
    status: "completed",
    novel_text: "一个关于少年与猫的温馨故事,讲述了他们之间的深厚情谊和成长经历...",
    created_at: "2025-10-23 14:30:00",
    progress: {
      total_scenes: 10,
      processed_scenes: 10,
    },
    current_stage: "已完成",
    result: {
      video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
      aspect_ratio: "16:9",
      file_size: "45.6 MB",
    },
    style: "古风",
    resolution: "1080p",
    duration: "2:30",
    description: "一个关于少年与猫的温馨故事",
    keywords: ["温馨", "友谊", "成长"],
    slices: [
      {
        id: "task-002-slice-1",
        scene_number: 1,
        thumbnail_url:
          "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        time_in_seconds: 0,
      },
      {
        id: "task-002-slice-2",
        scene_number: 2,
        thumbnail_url:
          "https://placehold.co/160x90/10b981/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:15",
        time_in_seconds: 15,
      },
    ],
    thumbnail_url:
      "https://placehold.co/160x120/10b981/ffffff?text=%E5%B7%B2%E5%AE%8C%E6%88%90",
    title: "少年与猫...",
  },
  {
    task_id: "task-003",
    status: "failed",
    novel_text: "星际旅行...",
    created_at: "2025-10-23 12:15:00",
    progress: {
      total_scenes: 10,
      processed_scenes: 4,
    },
    current_stage: "失败",
    error: "图像生成 API 限流,请稍后重试",
    title: "星际旅行...",
  },
  {
    task_id: "task-004",
    status: "completed",
    novel_text: "江湖侠客,快意恩仇。一段关于武林侠客的传奇故事...",
    created_at: "2025-10-22 16:20:00",
    progress: {
      total_scenes: 12,
      processed_scenes: 12,
    },
    current_stage: "已完成",
    result: {
      video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
      aspect_ratio: "16:9",
      file_size: "62.3 MB",
    },
    style: "古风",
    resolution: "1080p",
    duration: "3:15",
    description: "江湖侠客的传奇故事",
    keywords: ["武侠", "江湖", "侠客"],
    slices: [
      {
        id: "task-004-slice-1",
        scene_number: 1,
        thumbnail_url:
          "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF1",
        timestamp: "0:00",
        time_in_seconds: 0,
      },
      {
        id: "task-004-slice-2",
        scene_number: 2,
        thumbnail_url:
          "https://placehold.co/160x90/8b5cf6/ffffff?text=%E5%9C%BA%E6%99%AF2",
        timestamp: "0:20",
        time_in_seconds: 20,
      },
    ],
    thumbnail_url:
      "https://placehold.co/160x120/8b5cf6/ffffff?text=%E5%8F%A4%E9%A3%8E",
    title: "古风江湖侠客传...",
  },
  {
    task_id: "task-005",
    status: "analyzing",
    novel_text: "未来都市赛博朋克...",
    created_at: "2025-10-25 11:00:00",
    progress: {
      total_scenes: 0,
      processed_scenes: 0,
    },
    current_stage: "文本分析中",
    title: "未来都市赛博朋克...",
  },
]

export const getTaskTemplates = async (): Promise<
  ApiResponse<TaskTemplate[]>
> => {
  await new Promise((resolve) => setTimeout(resolve, 300))

  return {
    code: 0,
    message: "获取任务模板成功",
    data: mockTaskTemplates,
  }
}

export const createTask = async (
  params: CreateTaskParams
): Promise<ApiResponse<CreateTaskResponse>> => {
  return httpClient.post<CreateTaskResponse>("/tasks", params)
}

export const getTaskStatus = async (
  task_id: string
): Promise<ApiResponse<Task>> => {
  return httpClient.get<Task>(`/tasks/${task_id}`)
}

export const getTasks = async (): Promise<ApiResponse<Task[]>> => {
  return httpClient.get<Task[]>("/tasks")
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
