import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Info } from "lucide-react"

interface ShareDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

type Platform = "douyin" | "kuaishou"

export function ShareDialog({ open, onOpenChange }: ShareDialogProps) {
  const [selectedPlatform, setSelectedPlatform] = useState<Platform>("douyin")
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  const handleShare = () => {
    console.log("分享到:", selectedPlatform)
    console.log("标题:", title)
    console.log("描述:", description)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>一键分享到短视频平台</DialogTitle>
          <DialogDescription>
            选择平台并填写视频信息,一键发布到短视频平台
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <Alert>
            <Info className="h-4 w-4" />
            <AlertDescription>
              请先绑定短视频平台账号,才能进行分享操作
            </AlertDescription>
          </Alert>

          <div className="space-y-3">
            <Label className="text-base">选择平台</Label>
            <RadioGroup value={selectedPlatform} onValueChange={(v) => setSelectedPlatform(v as Platform)}>
              <div className="flex gap-6">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="douyin" id="platform-douyin" />
                  <Label htmlFor="platform-douyin" className="cursor-pointer font-normal">
                    抖音
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="kuaishou" id="platform-kuaishou" />
                  <Label htmlFor="platform-kuaishou" className="cursor-pointer font-normal">
                    快手
                  </Label>
                </div>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label htmlFor="share-title">视频标题</Label>
            <Input
              id="share-title"
              placeholder="请输入视频标题"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="share-description">视频描述</Label>
            <Textarea
              id="share-description"
              placeholder="请输入视频描述信息"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="min-h-[100px] resize-none"
            />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            取消
          </Button>
          <Button onClick={handleShare}>
            确定分享
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
