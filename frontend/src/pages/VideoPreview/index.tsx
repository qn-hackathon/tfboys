import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Spin, Button, Progress, Typography, Alert, Space } from 'antd'
import { DownloadOutlined, ReloadOutlined } from '@ant-design/icons'
import { taskService } from '../../services/taskService'
import { usePolling } from '../../hooks/usePolling'
import type { Task } from '../../types/task'

const { Title, Paragraph } = Typography

export default function VideoPreview() {
  const { taskId } = useParams<{ taskId: string }>()
  const [task, setTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchTask = async () => {
    if (!taskId) return
    try {
      const data = await taskService.getTask(taskId)
      setTask(data)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTask()
  }, [taskId])

  usePolling(fetchTask, 3000, task?.status === 'processing')

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!task) {
    return <Alert message="任务不存在" type="error" />
  }

  const progress = task.progress
    ? Math.round((task.progress.processed_scenes / task.progress.total_scenes) * 100)
    : 0

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto' }}>
      <Card>
        <Title level={3}>视频生成详情</Title>
        <Paragraph>任务ID: {task.task_id}</Paragraph>

        {task.status === 'processing' && (
          <Space direction="vertical" style={{ width: '100%', marginBottom: 24 }}>
            <Alert message="视频正在生成中，请稍候..." type="info" showIcon />
            <Progress percent={progress} status="active" />
            {task.progress && (
              <Paragraph>
                进度: {task.progress.processed_scenes} / {task.progress.total_scenes} 场景
              </Paragraph>
            )}
          </Space>
        )}

        {task.status === 'completed' && task.result?.video_url && (
          <Space direction="vertical" style={{ width: '100%' }}>
            <Alert message="视频生成成功!" type="success" showIcon />
            <video
              controls
              style={{ width: '100%', maxHeight: 500, marginTop: 16 }}
              src={task.result.video_url}
            />
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              href={task.result.video_url}
              download
            >
              下载视频
            </Button>
          </Space>
        )}

        {task.status === 'failed' && (
          <Alert
            message="视频生成失败"
            description={task.error || '未知错误'}
            type="error"
            showIcon
          />
        )}

        <Button
          icon={<ReloadOutlined />}
          onClick={fetchTask}
          style={{ marginTop: 16 }}
        >
          刷新状态
        </Button>
      </Card>
    </div>
  )
}
