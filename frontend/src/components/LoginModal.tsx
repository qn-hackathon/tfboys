import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Github } from 'lucide-react'
import { loginWithPassword, loginWithPhone, type User } from '@/apis/user'

interface LoginModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onLoginSuccess: (user: User) => void
}

export function LoginModal({ open, onOpenChange, onLoginSuccess }: LoginModalProps) {
  const [activeTab, setActiveTab] = useState('password')
  
  // 密码登录状态
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [passwordLoading, setPasswordLoading] = useState(false)
  
  // 手机验证码登录状态
  const [phone, setPhone] = useState('')
  const [code, setCode] = useState('')
  const [phoneLoading, setPhoneLoading] = useState(false)
  const [codeSent, setCodeSent] = useState(false)
  const [countdown, setCountdown] = useState(0)

  // 处理密码登录
  const handlePasswordLogin = async () => {
    if (!username || !password) {
      alert('请输入用户名和密码')
      return
    }

    setPasswordLoading(true)
    try {
      const response = await loginWithPassword({ username, password })
      if (response.success && response.user) {
        onLoginSuccess(response.user)
        onOpenChange(false)
        // 清空表单
        setUsername('')
        setPassword('')
      } else {
        alert(response.message)
      }
    } catch (error) {
      alert('登录失败，请稍后重试')
    } finally {
      setPasswordLoading(false)
    }
  }

  // 发送验证码
  const handleSendCode = () => {
    if (!phone) {
      alert('请输入手机号')
      return
    }

    if (!/^1[3-9]\d{9}$/.test(phone)) {
      alert('请输入有效的手机号')
      return
    }

    // Mock 发送验证码
    setCodeSent(true)
    setCountdown(60)
    
    // 倒计时
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          setCodeSent(false)
          return 0
        }
        return prev - 1
      })
    }, 1000)
  }

  // 处理手机验证码登录
  const handlePhoneLogin = async () => {
    if (!phone || !code) {
      alert('请输入手机号和验证码')
      return
    }

    setPhoneLoading(true)
    try {
      const response = await loginWithPhone({ phone, code })
      if (response.success && response.user) {
        onLoginSuccess(response.user)
        onOpenChange(false)
        // 清空表单
        setPhone('')
        setCode('')
        setCodeSent(false)
        setCountdown(0)
      } else {
        alert(response.message)
      }
    } catch (error) {
      alert('登录失败，请稍后重试')
    } finally {
      setPhoneLoading(false)
    }
  }

  // 处理第三方登录（Mock，仅显示提示）
  const handleThirdPartyLogin = (provider: string) => {
    alert(`${provider} 登录功能开发中，敬请期待`)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>登录</DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="password">密码登录</TabsTrigger>
            <TabsTrigger value="phone">验证码登录</TabsTrigger>
            <TabsTrigger value="third-party">第三方登录</TabsTrigger>
          </TabsList>

          {/* 密码登录 */}
          <TabsContent value="password" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">用户名</Label>
              <Input
                id="username"
                placeholder="请输入用户名"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handlePasswordLogin()}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">密码</Label>
              <Input
                id="password"
                type="password"
                placeholder="请输入密码"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handlePasswordLogin()}
              />
            </div>
            <Button
              className="w-full"
              onClick={handlePasswordLogin}
              disabled={passwordLoading}
            >
              {passwordLoading ? '登录中...' : '登录'}
            </Button>
            <p className="text-xs text-muted-foreground text-center">
              提示: 当前为演示模式，任意用户名和密码均可登录
            </p>
          </TabsContent>

          {/* 手机验证码登录 */}
          <TabsContent value="phone" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="phone">手机号</Label>
              <Input
                id="phone"
                placeholder="请输入手机号"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="code">验证码</Label>
              <div className="flex gap-2">
                <Input
                  id="code"
                  placeholder="请输入验证码"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handlePhoneLogin()}
                />
                <Button
                  variant="outline"
                  onClick={handleSendCode}
                  disabled={codeSent}
                  className="shrink-0"
                >
                  {codeSent ? `${countdown}秒` : '发送验证码'}
                </Button>
              </div>
            </div>
            <Button
              className="w-full"
              onClick={handlePhoneLogin}
              disabled={phoneLoading}
            >
              {phoneLoading ? '登录中...' : '登录'}
            </Button>
            <p className="text-xs text-muted-foreground text-center">
              提示: 当前为演示模式，任意手机号和验证码均可登录
            </p>
          </TabsContent>

          {/* 第三方登录 */}
          <TabsContent value="third-party" className="space-y-4">
            <div className="space-y-3">
              <Button
                variant="outline"
                className="w-full justify-start gap-2"
                onClick={() => handleThirdPartyLogin('微信')}
              >
                <svg
                  className="h-5 w-5"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89l-.062-.001-.081-.001a8.098 8.098 0 0 0-.18-.002zM15.312 9.82c.12 0 .24.012.36.024l.08.005.08.005c.28.024.56.072.824.144l.12.024.12.024c.24.06.48.144.72.24l.12.048.12.048c.24.096.456.216.672.336l.096.048.096.048c.216.12.408.264.6.408l.072.072.072.072c.192.144.36.312.528.48l.048.048.048.048c.168.168.312.36.456.552l.024.024.024.024c.144.192.264.408.384.624l.024.048.024.048c.12.216.216.432.312.672l.024.096.024.096c.096.24.168.48.216.72l.024.12.024.12c.048.264.072.528.072.792v.024c0 .12-.024.24-.024.36v.024c0 .12-.024.24-.048.36l-.024.12-.024.12c-.048.24-.096.48-.168.72l-.024.12-.024.12c-.072.24-.168.456-.264.672l-.048.096-.048.096c-.096.216-.216.432-.336.624l-.072.096-.072.096c-.12.192-.264.384-.408.552l-.048.072-.048.072c-.144.168-.312.336-.48.504l-.048.048-.048.048c-.168.144-.36.288-.552.432l-.024.024-.024.024c-.192.12-.408.24-.624.336l-.048.024-.048.024c-.216.096-.456.168-.672.24l-.096.024-.096.024c-.24.048-.48.096-.72.12l-.12.012-.12.012c-.24.024-.48.024-.72.024h-.024c-.12 0-.24 0-.36-.024h-.024c-.12 0-.24-.024-.36-.024l-.12-.024-.12-.024c-.24-.048-.48-.096-.72-.168l-.12-.024-.12-.024c-.24-.072-.456-.168-.672-.264l-.096-.048-.096-.048c-.216-.096-.432-.216-.624-.336l-.096-.072-.096-.072c-.192-.12-.384-.264-.552-.408l-.072-.048-.072-.048c-.168-.144-.336-.312-.504-.48l-.048-.048-.048-.048c-.144-.168-.288-.36-.432-.552l-.024-.024-.024-.024a5.862 5.862 0 0 1-.336-.624l-.024-.048-.024-.048c-.096-.216-.168-.432-.24-.672l-.024-.096-.024-.096c-.048-.24-.096-.48-.12-.72l-.012-.12-.012-.12c-.024-.24-.024-.48-.024-.72v-.024c0-.12 0-.24.024-.36v-.024c0-.12.024-.24.024-.36l.024-.12.024-.12c.048-.24.096-.48.168-.72l.024-.12.024-.12c.072-.24.168-.456.264-.672l.048-.096.048-.096c.096-.216.216-.432.336-.624l.072-.096.072-.096c.12-.192.264-.384.408-.552l.048-.072.048-.072c.144-.168.312-.336.48-.504l.048-.048.048-.048c.168-.144.36-.288.552-.432l.024-.024.024-.024c.192-.12.408-.24.624-.336l.048-.024.048-.024c.216-.096.456-.168.672-.24l.096-.024.096-.024c.24-.048.48-.096.72-.12l.12-.012.12-.012c.12 0 .24-.024.36-.024h.024c.12 0 .24 0 .36.024h.024z" />
                </svg>
                微信登录
              </Button>

              <Button
                variant="outline"
                className="w-full justify-start gap-2"
                onClick={() => handleThirdPartyLogin('抖音')}
              >
                <svg
                  className="h-5 w-5"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z" />
                </svg>
                抖音登录
              </Button>

              <Button
                variant="outline"
                className="w-full justify-start gap-2"
                onClick={() => handleThirdPartyLogin('GitHub')}
              >
                <Github className="h-5 w-5" />
                GitHub 登录
              </Button>
            </div>
            <p className="text-xs text-muted-foreground text-center">
              提示: 第三方登录功能开发中
            </p>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}
