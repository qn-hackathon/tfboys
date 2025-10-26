#!/bin/bash

# AI Service Docker 环境测试脚本
# 用于验证 Docker 部署的 AI Service 是否正常工作

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
AI_SERVICE_URL="http://localhost:8002"
VIDEO_SERVICE_URL="http://localhost:8003"
API_GATEWAY_URL="http://localhost:8001"
TEST_TASK_ID="test_docker_$(date +%s)"
MAX_WAIT_TIME=300  # 最大等待时间（秒）

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装"
        exit 1
    fi
}

# 检查 Docker 服务状态
check_docker_services() {
    print_header "检查 Docker 服务状态"
    
    # 检查必需的服务
    REQUIRED_SERVICES=("tfboys-redis" "tfboys-ai-service" "tfboys-ai-worker")
    
    for service in "${REQUIRED_SERVICES[@]}"; do
        if docker ps --format '{{.Names}}' | grep -q "^${service}$"; then
            STATUS=$(docker inspect --format='{{.State.Status}}' $service)
            if [ "$STATUS" = "running" ]; then
                print_success "$service 运行中"
            else
                print_error "$service 状态异常: $STATUS"
                exit 1
            fi
        else
            print_error "$service 未运行"
            print_info "请先启动服务: docker-compose up -d"
            exit 1
        fi
    done
    
    # 检查可选服务
    OPTIONAL_SERVICES=("tfboys-video-service" "tfboys-video-worker" "tfboys-api-gateway")
    
    for service in "${OPTIONAL_SERVICES[@]}"; do
        if docker ps --format '{{.Names}}' | grep -q "^${service}$"; then
            print_success "$service 运行中"
        else
            print_warning "$service 未运行（可选）"
        fi
    done
}

# 健康检查
health_check() {
    print_header "健康检查"
    
    # Redis
    print_info "检查 Redis..."
    if docker exec tfboys-redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis 健康"
    else
        print_error "Redis 不健康"
        exit 1
    fi
    
    # AI Service
    print_info "检查 AI Service..."
    if curl -s -f "$AI_SERVICE_URL/health" > /dev/null; then
        HEALTH=$(curl -s "$AI_SERVICE_URL/health" | jq -r '.status')
        if [ "$HEALTH" = "healthy" ]; then
            print_success "AI Service 健康"
        else
            print_error "AI Service 不健康: $HEALTH"
            exit 1
        fi
    else
        print_error "AI Service 无响应"
        exit 1
    fi
    
    # Video Service（如果运行）
    if docker ps --format '{{.Names}}' | grep -q "^tfboys-video-service$"; then
        print_info "检查 Video Service..."
        if curl -s -f "$VIDEO_SERVICE_URL/health" > /dev/null; then
            print_success "Video Service 健康"
        else
            print_warning "Video Service 无响应"
        fi
    fi
    
    # API Gateway（如果运行）
    if docker ps --format '{{.Names}}' | grep -q "^tfboys-api-gateway$"; then
        print_info "检查 API Gateway..."
        if curl -s -f "$API_GATEWAY_URL/health" > /dev/null; then
            print_success "API Gateway 健康"
        else
            print_warning "API Gateway 无响应"
        fi
    fi
}

# 检查 Celery Worker
check_celery_worker() {
    print_header "检查 Celery Worker"
    
    print_info "检查 AI Worker 注册的任务..."
    REGISTERED_TASKS=$(docker exec tfboys-ai-worker celery -A app.workers.celery_app inspect registered 2>&1)
    
    if echo "$REGISTERED_TASKS" | grep -q "process_novel_task"; then
        print_success "AI Worker 已注册 process_novel_task"
    else
        print_error "AI Worker 未注册必需的任务"
        echo "$REGISTERED_TASKS"
        exit 1
    fi
    
    print_info "检查 AI Worker 活跃任务..."
    ACTIVE_TASKS=$(docker exec tfboys-ai-worker celery -A app.workers.celery_app inspect active 2>&1)
    print_success "AI Worker 状态正常"
}

# 检查存储目录
check_storage() {
    print_header "检查存储目录"
    
    print_info "检查 /tmp/tfboys 目录..."
    if docker exec tfboys-ai-service test -d /tmp/tfboys; then
        print_success "/tmp/tfboys 目录存在"
        
        # 测试写入权限
        if docker exec tfboys-ai-service touch /tmp/tfboys/.test_write 2>/dev/null; then
            docker exec tfboys-ai-service rm /tmp/tfboys/.test_write
            print_success "/tmp/tfboys 可写"
        else
            print_error "/tmp/tfboys 不可写"
            exit 1
        fi
    else
        print_error "/tmp/tfboys 目录不存在"
        exit 1
    fi
}

# 创建测试任务
create_test_task() {
    print_header "创建测试任务"
    
    print_info "任务ID: $TEST_TASK_ID"
    
    RESPONSE=$(curl -s -X POST "$AI_SERVICE_URL/internal/tasks" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_id\": \"$TEST_TASK_ID\",
            \"novel_text\": \"小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。\"
        }")
    
    STATUS=$(echo $RESPONSE | jq -r '.status')
    
    if [ "$STATUS" = "pending" ]; then
        print_success "任务创建成功"
        echo "$RESPONSE" | jq '.'
    else
        print_error "任务创建失败"
        echo "$RESPONSE" | jq '.'
        exit 1
    fi
}

# 监控任务进度
monitor_task() {
    print_header "监控任务进度"
    
    print_info "等待任务完成（最多 ${MAX_WAIT_TIME} 秒）..."
    
    START_TIME=$(date +%s)
    LAST_STATUS=""
    
    while true; do
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        
        if [ $ELAPSED -gt $MAX_WAIT_TIME ]; then
            print_error "任务超时（超过 ${MAX_WAIT_TIME} 秒）"
            print_info "查看日志: docker-compose logs ai-worker"
            exit 1
        fi
        
        RESPONSE=$(curl -s "$AI_SERVICE_URL/internal/tasks/$TEST_TASK_ID")
        STATUS=$(echo $RESPONSE | jq -r '.status')
        PROGRESS=$(echo $RESPONSE | jq -r '.progress.percentage // 0')
        CURRENT_STAGE=$(echo $RESPONSE | jq -r '.progress.current_stage // "unknown"')
        
        # 只在状态变化时打印
        if [ "$STATUS" != "$LAST_STATUS" ]; then
            print_info "状态: $STATUS | 进度: $PROGRESS% | 阶段: $CURRENT_STAGE"
            LAST_STATUS=$STATUS
        fi
        
        if [ "$STATUS" = "completed" ]; then
            print_success "任务完成！"
            echo "$RESPONSE" | jq '.'
            break
        elif [ "$STATUS" = "failed" ]; then
            print_error "任务失败"
            echo "$RESPONSE" | jq '.'
            
            print_info "查看 AI Service 日志:"
            docker-compose logs --tail=50 ai-service
            
            print_info "查看 AI Worker 日志:"
            docker-compose logs --tail=50 ai-worker
            
            exit 1
        fi
        
        sleep 3
    done
}

# 验证结果
verify_results() {
    print_header "验证结果"
    
    RESPONSE=$(curl -s "$AI_SERVICE_URL/internal/tasks/$TEST_TASK_ID")
    
    # 检查状态
    STATUS=$(echo $RESPONSE | jq -r '.status')
    if [ "$STATUS" = "completed" ]; then
        print_success "任务状态: completed"
    else
        print_error "任务状态异常: $STATUS"
        exit 1
    fi
    
    # 检查进度
    PROGRESS=$(echo $RESPONSE | jq -r '.progress.percentage')
    if [ "$PROGRESS" = "100" ]; then
        print_success "任务进度: 100%"
    else
        print_warning "任务进度: $PROGRESS%"
    fi
    
    # 检查场景数量
    TOTAL_SCENES=$(echo $RESPONSE | jq -r '.progress.total_scenes // 0')
    PROCESSED_SCENES=$(echo $RESPONSE | jq -r '.progress.processed_scenes // 0')
    print_success "场景处理: $PROCESSED_SCENES / $TOTAL_SCENES"
    
    # 检查结果数据
    HAS_RESULT=$(echo $RESPONSE | jq 'has("result")')
    if [ "$HAS_RESULT" = "true" ]; then
        print_success "包含结果数据"
        
        # 检查场景列表
        SCENES_COUNT=$(echo $RESPONSE | jq '.result.scenes | length')
        print_info "生成场景数: $SCENES_COUNT"
        
        # 检查视频 URL
        VIDEO_URL=$(echo $RESPONSE | jq -r '.result.video_url // ""')
        if [ -n "$VIDEO_URL" ]; then
            print_success "视频 URL: $VIDEO_URL"
        else
            print_warning "未生成视频 URL（Video Service 可能未运行）"
        fi
    else
        print_warning "未包含结果数据"
    fi
}

# 清理测试数据
cleanup() {
    print_header "清理测试数据"
    
    print_info "删除 Redis 中的测试任务数据..."
    docker exec tfboys-redis redis-cli DEL "task:$TEST_TASK_ID" > /dev/null 2>&1 || true
    
    print_success "清理完成"
}

# 主函数
main() {
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║   AI Service Docker 环境测试脚本      ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    
    # 检查依赖
    print_info "检查依赖工具..."
    check_command "docker"
    check_command "curl"
    check_command "jq"
    print_success "依赖工具检查通过"
    
    # 执行测试步骤
    check_docker_services
    health_check
    check_celery_worker
    check_storage
    create_test_task
    monitor_task
    verify_results
    
    # 询问是否清理
    echo ""
    read -p "是否清理测试数据？(y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup
    else
        print_info "测试数据保留，任务ID: $TEST_TASK_ID"
        print_info "手动查看: curl $AI_SERVICE_URL/internal/tasks/$TEST_TASK_ID"
    fi
    
    # 测试成功
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║      ✓ 所有测试通过！               ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    print_success "AI Service Docker 环境运行正常"
    echo ""
    print_info "下一步："
    echo "  - 查看 API 文档: $AI_SERVICE_URL/docs"
    echo "  - 查看日志: docker-compose logs -f ai-service ai-worker"
    echo "  - 监控资源: docker stats tfboys-ai-service tfboys-ai-worker"
    echo ""
}

# 捕获 Ctrl+C
trap 'echo ""; print_warning "测试中断"; exit 130' INT

# 运行主函数
main
