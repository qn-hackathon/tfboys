import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Search, Eye, Edit } from "lucide-react"
import { getVideoTemplates, type VideoTemplate, type Video } from "@/apis/video"
import { VideoPreviewDialog } from "@/components/VideoPreviewDialog"
import { toast } from "sonner"

type VideoStyle = "全部" | "古风" | "现代" | "动漫" | "奇幻" | "3D卡通"
type VideoResolution = "全部" | "720p" | "1080p" | "4K"

export function VideoTemplatesPage() {
  const [searchKeyword, setSearchKeyword] = useState("")
  const [selectedStyle, setSelectedStyle] = useState<VideoStyle>("全部")
  const [selectedResolution, setSelectedResolution] = useState<VideoResolution>("全部")
  const [previewVideo, setPreviewVideo] = useState<Video | null>(null)
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false)
  const [templates, setTemplates] = useState<VideoTemplate[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        setIsLoading(true)
        const response = await getVideoTemplates()
        if (response.code === 0 && response.data) {
          setTemplates(response.data)
        } else {
          toast.error(response.message || "获取视频模板失败")
        }
      } catch (error) {
        toast.error("获取视频模板时发生错误")
      } finally {
        setIsLoading(false)
      }
    }

    fetchTemplates()
  }, [])

  const filteredTemplates = templates.filter((template) => {
    const matchesKeyword =
      searchKeyword === "" ||
      template.name.toLowerCase().includes(searchKeyword.toLowerCase()) ||
      template.video.description.toLowerCase().includes(searchKeyword.toLowerCase()) ||
      template.video.keywords.some((keyword) =>
        keyword.toLowerCase().includes(searchKeyword.toLowerCase())
      )

    const matchesStyle = selectedStyle === "全部" || template.video.style === selectedStyle

    const matchesResolution =
      selectedResolution === "全部" || template.video.resolution === selectedResolution

    return matchesKeyword && matchesStyle && matchesResolution
  })

  const handlePreview = (template: VideoTemplate) => {
    setPreviewVideo(template.video)
    setPreviewDialogOpen(true)
  }

  const handleEdit = (template: VideoTemplate) => {
    console.log("编辑模板:", template.name)
  }

  const handleDownload = () => {
    console.log("下载视频")
  }

  const handleShare = () => {
    console.log("分享视频")
  }


  return (
    <div className="h-full p-6 overflow-auto">
      <div className="max-w-[1400px] mx-auto">
        <h1 className="text-3xl font-bold mb-6">🎬 视频模板</h1>

        <div className="bg-background rounded-lg border p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="搜索模板名称、描述或关键词..."
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                className="pl-10"
              />
            </div>

            <Select value={selectedStyle} onValueChange={(v) => setSelectedStyle(v as VideoStyle)}>
              <SelectTrigger className="w-full md:w-[180px]">
                <SelectValue placeholder="选择风格" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="全部">全部风格</SelectItem>
                <SelectItem value="古风">古风</SelectItem>
                <SelectItem value="现代">现代</SelectItem>
                <SelectItem value="动漫">动漫</SelectItem>
                <SelectItem value="奇幻">奇幻</SelectItem>
                <SelectItem value="3D卡通">3D卡通</SelectItem>
              </SelectContent>
            </Select>

            <Select
              value={selectedResolution}
              onValueChange={(v) => setSelectedResolution(v as VideoResolution)}
            >
              <SelectTrigger className="w-full md:w-[180px]">
                <SelectValue placeholder="选择分辨率" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="全部">全部分辨率</SelectItem>
                <SelectItem value="720p">720p</SelectItem>
                <SelectItem value="1080p">1080p</SelectItem>
                <SelectItem value="4K">4K</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {(searchKeyword || selectedStyle !== "全部" || selectedResolution !== "全部") && (
            <div className="mt-3 flex items-center gap-2 text-sm text-muted-foreground">
              <span>找到 {filteredTemplates.length} 个模板</span>
              {(selectedStyle !== "全部" ||
                selectedResolution !== "全部" ||
                searchKeyword) && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setSearchKeyword("")
                    setSelectedStyle("全部")
                    setSelectedResolution("全部")
                  }}
                  className="h-6 px-2"
                >
                  清除筛选
                </Button>
              )}
            </div>
          )}
        </div>

        {isLoading ? (
          <div className="text-center py-20">
            <p className="text-muted-foreground text-lg">加载中...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredTemplates.map((template) => (
            <TemplateCard
              key={template.id}
              template={template}
              onPreview={handlePreview}
              onEdit={handleEdit}
            />
            ))}
          </div>
        )}

        {!isLoading && filteredTemplates.length === 0 && (
          <div className="text-center py-20">
            <p className="text-muted-foreground text-lg">未找到匹配的模板</p>
            <Button
              variant="outline"
              onClick={() => {
                setSearchKeyword("")
                setSelectedStyle("全部")
                setSelectedResolution("全部")
              }}
              className="mt-4"
            >
              清除筛选条件
            </Button>
          </div>
        )}
      </div>

      <VideoPreviewDialog
        video={previewVideo}
        open={previewDialogOpen}
        onOpenChange={setPreviewDialogOpen}
        onDownload={handleDownload}
        onShare={handleShare}
      />
    </div>
  )
}

interface TemplateCardProps {
  template: VideoTemplate
  onPreview: (template: VideoTemplate) => void
  onEdit: (template: VideoTemplate) => void
}

function TemplateCard({ template, onPreview, onEdit }: TemplateCardProps) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div
      className="group relative rounded-lg overflow-hidden border bg-card transition-all hover:shadow-lg"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative aspect-video overflow-hidden bg-muted">
        <img
          src={template.video.thumbnailUrl}
          alt={template.name}
          className={`w-full h-full object-cover transition-all duration-300 ${
            isHovered ? "scale-110 blur-sm" : "scale-100 blur-0"
          }`}
        />

        <div
          className={`absolute inset-0 bg-black/60 flex items-center justify-center gap-3 transition-opacity duration-300 ${
            isHovered ? "opacity-100" : "opacity-0"
          }`}
        >
          <Button
            size="sm"
            variant="secondary"
            onClick={() => onEdit(template)}
            className="gap-2"
          >
            <Edit className="h-4 w-4" />
            编辑
          </Button>
          <Button
            size="sm"
            variant="default"
            onClick={() => onPreview(template)}
            className="gap-2"
          >
            <Eye className="h-4 w-4" />
            预览
          </Button>
        </div>
      </div>

      <div className="p-4">
        <h3 className="font-semibold text-base mb-2 line-clamp-1">{template.name}</h3>
        <p className="text-sm text-muted-foreground mb-3 line-clamp-2 min-h-[40px]">
          {template.video.description}
        </p>

        <div className="flex items-center justify-between mb-3">
          <Badge variant="secondary" className="text-xs">
            {template.video.style}
          </Badge>
          <span className="text-xs text-muted-foreground">{template.video.duration}</span>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {template.video.keywords.slice(0, 3).map((keyword) => (
            <Badge key={keyword} variant="outline" className="text-xs">
              {keyword}
            </Badge>
          ))}
        </div>
      </div>
    </div>
  )
}
