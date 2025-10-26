#!/bin/bash
# AI Service 完整启动脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 启动 AI Service 环境${NC}"
echo "================================"

# 检查 Redis
echo -e "\n${YELLOW}1. 检查 Redis...${NC}"
if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis 正在运行${NC}"
else
    echo -e "${RED}❌ Redis 未运行，尝试启动...${NC}"
    docker-compose up -d redis 2>/dev/null || \
    docker run -d --name redis -p 6379:6379 redis:latest 2>/dev/null || \
    (echo -e "${RED}无法启动 Redis，请手动启动${NC}" && exit 1)
    echo -e "${GREEN}✅ Redis 已启动${NC}"
fi

# 设置 PYTHONPATH
export PYTHONPATH="$(cd ../.. && pwd)"
echo -e "\n${YELLOW}2. 设置 PYTHONPATH: $PYTHONPATH${NC}"

# 检查环境变量
echo -e "\n${YELLOW}3. 检查环境变量...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env 文件不存在${NC}"
    echo "请创建 .env 文件并设置 QINIU_API_KEY"
    echo "参考: E2E_TESTING.md"
    exit 1
fi

# 加载环境变量
source .env
if [ -z "$QINIU_API_KEY" ]; then
    echo -e "${RED}⚠️  QINIU_API_KEY 未设置${NC}"
    echo "请在 .env 文件中设置"
fi

echo -e "${GREEN}✅ 环境配置完成${NC}"

# 启动服务
echo -e "\n${YELLOW}4. 启动服务...${NC}"
echo -e "${GREEN}正在启动 AI Service API (端口 8002)...${NC}"

# 注意：这将在前台运行
# 要后台运行，可以使用: nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8002 > /tmp/ai_service.log 2>&1 &
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002

