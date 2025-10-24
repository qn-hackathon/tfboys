import { useState } from 'react'
import { Card, Input, Button, message, Typography } from 'antd'
import { useNavigate } from 'react-router-dom'
import { taskService } from '../../services/taskService'

const { TextArea } = Input
const { Title } = Typography

export default function TaskCreate() {
  const [novelText, setNovelText] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async () => {
    if (!novelText.trim()) {
      message.error('请输入小说文字')
      return
    }

    setLoading(true)
    try {
      const response = await taskService.createTask({ novel_text: novelText })
      message.success('任务创建成功!')
      navigate(`/video/${response.task_id}`)
    } catch (error) {
      message.error('任务创建失败，请重试')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <Card>
        <Title level={3}>创建视频生成任务</Title>
        <TextArea
          rows={10}
          placeholder="请输入小说文字内容..."
          value={novelText}
          onChange={(e) => setNovelText(e.target.value)}
          style={{ marginBottom: 16 }}
        />
        <Button
          type="primary"
          size="large"
          block
          loading={loading}
          onClick={handleSubmit}
        >
          开始生成视频
        </Button>
      </Card>
    </div>
  )
}
