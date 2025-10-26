import { Header } from './Header'
import { HomePage } from '@/pages/HomePage'

export function HomeLayout() {
  return (
    <div className="h-screen flex flex-col">
      <Header />
      <main className="flex-1 overflow-auto">
        <HomePage />
      </main>
    </div>
  )
}
