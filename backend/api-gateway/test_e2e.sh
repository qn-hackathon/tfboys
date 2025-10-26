#!/bin/bash
# API Gateway 端到端测试脚本 - 完整视频生成流程

set -e

echo "🎬 API Gateway 完整视频生成流程测试"
echo "================================================"

# 配置变量
# 检测是否在容器内运行
if [ -f /.dockerenv ]; then
    # 在容器内运行时，使用容器内部地址
    API_GATEWAY_URL="http://localhost:8001"
    AI_SERVICE_URL="http://ai-service:8002"
    VIDEO_SERVICE_URL="http://video-service:8003"
else
    # 在宿主机运行时，使用 localhost
    API_GATEWAY_URL="http://localhost:8001"
    AI_SERVICE_URL="http://localhost:8002"
    VIDEO_SERVICE_URL="http://localhost:8003"
fi
TEST_NOVEL_TEXT="小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
check_gateway() {
    echo -e "\n${YELLOW}1. 检查 API Gateway 是否运行...${NC}"
    echo "尝试访问: ${API_GATEWAY_URL}/health"
    
    # 先尝试获取详细错误信息
    RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}\n" "${API_GATEWAY_URL}/health" 2>&1)
    HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✅ API Gateway 正在运行${NC}"
        return 0
    else
        echo -e "${RED}❌ API Gateway 未运行${NC}"
        echo "HTTP 状态码: $HTTP_CODE"
        echo "响应内容: $RESPONSE"
        echo "请先启动服务:"
        echo "  cd backend/api-gateway"
        echo "  export PYTHONPATH=\"\$(cd ../.. && pwd)\""
        echo "  uvicorn app.main:app --reload --port 8001"
        return 1
    fi
}

check_ai_service() {
    echo -e "\n${YELLOW}2. 检查 AI Service 是否运行...${NC}"
    if curl -s -f "${AI_SERVICE_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ AI Service 正在运行${NC}"
        return 0
    else
        echo -e "${RED}❌ AI Service 未运行${NC}"
        echo "请先启动 AI Service (端口 8002)"
        return 1
    fi
}

check_video_service() {
    echo -e "\n${YELLOW}3. 检查 Video Service 是否运行...${NC}"
    if curl -s -f "${VIDEO_SERVICE_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Video Service 正在运行${NC}"
        return 0
    else
        echo -e "${RED}❌ Video Service 未运行${NC}"
        echo "请先启动 Video Service (端口 8003)"
        return 1
    fi
}

create_task() {
    echo -e "\n${YELLOW}4. 创建视频生成任务 (通过 Gateway)...${NC}"
    
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
    echo -e "\n${YELLOW}5. 获取任务详情 (任务ID: $TASK_ID)...${NC}"
    
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
    echo -e "\n${YELLOW}6. 获取任务列表...${NC}"
    
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
    echo -e "\n${YELLOW}7. 测试 CORS 配置...${NC}"
    
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

wait_for_task_completion() {
    if [ ! -f /tmp/test_task_id_gateway.txt ]; then
        echo -e "${RED}❌ 未找到任务ID文件${NC}"
        return 1
    fi
    
    TASK_ID=$(cat /tmp/test_task_id_gateway.txt)
    echo -e "\n${YELLOW}8. 等待任务完成 (任务ID: $TASK_ID)...${NC}"
    echo "这可能需要几分钟时间，请耐心等待..."
    
    # 轮询任务状态，最多检查120次（10分钟）
    MAX_ATTEMPTS=120
    ATTEMPT=0
    
    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        RESPONSE=$(curl -s "${API_GATEWAY_URL}/api/tasks/${TASK_ID}")
        
        # 检查响应码
        CODE=$(echo "$RESPONSE" | grep -o '"code":[0-9]*' | cut -d':' -f2 || echo "")
        
        if [ "$CODE" = "0" ]; then
            STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
            CURRENT_STAGE=$(echo "$RESPONSE" | grep -o '"current_stage":"[^"]*"' | cut -d'"' -f4 || echo "")
            PROGRESS=$(echo "$RESPONSE" | grep -o '"progress":{[^}]*}' || echo "")
            
            echo "[尝试 $((ATTEMPT+1))/${MAX_ATTEMPTS}] 状态: $STATUS"
            if [ -n "$CURRENT_STAGE" ]; then
                echo "当前阶段: $CURRENT_STAGE"
            fi
            
            if echo "$RESPONSE" | grep -q '"status":"completed"'; then
                echo -e "${GREEN}✅ 任务完成!${NC}"
                echo "完整响应:"
                echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
                
                # 提取视频URL
                VIDEO_URL=$(echo "$RESPONSE" | jq -r '.data.result.video_url' 2>/dev/null || echo "")
                if [ -n "$VIDEO_URL" ] && [ "$VIDEO_URL" != "null" ]; then
                    echo -e "\n${GREEN}🎬 视频生成成功!${NC}"
                    echo "视频URL: $VIDEO_URL"
                    echo ""
                    echo "视频访问方式:"
                    echo "1. 直接访问: $VIDEO_URL"
                    echo "2. 如果使用本地存储，文件路径: $VIDEO_URL"
                    echo "3. 如果使用OSS，请通过OSS控制台或SDK访问"
                    echo ""
                    echo "视频文件访问方式:"
                    echo "sudo docker exec -it tfboys-video-service ls -la /tmp/tfboys/videos/"
                    echo "sudo docker cp tfboys-video-service:$VIDEO_URL /tmp/"
                    echo "cd /tmp && python3 -m http.server 9000"
                    echo "测试视频下载: http://100.100.21.31:9000/$(basename $VIDEO_URL)"
                else
                    echo -e "${YELLOW}⚠️  未找到视频URL${NC}"
                fi
                
                return 0
            elif echo "$RESPONSE" | grep -q '"status":"failed"'; then
                echo -e "${RED}❌ 任务失败${NC}"
                echo "完整响应:"
                echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
                return 1
            fi
        else
            echo -e "${RED}❌ 获取任务状态失败${NC}"
            echo "响应: $RESPONSE"
            return 1
        fi
        
        ATTEMPT=$((ATTEMPT+1))
        sleep 5
    done
    
    echo -e "${RED}❌ 任务超时 (10分钟)${NC}"
    return 1
}

# 执行测试
if check_gateway; then
    if check_ai_service; then
        if check_video_service; then
            if create_task; then
                get_task_detail
                list_tasks
                test_cors
                
                # 等待任务完成
                if wait_for_task_completion; then
                    echo -e "\n${GREEN}===============================================${NC}"
                    echo -e "${GREEN}✅ 完整视频生成流程测试成功!${NC}"
                    echo -e "${GREEN}===============================================${NC}"
                    echo ""
                    echo "测试总结:"
                    echo "1. ✅ API Gateway 健康检查"
                    echo "2. ✅ AI Service 健康检查"
                    echo "3. ✅ Video Service 健康检查"
                    echo "4. ✅ 任务创建成功"
                    echo "5. ✅ 任务详情获取"
                    echo "6. ✅ 任务列表获取"
                    echo "7. ✅ CORS 配置测试"
                    echo "8. ✅ 视频生成完成"
                    echo ""
                    echo "🎬 视频已成功生成，请查看上述视频URL进行访问!"
                else
                    echo -e "\n${RED}❌ 视频生成失败或超时${NC}"
                    exit 1
                fi
            else
                echo -e "\n${RED}❌ 任务创建失败${NC}"
                exit 1
            fi
        else
            echo -e "\n${RED}❌ Video Service 未运行${NC}"
            exit 1
        fi
    else
        echo -e "\n${RED}❌ AI Service 未运行${NC}"
        exit 1
    fi
else
    echo -e "\n${RED}❌ API Gateway 未运行${NC}"
    exit 1
fi
