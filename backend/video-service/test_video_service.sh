#!/bin/bash

set -e

echo "=========================================="
echo "Video Service 测试脚本"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8003"

echo "测试 1: 健康检查"
echo "----------------------------------------"
response=$(curl -s "${BASE_URL}/health")
echo "响应: $response"
if echo "$response" | grep -q "healthy"; then
    echo "✅ 健康检查通过"
else
    echo "❌ 健康检查失败"
    exit 1
fi
echo ""

echo "测试 2: 根路径访问"
echo "----------------------------------------"
response=$(curl -s "${BASE_URL}/")
echo "响应: $response"
if echo "$response" | grep -q "TFBoys Video Service"; then
    echo "✅ 根路径访问成功"
else
    echo "❌ 根路径访问失败"
    exit 1
fi
echo ""

echo "测试 3: FFmpeg 版本检查"
echo "----------------------------------------"
docker-compose exec -T video-service ffmpeg -version | head -n 1
if [ $? -eq 0 ]; then
    echo "✅ FFmpeg 安装正常"
else
    echo "❌ FFmpeg 未安装或异常"
    exit 1
fi
echo ""

echo "测试 4: 中文字体检查"
echo "----------------------------------------"
font_check=$(docker-compose exec -T video-service fc-list | grep -i wqy | wc -l)
if [ "$font_check" -gt 0 ]; then
    echo "✅ 中文字体安装正常 (找到 $font_check 个字体)"
else
    echo "❌ 中文字体未安装"
    exit 1
fi
echo ""

echo "测试 5: Redis 连接检查"
echo "----------------------------------------"
redis_response=$(docker-compose exec -T redis redis-cli ping)
if echo "$redis_response" | grep -q "PONG"; then
    echo "✅ Redis 连接正常"
else
    echo "❌ Redis 连接失败"
    exit 1
fi
echo ""

echo "测试 6: Python 依赖检查"
echo "----------------------------------------"
echo "检查关键依赖包..."
docker-compose exec -T video-service python -c "
import fastapi
import celery
import redis
import PIL
print('✅ 所有 Python 依赖包正常')
"
echo ""

echo "测试 7: 本地存储目录权限检查"
echo "----------------------------------------"
docker-compose exec -T video-service ls -ld /tmp/tfboys
if [ $? -eq 0 ]; then
    echo "✅ 本地存储目录存在且可访问"
    docker-compose exec -T video-service python -c "
import os
storage_dir = '/tmp/tfboys'
test_file = os.path.join(storage_dir, 'test_write.txt')
try:
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print('✅ 存储目录可写入')
except Exception as e:
    print(f'❌ 存储目录写入失败: {e}')
    exit(1)
"
else
    echo "❌ 本地存储目录不存在或无权限"
    exit 1
fi
echo ""

echo "测试 8: API 文档访问"
echo "----------------------------------------"
response=$(curl -s "${BASE_URL}/docs")
if [ -n "$response" ]; then
    echo "✅ API 文档可访问: ${BASE_URL}/docs"
else
    echo "❌ API 文档访问失败"
    exit 1
fi
echo ""

echo "测试 9: Celery Worker 状态"
echo "----------------------------------------"
docker-compose exec -T celery-worker celery -A app.workers.celery_app inspect ping
if [ $? -eq 0 ]; then
    echo "✅ Celery Worker 运行正常"
else
    echo "❌ Celery Worker 未运行或异常"
    exit 1
fi
echo ""

echo "=========================================="
echo "✅ 所有基础测试通过！"
echo "=========================================="
echo ""
echo "下一步操作建议："
echo "1. 访问 API 文档: http://localhost:8003/docs"
echo "2. 查看服务日志: docker-compose logs -f"
echo "3. 运行完整视频合成测试（需要真实的图片和音频 URL）"
echo ""
