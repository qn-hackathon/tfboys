import { Bell, Moon, Sun, ChevronDown, Check } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useState, useEffect } from 'react'
import { Badge } from '@/components/ui/badge'
import { ShimmeringText } from '@/components/ui/shimmering-text'

// Mock 消息数据类型
interface Notification {
  id: string
  content: string
  isRead: boolean
  timestamp: Date
}

export function Header() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('theme')
    return savedTheme === 'dark'
  })

  // Mock 消息数据
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: '1',
      content: '您的视频 "春天的故事" 已生成完成',
      isRead: false,
      timestamp: new Date(Date.now() - 1000 * 60 * 5), // 5分钟前
    },
    {
      id: '2',
      content: '视频生成任务已开始处理',
      isRead: false,
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30分钟前
    },
    {
      id: '3',
      content: '您的账户额度已充值成功',
      isRead: true,
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2小时前
    },
  ])

  // 未读消息数量
  const unreadCount = notifications.filter((n) => !n.isRead).length

  useEffect(() => {
    const root = document.documentElement
    if (isDarkMode) {
      root.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      root.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }, [isDarkMode])

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
  }

  // Mock 函数：标记消息为已读
  const markAsRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((notification) =>
        notification.id === id
          ? { ...notification, isRead: true }
          : notification
      )
    )
  }

  // 格式化时间显示
  const formatTimestamp = (date: Date) => {
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / (1000 * 60))
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (minutes < 60) return `${minutes}分钟前`
    if (hours < 24) return `${hours}小时前`
    return `${days}天前`
  }

  return (
    <header className="border-b bg-background">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-2">
          <h1>
            <ShimmeringText 
              text="文创速推 - 文字内容的短视频传播加速平台" 
              className="text-xl font-semibold"
              wave={true}
            />
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-sm text-muted-foreground">
            额度: <span className="font-medium text-foreground">100 分钟</span>
          </div>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="gap-1">
                <span>用户名</span>
                <ChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>个人设置</DropdownMenuItem>
              <DropdownMenuItem>退出登录</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <Button variant="ghost" size="icon" onClick={toggleTheme}>
            {isDarkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>

          <Popover>
            <PopoverTrigger asChild>
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-5 w-5" />
                {unreadCount > 0 && (
                  <Badge 
                    variant="destructive" 
                    className="absolute -right-1 -top-1 h-5 w-5 rounded-full p-0 text-xs flex items-center justify-center"
                  >
                    {unreadCount}
                  </Badge>
                )}
              </Button>
            </PopoverTrigger>
            <PopoverContent align="end" className="w-80 p-0">
              <div className="flex items-center justify-between border-b px-4 py-3">
                <h3 className="font-semibold text-sm">消息通知</h3>
                {unreadCount > 0 && (
                  <Badge variant="secondary" className="text-xs">
                    {unreadCount} 条未读
                  </Badge>
                )}
              </div>
              <div className="max-h-[400px] overflow-y-auto">
                {notifications.length === 0 ? (
                  <div className="py-8 text-center text-sm text-muted-foreground">
                    暂无消息
                  </div>
                ) : (
                  notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`border-b px-4 py-3 hover:bg-accent/50 transition-colors ${
                        !notification.isRead ? 'bg-accent/20' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm leading-relaxed break-words">
                            {notification.content}
                          </p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {formatTimestamp(notification.timestamp)}
                          </p>
                        </div>
                        {!notification.isRead && (
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 shrink-0"
                            onClick={() => markAsRead(notification.id)}
                            title="标记为已读"
                          >
                            <Check className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
              {notifications.length > 0 && (
                <div className="border-t px-4 py-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full text-xs"
                    onClick={() => {
                      // Mock 函数：清空所有消息
                      setNotifications([])
                    }}
                  >
                    清空所有消息
                  </Button>
                </div>
              )}
            </PopoverContent>
          </Popover>
        </div>
      </div>
    </header>
  )
}
