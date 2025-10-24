export interface Task {
  task_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  novel_text: string
  created_at: string
  progress?: {
    total_scenes: number
    processed_scenes: number
  }
  result?: {
    video_url: string
  }
  error?: string
}

export interface CreateTaskRequest {
  novel_text: string
}

export interface CreateTaskResponse {
  task_id: string
  status: string
}
