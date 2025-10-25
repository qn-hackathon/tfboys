import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Sparkles } from 'lucide-react'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

function App() {
  const { data, error, isLoading } = useSWR('/api/health', fetcher, {
    shouldRetryOnError: false,
    revalidateOnFocus: false,
  })

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <motion.div
              animate={{ opacity: [1, 0.5, 1] }}
              transition={{ duration: 2, repeat: Infinity, ease: [0.4, 0, 0.6, 1] }}
            >
              <Sparkles className="w-6 h-6" />
            </motion.div>
            TFBoys Frontend
          </CardTitle>
          <CardDescription>
            基于 Vite + React + TypeScript 的现代化前端样板
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <h3 className="font-semibold">技术栈</h3>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>✅ Vite - 快速构建工具</li>
              <li>✅ React 18 - UI 框架</li>
              <li>✅ TypeScript - 类型安全</li>
              <li>✅ Tailwind CSS - 样式系统</li>
              <li>✅ shadcn/ui - 组件库</li>
              <li>✅ framer-motion - 动画库</li>
              <li>✅ lucide-react - 图标库</li>
              <li>✅ SWR - 数据获取</li>
            </ul>
          </div>

          <div className="space-y-2">
            <h3 className="font-semibold">API 状态</h3>
            <div className="text-sm">
              {isLoading && <p className="text-muted-foreground">检查中...</p>}
              {error && <p className="text-destructive">API 未连接</p>}
              {data && <p className="text-green-600">✓ API 已就绪</p>}
              {!isLoading && !error && !data && (
                <p className="text-muted-foreground">等待 API 服务启动</p>
              )}
            </div>
          </div>

          <Button className="w-full" onClick={() => alert('Hello from TFBoys!')}>
            <Sparkles className="w-4 h-4" />
            开始使用
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

export default App
