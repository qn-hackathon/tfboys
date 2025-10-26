/**
 * 用户 API - Mock 实现
 * 使用 localStorage 存储用户信息
 */

// 用户信息接口
export interface User {
  id: string
  username: string
  email: string
  quota: number // 剩余额度（分钟）
}

// 登录请求参数
export interface LoginParams {
  username: string
  password: string
}

// 手机验证码登录参数
export interface PhoneLoginParams {
  phone: string
  code: string
}

// 登录响应
export interface LoginResponse {
  success: boolean
  message: string
  user?: User
}

const USER_STORAGE_KEY = 'tfboys_user'

/**
 * 用户名密码登录 (Mock)
 */
export const loginWithPassword = async (
  params: LoginParams
): Promise<LoginResponse> => {
  // 模拟网络延迟
  await new Promise((resolve) => setTimeout(resolve, 800))

  // Mock 登录验证：任意用户名和密码都可以登录
  if (params.username && params.password) {
    const user: User = {
      id: `user_${Date.now()}`,
      username: params.username,
      email: `${params.username}@example.com`,
      quota: 100, // 默认 100 分钟额度
    }

    // 存储到 localStorage
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user))

    return {
      success: true,
      message: '登录成功',
      user,
    }
  }

  return {
    success: false,
    message: '用户名或密码不能为空',
  }
}

/**
 * 手机验证码登录 (Mock)
 */
export const loginWithPhone = async (
  params: PhoneLoginParams
): Promise<LoginResponse> => {
  // 模拟网络延迟
  await new Promise((resolve) => setTimeout(resolve, 800))

  // Mock 登录验证：任意手机号和验证码都可以登录
  if (params.phone && params.code) {
    const user: User = {
      id: `user_${Date.now()}`,
      username: `用户${params.phone.slice(-4)}`, // 使用手机号后4位作为用户名
      email: `${params.phone}@phone.com`,
      quota: 100, // 默认 100 分钟额度
    }

    // 存储到 localStorage
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user))

    return {
      success: true,
      message: '登录成功',
      user,
    }
  }

  return {
    success: false,
    message: '手机号或验证码不能为空',
  }
}

/**
 * 获取当前用户信息
 */
export const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem(USER_STORAGE_KEY)
  if (!userStr) return null

  try {
    return JSON.parse(userStr) as User
  } catch {
    return null
  }
}

/**
 * 退出登录
 */
export const logout = (): void => {
  localStorage.removeItem(USER_STORAGE_KEY)
}

/**
 * 更新用户信息
 */
export const updateUser = (user: User): void => {
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user))
}
