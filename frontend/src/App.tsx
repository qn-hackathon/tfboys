import { MainLayout } from '@/components/layout/MainLayout'
import { Toaster } from 'sonner'

function App() {
  return (
    <>
      <MainLayout />
      <Toaster position="top-center" richColors />
    </>
  )
}

export default App
