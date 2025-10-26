#!/bin/bash
# API Gateway 端到端测试脚本

set -e

echo "🚪 API Gateway 端到端测试"
echo "================================"

# 配置变量
API_GATEWAY_URL="http://localhost:8001"
TEST_NOVEL_TEXT="小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
check_gateway() {
    echo -e "\n${YELLOW}1. 检查 API Gateway 是否运行...${NC}"
    if curl -s -f "${API_GATEWAY_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API Gateway 正在运行${NC}"
        return 0
    else
        echo -e "${RED}❌ API Gateway 未运行${NC}"
        echo "请先启动服务:"
        echo "  cd backend/api-gateway"
        echo "  export PYTHONPATH=\"\$(cd ../.. && pwd)\""
        echo "  uvicorn app.main:app --reload --port 8001"
        return 1
    fi
}

check_ai_service() {
    echo -e "\n${YELLOW}2. 检查 AI Service 是否运行...${NC}"
    if curl -s -f "http://localhost:8002/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ AI Service 正在运行${NC}"
        return 0
    else
        echo -e "${RED}❌ AI Service 未运行${NC}"
        echo "请先启动 AI Service (端口 8002)"
        return 1
    fi
}

create_task() {
    echo -e "\n${YELLOW}3. 创建视频生成任务 (通过 Gateway)...${NC}"
    
    # 发送请求
    RESPONSE=$(curl -s -X POST "${API_GATEWAY_URL}/api/tasks" \
        -H "Content-Type: application/json" \
        -d "{
            \"novel_text\": \"${TEST_NOVEL_TEXT}\"
        }")
    
    # 检查响应码
    CODE=$(echo "$RESPONSE" | grep -o '"code":[0-9]*' | cut -d':' -f2 || echo "")
    
    # 提取任务ID (从 data 字段中)
    TASK_ID=$(echo "$RESPONSE" | jq -r '.data.task_id' 2>/dev/null || echo "")
    
    # 检查响应
    if [ "$CODE" = "0" ] && [ -n "$TASK_ID" ]; then
        echo -e "${GREEN}✅ 任务创建成功${NC}"
        echo "任务ID: $TASK_ID"
        echo "响应: $RESPONSE"
        echo "$TASK_ID" > /tmp/test_task_id_gateway.txt
        return 0
    else
        echo -e "${RED}❌ 任务创建失败${NC}"
        echo "响应: $RESPONSE"
        return 1
    fi
}

get_task_detail() {
    if [ ! -f /tmp/test_task_id_gateway.txt ]; then
        echo -e "${RED}❌ 未找到任务ID文件${NC}"
        return 1
    fi
    
    TASK_ID=$(cat /tmp/test_task_id_gateway.txt)
    echo -e "\n${YELLOW}4. 获取任务详情 (任务ID: $TASK_ID)...${NC}"
    
    RESPONSE=$(curl -s "${API_GATEWAY_URL}/api/tasks/${TASK_ID}")
    
    # 检查响应码
    CODE=$(echo "$RESPONSE" | grep -o '"code":[0-9]*' | cut -d':' -f2 || echo "")
    
    if [ "$CODE" = "0" ]; then
        echo -e "${GREEN}✅ 成功获取任务详情${NC}"
        echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        return 0
    else
        echo -e "${RED}❌ 获取任务失败${NC}"
        echo "响应: $RESPONSE"
        return 1
    fi
}

list_tasks() {
    echo -e "\n${YELLOW}5. 获取任务列表...${NC}"
    
    RESPONSE=$(curl -s "${API_GATEWAY_URL}/api/tasks")
    
    # 检查响应码
    CODE=$(echo "$RESPONSE" | grep -o '"code":[0-9]*' | cut -d':' -f2 || echo "")
    
    if [ "$CODE" = "0" ]; then
        TASK_COUNT=$(echo "$RESPONSE" | jq '.data | length' 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✅ 成功获取任务列表${NC}"
        echo "任务数量: $TASK_COUNT"
        echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        return 0
    else
        echo -e "${RED}❌ 获取任务列表失败${NC}"
        echo "响应: $RESPONSE"
        return 1
    fi
}

test_cors() {
    echo -e "\n${YELLOW}6. 测试 CORS 配置...${NC}"
    
    RESPONSE=$(curl -s -I -X OPTIONS "${API_GATEWAY_URL}/api/tasks" \
        -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST")
    
    if echo "$RESPONSE" | grep -q "access-control-allow-origin"; then
        echo -e "${GREEN}✅ CORS 配置正确${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  CORS 响应头未找到${NC}"
        return 0
    fi
}

# 执行测试
if check_gateway; then
    if check_ai_service; then
        if create_task; then
            get_task_detail
            list_tasks
            test_cors
            
            echo -e "\n${GREEN}================================${NC}"
            echo -e "${GREEN}✅ API Gateway 测试完成!${NC}"
            echo -e "${GREEN}================================${NC}"
        fi
    fi
fi
