import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import Home from './pages/Home'
import TaskCreate from './pages/TaskCreate'
import TaskList from './pages/TaskList'
import VideoPreview from './pages/VideoPreview'
import Header from './components/Header'
import Footer from './components/Footer'

const { Content } = Layout

function App() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header />
      <Content style={{ padding: '24px 50px' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<TaskCreate />} />
          <Route path="/tasks" element={<TaskList />} />
          <Route path="/video/:taskId" element={<VideoPreview />} />
        </Routes>
      </Content>
      <Footer />
    </Layout>
  )
}

export default App
