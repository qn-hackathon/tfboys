import { Video, ListTodo, Film } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

interface SidebarProps {
  currentPage: 'video-generation' | 'my-tasks' | 'video-templates'
  onPageChange: (page: 'video-generation' | 'my-tasks' | 'video-templates') => void
}

export function Sidebar({ currentPage, onPageChange }: SidebarProps) {
  const menuItems = [
    {
      id: 'video-generation' as const,
      icon: Video,
      label: '视频生成',
    },
    {
      id: 'video-templates' as const,
      icon: Film,
      label: '视频模板',
    },
    {
      id: 'my-tasks' as const,
      icon: ListTodo,
      label: '我的任务',
      badge: 0,
    },
  ]

  return (
    <aside className="w-60 border-r bg-background">
      <nav className="flex flex-col gap-1 p-4 pt-8">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id

          return (
            <Button
              key={item.id}
              variant={isActive ? 'default' : 'ghost'}
              className={cn(
                'justify-start gap-3 h-14',
                isActive && 'bg-primary text-primary-foreground'
              )}
              onClick={() => onPageChange(item.id)}
            >
              <Icon className="h-5 w-5" />
              <span>{item.label}</span>
              {item.badge !== undefined && item.badge > 0 && (
                <span className="ml-auto flex h-5 w-5 items-center justify-center rounded-full bg-destructive text-xs text-destructive-foreground">
                  {item.badge}
                </span>
              )}
            </Button>
          )
        })}
      </nav>
    </aside>
  )
}
