 #!/bin/bash
# 容器更新脚本

set -e

echo "🔄 开始更新容器..."

# 步骤1: 停止现有容器
echo "📦 停止现有容器..."
sudo docker compose down

# 步骤2: 清理旧镜像
echo "🧹 清理旧镜像..."
sudo docker image prune -f

# 步骤3: 重新构建并启动
echo "🔨 重新构建并启动容器..."
sudo docker compose up -d --build

# 步骤4: 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 步骤5: 验证服务状态
echo "✅ 验证服务状态..."
sudo docker compose ps

# 步骤6: 测试连接
echo "🔍 测试服务连接..."
echo "测试Redis连接..."
sudo docker exec -it tfboys-ai-service python -c "
from app.config import settings
import redis
try:
    r = redis.from_url(settings.redis_url)
    print('✅ Redis连接正常:', r.ping())
except Exception as e:
    print('❌ Redis连接失败:', e)
"

echo "测试AI Service健康检查..."
if curl -s -f http://localhost:8002/health > /dev/null; then
    echo "✅ AI Service健康检查通过"
else
    echo "❌ AI Service健康检查失败"
fi

echo "测试Video Service健康检查..."
if curl -s -f http://localhost:8003/health > /dev/null; then
    echo "✅ Video Service健康检查通过"
else
    echo "❌ Video Service健康检查失败"
fi

echo "测试API Gateway健康检查..."
if curl -s -f http://localhost:8001/health > /dev/null; then
    echo "✅ API Gateway健康检查通过"
else
    echo "❌ API Gateway健康检查失败"
fi

echo "测试Frontend服务..."
if curl -s -f http://localhost:3000 > /dev/null; then
    echo "✅ Frontend服务正常"
else
    echo "❌ Frontend服务异常"
fi

echo "🎉 容器更新完成！"
echo ""
echo "📋 服务访问地址："
echo "• 前端应用: http://localhost:3000"
echo "• API Gateway: http://localhost:8001"
echo "• AI Service: http://localhost:8002"
echo "• Video Service: http://localhost:8003"
echo ""
echo "📋 下一步操作："
echo "1. 运行端到端测试: sudo docker exec -it tfboys-api-gateway ./test_e2e.sh"
echo "2. 查看服务日志: sudo docker compose logs -f"
echo "3. 访问前端应用: http://localhost:3000"
