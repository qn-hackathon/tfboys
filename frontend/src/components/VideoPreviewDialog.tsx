import { useRef } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Download, Share2, Trash2, Clock, Monitor, Maximize, Film, HardDrive } from "lucide-react"
import { Task, mockVideoSlices } from "@/data/mockData"
import { VideoSliceCarousel } from "@/components/VideoSliceCarousel"

interface VideoPreviewDialogProps {
  task: Task | null
  open: boolean
  onOpenChange: (open: boolean) => void
  onDownload: (task: Task) => void
  onShare: () => void
  onDelete: (task: Task) => void
}

export function VideoPreviewDialog({
  task,
  open,
  onOpenChange,
  onDownload,
  onShare,
  onDelete,
}: VideoPreviewDialogProps) {
  const videoRef = useRef<HTMLVideoElement>(null)

  const handleSliceClick = (timeInSeconds: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = timeInSeconds
      videoRef.current.play()
    }
  }

  if (!task) return null

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-6xl h-[85vh] p-0">
        <DialogHeader className="sr-only">
          <DialogTitle>视频预览</DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full px-[3.5em] py-6 overflow-y-auto">
          <div className="lg:col-span-2 flex flex-col gap-4 min-h-0">
            <div className="aspect-video bg-black rounded-lg overflow-hidden flex-shrink-0">
              <video
                ref={videoRef}
                src={task.videoUrl}
                controls
                className="w-full h-full"
              >
                您的浏览器不支持视频播放
              </video>
            </div>

            <div className="flex justify-end gap-2">
              <Button variant="ghost" size="icon" onClick={() => onDownload(task)}>
                <Download className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" onClick={onShare}>
                <Share2 className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" onClick={() => onDelete(task)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>

            <div className="flex-1 min-h-0">
              <VideoSliceCarousel
                slices={mockVideoSlices}
                onSliceClick={handleSliceClick}
              />
            </div>
          </div>

          <div className="flex flex-col gap-4 overflow-y-auto">
            <div>
              <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                📄 小说 Prompt
              </h3>
              <Card className="p-4 min-h-[160px]">
                <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                  {task.novelPrompt}
                </p>
              </Card>
            </div>

            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Clock className="h-4 w-4 flex-shrink-0" />
                <span>时长: {task.duration}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <Monitor className="h-4 w-4 flex-shrink-0" />
                <span>分辨率: {task.resolution}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <Maximize className="h-4 w-4 flex-shrink-0" />
                <span>视频横纵比: {task.aspectRatio}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <Film className="h-4 w-4 flex-shrink-0" />
                <span>场景数: {task.totalScenes}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <HardDrive className="h-4 w-4 flex-shrink-0" />
                <span>文件大小: {task.fileSize}</span>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
