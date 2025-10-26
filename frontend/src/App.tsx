import { useState, useEffect } from 'react'
import { MainLayout } from '@/components/layout/MainLayout'
import { HomeLayout } from '@/components/layout/HomeLayout'
import { Toaster } from '@/components/ui/toaster'

function App() {
  const [currentRoute, setCurrentRoute] = useState<'home' | 'app'>(() => {
    const path = window.location.pathname
    return path === '/' || path === '/home' ? 'home' : 'app'
  })

  useEffect(() => {
    const handleNavigate = (event: CustomEvent<{ route: 'home' | 'app' }>) => {
      setCurrentRoute(event.detail.route)
      window.history.pushState({}, '', event.detail.route === 'home' ? '/' : '/app')
    }

    window.addEventListener('navigate' as any, handleNavigate as EventListener)
    return () => window.removeEventListener('navigate' as any, handleNavigate as EventListener)
  }, [])

  return (
    <>
      {currentRoute === 'home' ? <HomeLayout /> : <MainLayout />}
      <Toaster />
    </>
  )
}

export default App
