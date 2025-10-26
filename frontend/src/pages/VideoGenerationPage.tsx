import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import { Input } from "@/components/ui/input"
import { Upload, Link as LinkIcon, Play, Download, Share2, RefreshCw, Check } from "lucide-react"
import { getTaskTemplates, createTask, getTaskStatus, type VideoSlice, type TaskTemplate, type Task } from "@/apis/task"
import { VideoSliceCarousel } from "@/components/VideoSliceCarousel"
import { ShareDialog } from "@/components/ShareDialog"
import { toast } from "sonner"

type VideoStyle = "古风" | "现代" | "动漫" | "奇幻" | "3D卡通"
type Resolution = "1080p" | "720p"
type GenerationStatus = "idle" | "generating" | "completed" | "failed"

const VIDEO_STYLES: { id: VideoStyle; icon: string; label: string }[] = [
  { id: "古风", icon: "🏮", label: "古风" },
  { id: "现代", icon: "🏙️", label: "现代" },
  { id: "动漫", icon: "🎨", label: "动漫" },
  { id: "奇幻", icon: "✨", label: "奇幻" },
  { id: "3D卡通", icon: "🎭", label: "3D卡通" },
]

const MAX_CHARS = 10000
const RECOMMENDED_MIN = 500
const RECOMMENDED_MAX = 5000

export function VideoGenerationPage() {
  const [inputMethod, setInputMethod] = useState<"text" | "file" | "url">("text")
  const [novelText, setNovelText] = useState("")
  const [urlInput, setUrlInput] = useState("")
  const [selectedStyle, setSelectedStyle] = useState<VideoStyle>("古风")
  const [resolution, setResolution] = useState<Resolution>("1080p")
  const [status, setStatus] = useState<GenerationStatus>("idle")
  const [progress, setProgress] = useState(0)
  const [statusText, setStatusText] = useState("")
  const [shareDialogOpen, setShareDialogOpen] = useState(false)
  const [videoSlices, setVideoSlices] = useState<VideoSlice[]>([])
  const [templateTasks, setTemplateTasks] = useState<TaskTemplate[]>([])
  const [generatedVideoUrl, setGeneratedVideoUrl] = useState<string>("")
  const [currentTask, setCurrentTask] = useState<Task | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const templatesResponse = await getTaskTemplates()

        if (templatesResponse.code === 0 && templatesResponse.data) {
          setTemplateTasks(templatesResponse.data)
          if (templatesResponse.data.length > 0 && templatesResponse.data[0].task.slices) {
            setVideoSlices(templatesResponse.data[0].task.slices)
            setGeneratedVideoUrl(templatesResponse.data[0].task.result?.video_url || "")
          }
        } else {
          toast.error(templatesResponse.message || "获取视频模板失败")
        }
      } catch {
        toast.error("加载数据时发生错误")
      }
    }

    fetchData()
  }, [])

  const charCount = novelText.length
  const isOverLimit = charCount > MAX_CHARS
  const estimatedTime = Math.ceil(charCount / 200)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type === "text/plain") {
      const reader = new FileReader()
      reader.onload = (event) => {
        const text = event.target?.result as string
        setNovelText(text)
      }
      reader.readAsText(file)
    }
  }

  const handleUrlFetch = () => {
    // TODO: 实现 URL 抓取功能
    console.log("抓取 URL:", urlInput)
  }

  const handleGenerate = async () => {
    if (!novelText || isOverLimit) return

    setStatus("generating")
    setProgress(0)
    setStatusText("正在创建任务...")

    try {
      const response = await createTask({
        novel_text: novelText,
        style: selectedStyle,
      })

      if (response.code === 0 && response.data?.task_id) {
        const taskId = response.data.task_id
        toast.success("任务创建成功,开始生成...")
        
        startPolling(taskId)
      } else {
        toast.error(response.message || "任务创建失败")
        setStatus("failed")
      }
    } catch (error) {
      console.error("创建任务失败:", error)
      toast.error("任务创建失败")
      setStatus("failed")
    }
  }

  const startPolling = (taskId: string) => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current)
    }

    const pollTaskStatus = async () => {
      try {
        const response = await getTaskStatus(taskId)
        
        if (response.code === 0 && response.data) {
          const task = response.data
          setCurrentTask(task)

          const totalScenes = task.progress?.total_scenes || 1
          const processedScenes = task.progress?.processed_scenes || 0
          const progressPercent = Math.floor((processedScenes / totalScenes) * 100)
          
          setProgress(progressPercent)
          setStatusText(task.current_stage || "处理中...")

          if (task.status === "completed") {
            if (pollingIntervalRef.current) {
              clearInterval(pollingIntervalRef.current)
            }
            setStatus("completed")
            if (task.result?.video_url) {
              setGeneratedVideoUrl(task.result.video_url)
            }
            if (task.slices) {
              setVideoSlices(task.slices)
            }
            toast.success("视频生成完成!")
          } else if (task.status === "failed") {
            if (pollingIntervalRef.current) {
              clearInterval(pollingIntervalRef.current)
            }
            setStatus("failed")
            toast.error(task.error || "视频生成失败")
          }
        }
      } catch (error) {
        console.error("轮询任务状态失败:", error)
      }
    }

    pollTaskStatus()
    pollingIntervalRef.current = setInterval(pollTaskStatus, 3000)
  }

  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current)
      }
    }
  }, [])

  const handleRegenerate = () => {
    // TODO: 实现重新生成功能
    console.log("重新生成视频")
    handleGenerate()
  }

  const handleDownload = () => {
    console.log("下载视频:", generatedVideoUrl)
    toast.success("开始下载视频")
  }

  const handleShare = () => {
    setShareDialogOpen(true)
  }

  const handleSliceClick = (timeInSeconds: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = timeInSeconds
      videoRef.current.play()
    }
  }

  const handleTemplateClick = (templateId: string) => {
    const template = templateTasks.find(t => t.id === templateId)
    if (template) {
      setNovelText(template.task.novel_text)
      setSelectedStyle(template.task.style as VideoStyle)
      setResolution(template.task.resolution as Resolution)
      setVideoSlices(template.task.slices || [])
      setStatus("completed")
      toast.success(`已应用模板: ${template.name}`)
    }
  }

  return (
    <div className="h-full p-6 overflow-auto">
      <div className="max-w-[1400px] mx-auto">
        <h1 className="text-3xl font-bold mb-6">📹 视频生成</h1>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {/* 左侧：输入与配置区域 */}
          <div className="lg:col-span-2 space-y-6">
            {/* 输入小说内容 */}
            <Card className="p-6">
              <h2 className="text-lg font-semibold mb-4">📝 输入小说内容</h2>

              <Tabs value={inputMethod} onValueChange={(v) => setInputMethod(v as typeof inputMethod)}>
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="text">直接输入</TabsTrigger>
                  <TabsTrigger value="file">上传文件</TabsTrigger>
                  <TabsTrigger value="url">粘贴 URL</TabsTrigger>
                </TabsList>

                <TabsContent value="text" className="space-y-4">
                  <Textarea
                    placeholder="在这里输入或粘贴小说内容..."
                    value={novelText}
                    onChange={(e) => setNovelText(e.target.value)}
                    className="min-h-[200px] resize-none"
                  />
                </TabsContent>

                <TabsContent value="file" className="space-y-4">
                  <div className="border-2 border-dashed rounded-lg p-8 text-center">
                    <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                    <Label htmlFor="file-upload" className="cursor-pointer">
                      <span className="text-primary hover:underline">点击上传</span>
                      <span className="text-muted-foreground"> 或拖拽 .txt 文件到此处</span>
                    </Label>
                    <Input
                      id="file-upload"
                      type="file"
                      accept=".txt"
                      className="hidden"
                      onChange={handleFileUpload}
                    />
                  </div>
                  <Textarea
                    placeholder="输入关键章节或者页码"
                    value={novelText}
                    onChange={(e) => setNovelText(e.target.value)}
                    className="min-h-[120px] resize-none"
                  />
                </TabsContent>

                <TabsContent value="url" className="space-y-4">
                  <div className="flex gap-2">
                    <div className="flex-1">
                      <Input
                        placeholder="粘贴小说网站 URL"
                        value={urlInput}
                        onChange={(e) => setUrlInput(e.target.value)}
                      />
                    </div>
                    <Button onClick={handleUrlFetch} variant="outline">
                      <LinkIcon className="mr-2 h-4 w-4" />
                      抓取
                    </Button>
                  </div>
                  <Textarea
                    placeholder="输入关键章节或者页码"
                    value={novelText}
                    onChange={(e) => setNovelText(e.target.value)}
                    className="min-h-[120px] resize-none"
                  />
                </TabsContent>
              </Tabs>

              <div className="mt-4 flex items-center justify-between">
                <div className="text-sm">
                  <span className={isOverLimit ? "text-destructive font-semibold" : "text-muted-foreground"}>
                    字数: {charCount} / {MAX_CHARS} 字
                  </span>
                </div>
                {charCount > 0 && charCount < RECOMMENDED_MIN && (
                  <Badge variant="outline" className="text-xs">
                    💡 建议 {RECOMMENDED_MIN}-{RECOMMENDED_MAX} 字
                  </Badge>
                )}
              </div>
            </Card>

            {/* 配置视频参数 */}
            <Card className="p-6">
              <h2 className="text-lg font-semibold mb-4">🎨 配置视频参数</h2>

              <div className="space-y-6">
                {/* 视频风格 */}
                <div>
                  <Label className="text-base mb-3 block">视频风格</Label>
                  <div className="grid grid-cols-5 gap-2">
                    {VIDEO_STYLES.map((style) => (
                      <button
                        key={style.id}
                        onClick={() => setSelectedStyle(style.id)}
                        className={`
                          relative p-3 rounded-lg border-2 transition-all
                          ${
                            selectedStyle === style.id
                              ? "border-primary bg-primary/5"
                              : "border-border hover:border-primary/50"
                          }
                        `}
                      >
                        <div className="text-2xl mb-1">{style.icon}</div>
                        <div className="text-xs">{style.label}</div>
                        {selectedStyle === style.id && (
                          <Check className="absolute top-1 right-1 h-4 w-4 text-primary" />
                        )}
                      </button>
                    ))}
                  </div>
                </div>

                {/* 视频分辨率 */}
                <div>
                  <Label className="text-base mb-3 block">视频分辨率</Label>
                  <RadioGroup value={resolution} onValueChange={(v) => setResolution(v as Resolution)}>
                    <div className="flex gap-6">
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem value="1080p" id="res-1080p" />
                        <Label htmlFor="res-1080p" className="cursor-pointer">
                          1080p (高清)
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem value="720p" id="res-720p" />
                        <Label htmlFor="res-720p" className="cursor-pointer">
                          720p (快速)
                        </Label>
                      </div>
                    </div>
                  </RadioGroup>
                </div>

                {/* 预计生成时间 */}
                {charCount > 0 && (
                  <div className="pt-2 border-t">
                    <div className="text-sm text-muted-foreground">
                      ⏱️ 预计生成时间: 约 {estimatedTime} 分钟
                    </div>
                  </div>
                )}
              </div>
            </Card>

            {/* 生成按钮 */}
            <Button
              size="lg"
              className="w-full"
              onClick={handleGenerate}
              disabled={!novelText || isOverLimit || status === "generating"}
            >
              {status === "generating" ? "生成中..." : "生成视频"}
            </Button>
          </div>

          {/* 右侧：预览与展示区域 */}
          <div className="lg:col-span-3 space-y-6">
            {/* 视频预览播放器 */}
            <Card className="p-6">
              <div className="aspect-video bg-black rounded-lg overflow-hidden mb-4 flex items-center justify-center">
                {status === "completed" ? (
                  <video
                    ref={videoRef}
                    src={generatedVideoUrl}
                    controls
                    className="w-full h-full"
                  >
                    您的浏览器不支持视频播放
                  </video>
                ) : (
                  <div className="text-white/60 flex flex-col items-center gap-4">
                    <Play className="h-16 w-16" />
                    <p className="text-sm">视频预览区域</p>
                  </div>
                )}
              </div>

              {/* 生成进度 */}
              {status === "generating" && (
                <div className="mb-4 space-y-2">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-muted-foreground">生成进度:</span>
                    <span className="font-semibold">{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                  <p className="text-sm text-muted-foreground">状态: {statusText}</p>
                </div>
              )}

              {/* 操作按钮组 */}
              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={handleRegenerate}
                  disabled={status !== "completed"}
                  className="flex-1"
                >
                  <RefreshCw className="mr-2 h-4 w-4" />
                  重新生成
                </Button>
                <Button onClick={handleDownload} disabled={status !== "completed"} className="flex-1">
                  <Download className="mr-2 h-4 w-4" />
                  下载视频
                </Button>
                <Button
                  variant="outline"
                  onClick={handleShare}
                  disabled={status !== "completed"}
                  className="flex-1"
                >
                  <Share2 className="mr-2 h-4 w-4" />
                  分享视频
                </Button>
              </div>
            </Card>

            {/* 视频切片 */}
            {status === "completed" && (
              <Card className="p-6">
                <VideoSliceCarousel
                  slices={videoSlices}
                  onSliceClick={handleSliceClick}
                />
              </Card>
            )}

            {/* 模板视频 */}
            <Card className="p-6">
              <h3 className="text-sm font-semibold mb-4">📚 模板视频</h3>
              <Carousel
                opts={{
                  align: "start",
                  loop: true,
                }}
                className="w-full"
              >
                <CarouselContent>
                  {templateTasks.map((template) => (
                    <CarouselItem key={template.id} className="basis-1/2 lg:basis-1/3">
                      <button
                        onClick={() => handleTemplateClick(template.id)}
                        className="w-full rounded-lg overflow-hidden border border-border hover:border-primary/50 transition-all"
                      >
                        <div className="aspect-video bg-muted">
                          <img
                            src={template.task.thumbnail_url}
                            alt={template.name}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div className="p-3 bg-background">
                          <p className="text-sm font-medium">{template.name}</p>
                          <Badge variant="secondary" className="mt-1 text-xs">
                            {template.task.style}
                          </Badge>
                        </div>
                      </button>
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
              </Carousel>
            </Card>
          </div>
        </div>
      </div>

      <ShareDialog open={shareDialogOpen} onOpenChange={setShareDialogOpen} />
    </div>
  )
}
