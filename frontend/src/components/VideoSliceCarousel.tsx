import { useState } from "react"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import { VideoSlice } from "@/data/mockData"

interface VideoSliceCarouselProps {
  slices: VideoSlice[]
  onSliceClick: (index: number, timeInSeconds: number) => void
  currentSliceIndex?: number
}

export function VideoSliceCarousel({
  slices,
  onSliceClick,
  currentSliceIndex = 0,
}: VideoSliceCarouselProps) {
  return (
    <Carousel
      opts={{
        align: "start",
      }}
      className="w-full"
    >
      <CarouselContent>
        {slices.map((slice, index) => (
          <CarouselItem key={slice.id} className="basis-1/3 lg:basis-1/4">
            <button
              onClick={() => onSliceClick(index, slice.timeInSeconds)}
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
  )
}
