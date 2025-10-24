import { Layout } from 'antd'

const { Footer: AntFooter } = Layout

export default function Footer() {
  return (
    <AntFooter style={{ textAlign: 'center' }}>
      TFBoys ©{new Date().getFullYear()} - Token Free Boys
    </AntFooter>
  )
}
