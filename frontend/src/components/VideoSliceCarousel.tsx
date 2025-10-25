import { useState, useEffect } from "react"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import { mockVideoSlices, VideoSlice } from "@/data/mockData"

interface VideoSliceCarouselProps {
  taskId: string
  onSliceClick?: (timeInSeconds: number) => void
}

export function VideoSliceCarousel({
  taskId,
  onSliceClick,
}: VideoSliceCarouselProps) {
  const [currentSliceIndex, setCurrentSliceIndex] = useState(0)
  const [slices, setSlices] = useState<VideoSlice[]>([])

  useEffect(() => {
    setSlices(mockVideoSlices)
  }, [taskId])

  const handleSliceClick = (index: number, timeInSeconds: number) => {
    setCurrentSliceIndex(index)
    if (onSliceClick) {
      onSliceClick(timeInSeconds)
    }
  }

  if (slices.length === 0) return null

  return (
    <div className="h-full flex flex-col">
      <h3 className="text-sm font-semibold mb-3">🎞️ 视频切片</h3>
      <Carousel
        opts={{
          align: "start",
        }}
        className="w-full flex-1"
      >
        <CarouselContent>
          {slices.map((slice, index) => (
            <CarouselItem key={slice.id} className="basis-1/3 lg:basis-1/4">
              <button
                onClick={() => handleSliceClick(index, slice.timeInSeconds)}
                className={`
                  w-full rounded-lg overflow-hidden border-2 transition-all
                  ${
                    currentSliceIndex === index
                      ? "border-primary ring-2 ring-primary/20"
                      : "border-border hover:border-primary/50"
                  }
                `}
              >
                <div className="aspect-video bg-muted">
                  <img
                    src={slice.thumbnailUrl}
                    alt={`场景 ${slice.sceneNumber}`}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-2 bg-background">
                  <p className="text-xs font-medium">场景 {slice.sceneNumber}</p>
                  <p className="text-xs text-muted-foreground">{slice.timestamp}</p>
                </div>
              </button>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  )
}
