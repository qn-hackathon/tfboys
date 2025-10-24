import { useState, useEffect } from 'react'
import { Card, Table, Tag, Button, message } from 'antd'
import { useNavigate } from 'react-router-dom'
import type { ColumnsType } from 'antd/es/table'
import { taskService } from '../../services/taskService'
import { usePolling } from '../../hooks/usePolling'
import type { Task } from '../../types/task'

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const fetchTasks = async () => {
    setLoading(true)
    try {
      const data = await taskService.listTasks()
      setTasks(data)
    } catch (error) {
      message.error('获取任务列表失败')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  usePolling(fetchTasks, 5000, tasks.some(t => t.status === 'processing'))

  const statusMap = {
    pending: { color: 'default', text: '等待中' },
    processing: { color: 'processing', text: '处理中' },
    completed: { color: 'success', text: '已完成' },
    failed: { color: 'error', text: '失败' },
  }

  const columns: ColumnsType<Task> = [
    {
      title: '任务ID',
      dataIndex: 'task_id',
      key: 'task_id',
      width: 200,
      render: (text) => text.slice(0, 8) + '...',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: Task['status']) => (
        <Tag color={statusMap[status].color}>{statusMap[status].text}</Tag>
      ),
    },
    {
      title: '进度',
      key: 'progress',
      width: 150,
      render: (_, record) => {
        if (record.progress) {
          const { processed_scenes, total_scenes } = record.progress
          return `${processed_scenes}/${total_scenes}`
        }
        return '-'
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (text) => new Date(text).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <Button
          type="link"
          onClick={() => navigate(`/video/${record.task_id}`)}
        >
          查看详情
        </Button>
      ),
    },
  ]

  return (
    <Card title="任务列表">
      <Table
        columns={columns}
        dataSource={tasks}
        rowKey="task_id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </Card>
  )
}
