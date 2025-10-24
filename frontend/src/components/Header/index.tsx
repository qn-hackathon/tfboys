import { Layout, Menu } from 'antd'
import { Link, useLocation } from 'react-router-dom'
import { HomeOutlined, PlusOutlined, UnorderedListOutlined } from '@ant-design/icons'

const { Header: AntHeader } = Layout

export default function Header() {
  const location = useLocation()

  const menuItems = [
    { key: '/', label: <Link to="/">首页</Link>, icon: <HomeOutlined /> },
    { key: '/create', label: <Link to="/create">创建任务</Link>, icon: <PlusOutlined /> },
    { key: '/tasks', label: <Link to="/tasks">任务列表</Link>, icon: <UnorderedListOutlined /> },
  ]

  return (
    <AntHeader style={{ display: 'flex', alignItems: 'center' }}>
      <div style={{ color: 'white', fontSize: '20px', marginRight: '50px' }}>
        TFBoys 文字生成视频系统
      </div>
      <Menu
        theme="dark"
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        style={{ flex: 1, minWidth: 0 }}
      />
    </AntHeader>
  )
}
