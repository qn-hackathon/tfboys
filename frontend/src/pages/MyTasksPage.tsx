import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Search,
  Play,
  Download,
  Trash2,
  RefreshCw,
  Share2,
} from "lucide-react"
import { getTasks, getTaskStatusText, getTaskStatusVariant, Task } from "@/apis/task"
import { VideoPreviewDialog } from "@/components/VideoPreviewDialog"
import { ShareDialog } from "@/components/ShareDialog"
import { toast } from "sonner"

type FilterStatus = "all" | "in-progress" | "completed" | "failed"

export function MyTasksPage() {
  const [filter, setFilter] = useState<FilterStatus>("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null)
  const [shareDialogOpen, setShareDialogOpen] = useState(false)

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setIsLoading(true)
        const response = await getTasks()
        if (response.code === 0 && response.data) {
          setTasks(response.data)
        } else {
          toast.error(response.message || "获取任务列表失败")
        }
      } catch {
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
    if (task.result) {
      setSelectedTask(task)
    }
  }

  const handleDownload = () => {
    console.log("下载视频")
  }

  const handleDelete = (task: Task) => {
    setTaskToDelete(task)
    setDeleteDialogOpen(true)
  }

  const confirmDelete = () => {
    if (taskToDelete) {
      console.log("删除任务:", taskToDelete.task_id)
      toast.success("任务已删除")
      setDeleteDialogOpen(false)
      setTaskToDelete(null)
    }
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
    setShareDialogOpen(true)
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
                  {task.thumbnail_url && task.status === "completed" && (
                    <div className="w-32 h-24 flex-shrink-0 rounded-lg overflow-hidden bg-muted">
                      <img
                        src={task.thumbnail_url}
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
                          创建时间: {task.created_at}
                        </p>
                      </div>
                      <Badge variant={getTaskStatusVariant(task.status)}>
                        {getStatusIcon(task.status)} {getTaskStatusText(task.status)}
                      </Badge>
                    </div>

                    {task.status !== "completed" && task.status !== "failed" && task.progress && (
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">状态: {task.current_stage}</span>
                          <span className="font-semibold">{Math.floor((task.progress.processed_scenes / task.progress.total_scenes) * 100)}%</span>
                        </div>
                        <Progress value={Math.floor((task.progress.processed_scenes / task.progress.total_scenes) * 100)} className="h-2" />
                        <p className="text-sm text-muted-foreground">
                          已处理: {task.progress.processed_scenes} / {task.progress.total_scenes} 场景
                        </p>
                        {task.estimated_time_remaining && (
                          <p className="text-sm text-muted-foreground">
                            预计剩余时间: {task.estimated_time_remaining}
                          </p>
                        )}
                      </div>
                    )}

                    {task.status === "completed" && task.result && (
                      <div className="mb-4">
                        <p className="text-sm text-muted-foreground">
                          时长: {task.duration} | {task.progress?.total_scenes ?? 0} 个场景 | {task.result.file_size}
                        </p>
                      </div>
                    )}

                    {task.status === "failed" && task.error && (
                      <div className="mb-4">
                        <p className="text-sm text-destructive">
                          错误原因: {task.error}
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
                        <Button variant="outline" onClick={() => handleDelete(task)}>
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
                    <Button variant="outline" onClick={handleShare}>
                      <Share2 className="mr-2 h-4 w-4" />
                      分享
                    </Button>
                    <Button variant="outline" onClick={() => handleDelete(task)}>
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
        video={selectedTask}
        open={!!selectedTask && !shareDialogOpen}
        onOpenChange={() => setSelectedTask(null)}
        onDownload={handleDownload}
        onShare={handleShare}
      />

      <ShareDialog
        open={shareDialogOpen}
        onOpenChange={setShareDialogOpen}
      />

      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>确认删除</DialogTitle>
            <DialogDescription>
              确定要删除任务 "{taskToDelete?.title}" 吗?此操作不可恢复。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>
              取消
            </Button>
            <Button variant="destructive" onClick={confirmDelete}>
              确认删除
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
