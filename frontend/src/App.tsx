import { useState, useEffect } from 'react'
import { MainLayout } from '@/components/layout/MainLayout'
import { HomeLayout } from '@/components/layout/HomeLayout'
import { Toaster } from 'sonner'

function App() {
  const [currentRoute, setCurrentRoute] = useState<'home' | 'app'>(() => {
    const path = window.location.pathname
    return path === '/' || path === '/home' ? 'home' : 'app'
  })

  useEffect(() => {
    const handleNavigate = (event: Event) => {
      const customEvent = event as CustomEvent<{ route: 'home' | 'app' }>
      setCurrentRoute(customEvent.detail.route)
      window.history.pushState({}, '', customEvent.detail.route === 'home' ? '/' : '/app')
    }

    window.addEventListener('navigate', handleNavigate)
    return () => window.removeEventListener('navigate', handleNavigate)
  }, [])

  return (
    <>
      {currentRoute === 'home' ? <HomeLayout /> : <MainLayout />}
      <Toaster position="top-center" richColors />
    </>
  )
}

export default App
