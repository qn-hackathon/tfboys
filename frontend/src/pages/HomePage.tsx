import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'

export function HomePage() {
  const handleNavigateToApp = () => {
    window.dispatchEvent(new CustomEvent('navigate', { detail: { route: 'app' } }))
  }

  const videoTemplates = [
    { id: 1, title: '模板 1', thumbnail: 'https://placehold.co/320x180/3b82f6/white?text=模板+1', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4' },
    { id: 2, title: '模板 2', thumbnail: 'https://placehold.co/320x180/8b5cf6/white?text=模板+2', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4' },
    { id: 3, title: '模板 3', thumbnail: 'https://placehold.co/320x180/ec4899/white?text=模板+3', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4' },
    { id: 4, title: '模板 4', thumbnail: 'https://placehold.co/320x180/f59e0b/white?text=模板+4', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4' },
    { id: 5, title: '模板 5', thumbnail: 'https://placehold.co/320x180/10b981/white?text=模板+5', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4' },
  ]

  const textToVideos = [
    { id: 1, title: '示例视频 1', thumbnail: 'https://placehold.co/320x180/3b82f6/white?text=示例+1', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4' },
    { id: 2, title: '示例视频 2', thumbnail: 'https://placehold.co/320x180/8b5cf6/white?text=示例+2', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4' },
    { id: 3, title: '示例视频 3', thumbnail: 'https://placehold.co/320x180/ec4899/white?text=示例+3', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4' },
    { id: 4, title: '示例视频 4', thumbnail: 'https://placehold.co/320x180/f59e0b/white?text=示例+4', videoSrc: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4' },
  ]

  const faqItems = [
    {
      question: '我可以用哪些类型的输入来制作视频?',
      answer: '您可以使用多种输入方式来制作视频:直接输入或粘贴文字内容、上传文本文件(.txt)、或者提供网页链接,我们会自动抓取内容。系统支持小说、故事、文章等各种文本内容,建议输入500-5000字以获得最佳效果。',
    },
    {
      question: '我可以自定义视频输出吗?',
      answer: '当然可以!我们提供了丰富的自定义选项,包括:选择视频风格(古风、现代、动漫、奇幻、3D卡通)、配音类型(女声、男声、童声)、视频分辨率(1080p、720p)。您可以根据内容特点和目标受众选择最合适的参数组合。',
    },
    {
      question: 'AI视频生成器有免费试用吗?',
      answer: '是的,我们为所有新用户提供免费试用额度。注册后您将获得一定的免费生成时长,可以体验完整的视频生成功能。试用期间生成的视频没有水印,可以正常下载和分享。如需更多额度,可以选择我们的付费套餐。',
    },
    {
      question: '生成AI视频需要多长时间?',
      answer: '视频生成时间取决于内容长度和所选参数。通常情况下,一个2-3分钟的视频需要3-5分钟生成时间。系统会实时显示生成进度,包括当前处理阶段(文本分析、图像生成、配音合成、视频合成)和完成百分比。您可以在生成过程中继续使用其他功能。',
    },
    {
      question: '我的数据在这里有多安全?',
      answer: '我们非常重视数据安全和隐私保护。所有上传的文本内容都经过加密传输和存储,仅用于视频生成。我们不会将您的内容用于其他目的或与第三方共享。生成的视频文件会保存7天,之后自动删除。您可以随时在账户设置中删除自己的数据。',
    },
    {
      question: '如何开始使用AI视频生成器?',
      answer: '开始使用非常简单:1) 点击"立即制作"按钮进入视频生成页面;2) 输入您的文本内容或上传文件;3) 选择视频风格、配音类型等参数;4) 点击"生成视频"按钮;5) 等待生成完成后预览、下载或分享您的视频。整个过程无需任何技术背景,界面友好易用。',
    },
  ]

  return (
    <div className="w-full">
      <section className="relative h-[calc(100vh-4rem)] w-full flex items-center justify-center overflow-hidden">
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover"
        >
          <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-black/40" />
        <div className="relative z-10 text-center text-white px-4 max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-2">文创速推</h1>
          <h2 className="text-3xl md:text-4xl font-semibold mb-8">文字内容的短视频传播加速平台</h2>
          <div className="w-32 h-0.5 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-8" />
          <p className="text-lg md:text-xl mb-8 max-w-2xl mx-auto leading-relaxed">
            只需简单的提示词,就能将您的文本、小说或链接转化为高质量视频。无需任何技术技能。
          </p>
          <div className="w-32 h-0.5 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-8" />
          <Button 
            size="lg" 
            className="text-lg px-12 py-4 h-auto rounded-2xl bg-gradient-to-r from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700 animate-gradient bg-[length:200%_auto]"
            onClick={handleNavigateToApp}
          >
            立即制作
          </Button>
        </div>
      </section>

      <section className="py-20 px-4 md:px-8 bg-background">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 tracking-wide">文生视频</h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              轻松将书面内容转化为引人入胜的视频。只需输入您的文字提示,让人工智能生成一个完整的视频,让您的文字变得生动起来。
            </p>
          </div>
          <Carousel className="w-full max-w-5xl mx-auto">
            <CarouselContent>
              {textToVideos.map((video) => (
                <CarouselItem key={video.id} className="md:basis-1/2 lg:basis-1/3">
                  <div className="p-2">
                    <Card className="overflow-hidden">
                      <div className="relative aspect-video">
                        <video
                          autoPlay
                          loop
                          muted
                          playsInline
                          className="w-full h-full object-cover"
                          poster={video.thumbnail}
                        >
                          <source src={video.videoSrc} type="video/mp4" />
                        </video>
                      </div>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      </section>

      <section className="py-20 px-4 md:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 tracking-wide">热门视频模板</h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              一系列有趣又吸引人的视频模板等你来探索。从人工智能生成的亲吻或拥抱等温馨时刻,到人工智能圣诞老人视频等节日祝福,你都能轻松为受众创作令人难忘的内容。
            </p>
          </div>
          <Carousel className="w-full max-w-5xl mx-auto">
            <CarouselContent>
              {videoTemplates.map((template) => (
                <CarouselItem key={template.id} className="md:basis-1/2 lg:basis-1/3">
                  <div className="p-2">
                    <Card className="overflow-hidden cursor-pointer hover:shadow-lg transition-shadow">
                      <div className="relative aspect-video">
                        <video
                          autoPlay
                          loop
                          muted
                          playsInline
                          className="w-full h-full object-cover"
                          poster={template.thumbnail}
                        >
                          <source src={template.videoSrc} type="video/mp4" />
                        </video>
                      </div>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      </section>

      <section className="py-20 px-4 md:px-8 bg-background">
        <div className="max-w-6xl mx-auto">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-3xl md:text-4xl mb-2 tracking-wide">
                超级大语言模型打造最佳的人工智能视频生成器
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-semibold mb-2">快速视频生成</h3>
                    <p className="text-muted-foreground">
                      体验人工智能驱动的视频创作速度。一分钟内生成视频,与传统视频编辑方法相比,为您节省时间和精力。
                    </p>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">高质量视频输出</h3>
                    <p className="text-muted-foreground">
                      我们采用先进算法,确保动画、转场和特效流畅。制作出始终如一、高质量的视频,在任何平台上都能脱颖而出。
                    </p>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">操作简单</h3>
                    <p className="text-muted-foreground">
                      您无需成为视频编辑师也能创作精彩视频!用户友好的界面设计注重易用性,让从初学者到专业人士的任何人都能以最小的成本生成视频。
                    </p>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="relative aspect-video rounded-lg overflow-hidden">
                    <video
                      autoPlay
                      loop
                      muted
                      playsInline
                      className="w-full h-full object-cover"
                    >
                      <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4" type="video/mp4" />
                    </video>
                  </div>
                  <Button 
                    size="lg" 
                    className="w-full text-lg py-6 h-auto rounded-2xl bg-gradient-to-r from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700 animate-gradient bg-[length:200%_auto]"
                    onClick={handleNavigateToApp}
                  >
                    立即制作
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="py-20 px-4 md:px-8 bg-muted/30">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 tracking-wide">FAQ</h2>
          <Accordion type="single" collapsible className="w-full">
            {faqItems.map((item, index) => (
              <AccordionItem key={index} value={`item-${index}`}>
                <AccordionTrigger className="text-left">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>
    </div>
  )
}
