#!/bin/bash
# AI Service 端到端测试脚本

set -e

echo "🎬 AI Service 端到端测试"
echo "================================"

# 配置变量
AI_SERVICE_URL="http://localhost:8002"
TEST_NOVEL_TEXT="小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
check_service() {
    echo -e "\n${YELLOW}1. 检查 AI Service 是否运行...${NC}"
    if curl -s -f "${AI_SERVICE_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ AI Service 正在运行${NC}"
        return 0
    else
        echo -e "${RED}❌ AI Service 未运行${NC}"
        echo "请先启动服务:"
        echo "  cd backend/ai-service"
        echo "  export PYTHONPATH=\"\$(cd ../.. && pwd)\""
        echo "  uvicorn app.main:app --reload --port 8002"
        return 1
    fi
}

create_task() {
    echo -e "\n${YELLOW}2. 创建视频生成任务...${NC}"
    
    # 生成任务ID
    TASK_ID="test_$(date +%s)"
    
    # 发送请求
    RESPONSE=$(curl -s -X POST "${AI_SERVICE_URL}/internal/tasks" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_id\": \"${TASK_ID}\",
            \"novel_text\": \"${TEST_NOVEL_TEXT}\"
        }")
    
    # 检查响应
    if echo "$RESPONSE" | grep -q "task_id"; then
        echo -e "${GREEN}✅ 任务创建成功${NC}"
        echo "任务ID: $TASK_ID"
        echo "响应: $RESPONSE"
        echo "$TASK_ID" > /tmp/test_task_id.txt
        return 0
    else
        echo -e "${RED}❌ 任务创建失败${NC}"
        echo "响应: $RESPONSE"
        return 1
    fi
}

check_task_status() {
    if [ ! -f /tmp/test_task_id.txt ]; then
        echo -e "${RED}❌ 未找到任务ID文件${NC}"
        return 1
    fi
    
    TASK_ID=$(cat /tmp/test_task_id.txt)
    echo -e "\n${YELLOW}3. 检查任务状态 (任务ID: $TASK_ID)...${NC}"
    
    # 轮询任务状态，最多检查60次（5分钟）
    MAX_ATTEMPTS=60
    ATTEMPT=0
    
    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        RESPONSE=$(curl -s "${AI_SERVICE_URL}/internal/tasks/${TASK_ID}")
        
        STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
        PROGRESS=$(echo "$RESPONSE" | grep -o '"progress":{[^}]*}' || echo "")
        
        echo "[尝试 $((ATTEMPT+1))/${MAX_ATTEMPTS}] 状态: $STATUS"
        
        if echo "$RESPONSE" | grep -q '"status":"completed"'; then
            echo -e "${GREEN}✅ 任务完成!${NC}"
            echo "完整响应:"
            echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
            return 0
        elif echo "$RESPONSE" | grep -q '"status":"failed"'; then
            echo -e "${RED}❌ 任务失败${NC}"
            echo "完整响应:"
            echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
            return 1
        fi
        
        ATTEMPT=$((ATTEMPT+1))
        sleep 5
    done
    
    echo -e "${RED}❌ 任务超时${NC}"
    return 1
}

# 执行测试
if check_service; then
    if create_task; then
        check_task_status
    fi
fi

