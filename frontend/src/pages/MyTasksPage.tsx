import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Search,
  Play,
  Download,
  Trash2,
  RefreshCw,
} from "lucide-react"
import { getTasks, getTaskStatusText, getTaskStatusVariant, Task } from "@/apis/task"
import { Video } from "@/apis/video"
import { VideoPreviewDialog } from "@/components/VideoPreviewDialog"
import { toast } from "sonner"

type FilterStatus = "all" | "in-progress" | "completed" | "failed"

export function MyTasksPage() {
  const [filter, setFilter] = useState<FilterStatus>("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setIsLoading(true)
        const response = await getTasks({ page: 1, page_size: 100 })
        if (response.code === 0 && response.data) {
          setTasks(response.data.tasks)
        } else {
          toast.error(response.message || "获取任务列表失败")
        }
      } catch (error) {
        toast.error("获取任务列表时发生错误")
      } finally {
        setIsLoading(false)
      }
    }

    fetchTasks()
  }, [])

  const filteredTasks = tasks.filter((task) => {
    if (filter === "in-progress") {
      return ["pending", "analyzing", "generating_images", "generating_audio", "synthesizing_video"].includes(task.status)
    }
    if (filter === "completed") {
      return task.status === "completed"
    }
    if (filter === "failed") {
      return task.status === "failed"
    }
    return true
  }).filter((task) => {
    if (!searchQuery) return true
    return task.title?.toLowerCase().includes(searchQuery.toLowerCase())
  })

  const handlePreview = (task: Task) => {
    if (task.video) {
      setSelectedVideo(task.video)
    }
  }

  const handleDownload = () => {
    console.log("下载视频")
  }

  const handleDelete = () => {
    console.log("删除视频")
  }

  const handleRetry = (task: Task) => {
    console.log("重试任务:", task.task_id)
  }

  const handleCancel = (task: Task) => {
    console.log("取消任务:", task.task_id)
  }

  const handleViewDetails = (task: Task) => {
    console.log("查看详情:", task.task_id)
  }

  const handleShare = () => {
    console.log("分享视频")
  }


  const getStatusIcon = (status: Task["status"]) => {
    if (status === "completed") return "✅"
    if (status === "failed") return "❌"
    return "🔄"
  }

  const inProgressCount = tasks.filter((task) =>
    ["pending", "analyzing", "generating_images", "generating_audio", "synthesizing_video"].includes(task.status)
  ).length

  return (
    <div className="h-full p-6 overflow-auto">
      <div className="max-w-[1400px] mx-auto">
        <h1 className="text-3xl font-bold mb-6">📋 我的任务</h1>

        <div className="flex items-center justify-between mb-6">
          <Tabs value={filter} onValueChange={(v) => setFilter(v as FilterStatus)}>
            <TabsList>
              <TabsTrigger value="all">全部</TabsTrigger>
              <TabsTrigger value="in-progress">
                进行中
                {inProgressCount > 0 && (
                  <Badge variant="destructive" className="ml-2 px-1.5 py-0 h-5 min-w-5 rounded-full text-xs">
                    {inProgressCount}
                  </Badge>
                )}
              </TabsTrigger>
              <TabsTrigger value="completed">已完成</TabsTrigger>
              <TabsTrigger value="failed">失败</TabsTrigger>
            </TabsList>
          </Tabs>

          <div className="relative w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="搜索任务..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        <div className="space-y-4">
          {isLoading ? (
            <Card className="p-12">
              <div className="text-center text-muted-foreground">
                <p>加载中...</p>
              </div>
            </Card>
          ) : filteredTasks.length === 0 ? (
            <Card className="p-12">
              <div className="text-center text-muted-foreground">
                <p>暂无任务</p>
              </div>
            </Card>
          ) : (
            filteredTasks.map((task) => (
              <Card key={task.task_id} className="p-6">
                <div className="flex items-start gap-4">
                  {task.video?.thumbnailUrl && task.status === "completed" && (
                    <div className="w-32 h-24 flex-shrink-0 rounded-lg overflow-hidden bg-muted">
                      <img
                        src={task.video.thumbnailUrl}
                        alt={task.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}

                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-semibold mb-1">
                          任务 #{task.task_id.split("-")[1]}: {task.title}
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          创建时间: {new Date(task.created_at).toLocaleString('zh-CN')}
                        </p>
                      </div>
                      <Badge variant={getTaskStatusVariant(task.status)}>
                        {getStatusIcon(task.status)} {getTaskStatusText(task.status)}
                      </Badge>
                    </div>

                    {task.status !== "completed" && task.status !== "failed" && task.progress && (
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">
                            状态: {task.progress.current_stage ? getTaskStatusText(task.progress.current_stage as any) : getTaskStatusText(task.status)}
                          </span>
                          <span className="font-semibold">{task.progress.percentage}%</span>
                        </div>
                        <Progress value={task.progress.percentage} className="h-2" />
                        {task.progress.processed_scenes && task.progress.total_scenes && (
                          <p className="text-sm text-muted-foreground">
                            已处理: {task.progress.processed_scenes} / {task.progress.total_scenes} 场景
                          </p>
                        )}
                      </div>
                    )}

                    {task.status === "completed" && task.video && (
                      <div className="mb-4">
                        <p className="text-sm text-muted-foreground">
                          时长: {task.video.duration} | {task.video.totalScenes} 个场景 | {task.video.fileSize}
                        </p>
                      </div>
                    )}

                    {task.status === "failed" && task.error && (
                      <div className="mb-4">
                        <p className="text-sm text-destructive">
                          错误原因: {task.error.message}
                        </p>
                      </div>
                    )}

                    {!["completed", "failed"].includes(task.status) && (
                      <div className="flex gap-2">
                        <Button variant="outline" onClick={() => handleViewDetails(task)}>
                          查看详情
                        </Button>
                        <Button variant="outline" onClick={() => handleCancel(task)}>
                          取消任务
                        </Button>
                      </div>
                    )}

                    {task.status === "failed" && (
                      <div className="flex gap-2">
                        <Button onClick={() => handleRetry(task)}>
                          <RefreshCw className="mr-2 h-4 w-4" />
                          重试
                        </Button>
                        <Button variant="outline" onClick={handleDelete}>
                          <Trash2 className="mr-2 h-4 w-4" />
                          删除
                        </Button>
                      </div>
                    )}
                  </div>
                </div>

                {task.status === "completed" && (
                  <div className="flex gap-2 mt-4">
                    <Button onClick={() => handlePreview(task)}>
                      <Play className="mr-2 h-4 w-4" />
                      预览
                    </Button>
                    <Button variant="outline" onClick={handleDownload}>
                      <Download className="mr-2 h-4 w-4" />
                      下载
                    </Button>
                    <Button variant="outline" onClick={handleDelete}>
                      <Trash2 className="mr-2 h-4 w-4" />
                      删除
                    </Button>
                  </div>
                )}
              </Card>
            ))
          )}
        </div>

        {filteredTasks.length > 0 && (
          <div className="flex items-center justify-center gap-4 mt-6">
            <Button variant="outline" size="sm" disabled>
              ← 上一页
            </Button>
            <span className="text-sm text-muted-foreground">1 / 1</span>
            <Button variant="outline" size="sm" disabled>
              下一页 →
            </Button>
          </div>
        )}
      </div>

      <VideoPreviewDialog
        video={selectedVideo}
        open={!!selectedVideo}
        onOpenChange={() => setSelectedVideo(null)}
        onDownload={handleDownload}
        onShare={handleShare}
        onDelete={handleDelete}
      />
    </div>
  )
}
