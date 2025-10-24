import { Card, Button, Typography, Row, Col } from 'antd'
import { useNavigate } from 'react-router-dom'
import { PlusOutlined, UnorderedListOutlined } from '@ant-design/icons'

const { Title, Paragraph } = Typography

export default function Home() {
  const navigate = useNavigate()

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '40px 0' }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
        欢迎使用 TFBoys 文字生成视频系统
      </Title>
      
      <Paragraph style={{ fontSize: 16, textAlign: 'center', marginBottom: 60 }}>
        将小说文字自动转换为动漫风格视频，支持角色一致性、智能配音和自动字幕
      </Paragraph>

      <Row gutter={[24, 24]}>
        <Col xs={24} md={12}>
          <Card
            hoverable
            onClick={() => navigate('/create')}
            style={{ height: '100%' }}
          >
            <PlusOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
            <Title level={4}>创建新任务</Title>
            <Paragraph>
              上传小说文字，系统将自动分析场景、生成图像和配音，最终合成视频
            </Paragraph>
            <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/create')}>
              立即开始
            </Button>
          </Card>
        </Col>
        
        <Col xs={24} md={12}>
          <Card
            hoverable
            onClick={() => navigate('/tasks')}
            style={{ height: '100%' }}
          >
            <UnorderedListOutlined style={{ fontSize: 48, color: '#52c41a', marginBottom: 16 }} />
            <Title level={4}>查看任务</Title>
            <Paragraph>
              查看所有任务的处理进度，下载已完成的视频
            </Paragraph>
            <Button icon={<UnorderedListOutlined />} onClick={() => navigate('/tasks')}>
              查看列表
            </Button>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
