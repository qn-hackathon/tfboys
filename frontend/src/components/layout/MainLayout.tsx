import { useState } from 'react'
import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { VideoGenerationPage } from '@/pages/VideoGenerationPage'
import { MyTasksPage } from '@/pages/MyTasksPage'
import { VideoTemplatesPage } from '@/pages/VideoTemplatesPage'

export function MainLayout() {
  const [currentPage, setCurrentPage] = useState<'video-generation' | 'my-tasks' | 'video-templates'>(
    'video-generation'
  )

  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar currentPage={currentPage} onPageChange={setCurrentPage} />
        <main className="flex-1 overflow-auto">
          {currentPage === 'video-generation' && <VideoGenerationPage />}
          {currentPage === 'video-templates' && <VideoTemplatesPage />}
          {currentPage === 'my-tasks' && <MyTasksPage />}
        </main>
      </div>
    </div>
  )
}
