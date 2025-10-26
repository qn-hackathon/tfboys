#!/bin/bash
# TFBoys Docker 部署脚本
# 快速部署 AI Service 测试环境

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":$port "; then
        print_warning "端口 $port 已被占用"
        return 1
    fi
    return 0
}

# 检查环境
check_environment() {
    print_header "步骤 1: 环境检查"
    
    print_info "检查 Docker..."
    check_command docker
    DOCKER_VERSION=$(docker --version)
    print_success "Docker 已安装: $DOCKER_VERSION"
    
    print_info "检查 Docker Compose..."
    check_command docker
    if docker compose version &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version)
        print_success "Docker Compose 已安装: $COMPOSE_VERSION"
    else
        print_error "Docker Compose V2 未安装"
        exit 1
    fi
    
    print_info "检查端口占用..."
    PORTS_TO_CHECK=(6379 8001 8002 8003 3000)
    PORT_CONFLICT=0
    
    for port in "${PORTS_TO_CHECK[@]}"; do
        if ! check_port $port; then
            PORT_CONFLICT=1
        fi
    done
    
    if [ $PORT_CONFLICT -eq 1 ]; then
        print_warning "存在端口冲突，请停止占用端口的服务或修改 docker-compose.yml 中的端口映射"
        read -p "是否继续部署? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "部署已取消"
            exit 0
        fi
    else
        print_success "所有端口可用"
    fi
}

# 配置环境变量
setup_env() {
    print_header "步骤 2: 配置环境变量"
    
    if [ ! -f "backend/ai-service/.env" ]; then
        print_info "复制 AI Service 环境变量模板..."
        cp backend/ai-service/.env.example backend/ai-service/.env
        print_success "已创建 backend/ai-service/.env"
        
        print_warning "请编辑 backend/ai-service/.env 文件，填写真实的 QINIU_API_KEY"
        print_info "获取方式: https://portal.qiniu.com/kodo/ak-sk"
        echo ""
        read -p "按 Enter 键打开编辑器..." 
        
        # 尝试使用可用的编辑器
        if command -v vim &> /dev/null; then
            vim backend/ai-service/.env
        elif command -v nano &> /dev/null; then
            nano backend/ai-service/.env
        elif command -v vi &> /dev/null; then
            vi backend/ai-service/.env
        else
            print_warning "未找到文本编辑器，请手动编辑 backend/ai-service/.env"
            return
        fi
    else
        print_info "AI Service .env 文件已存在"
    fi
    
    # 检查 QINIU_API_KEY 是否配置
    if grep -q "your-qiniu-ai-token-api-key" backend/ai-service/.env; then
        print_error "QINIU_API_KEY 未配置，请编辑 backend/ai-service/.env 文件"
        exit 1
    fi
    
    print_success "环境变量配置完成"
}

# 构建镜像
build_images() {
    print_header "步骤 3: 构建 Docker 镜像"
    
    print_info "开始构建镜像 (这可能需要几分钟)..."
    docker compose build
    
    print_success "镜像构建完成"
}

# 启动服务
start_services() {
    print_header "步骤 4: 启动服务"
    
    print_info "启动所有服务..."
    docker compose up -d
    
    print_info "等待服务启动..."
    sleep 10
    
    print_success "服务启动完成"
}

# 验证服务
verify_services() {
    print_header "步骤 5: 验证服务"
    
    print_info "检查容器状态..."
    docker compose ps
    echo ""
    
    print_info "测试 Redis 连接..."
    if docker exec tfboys-redis redis-cli ping | grep -q "PONG"; then
        print_success "Redis 连接正常"
    else
        print_error "Redis 连接失败"
        return 1
    fi
    
    print_info "等待服务健康检查..."
    sleep 5
    
    print_info "测试 AI Service..."
    if curl -s -f http://localhost:8002/health > /dev/null 2>&1; then
        RESPONSE=$(curl -s http://localhost:8002/health)
        print_success "AI Service 正常运行: $RESPONSE"
    else
        print_error "AI Service 未响应"
        print_info "查看日志: docker compose logs ai-service"
        return 1
    fi
    
    print_info "测试 Video Service..."
    if curl -s -f http://localhost:8003/health > /dev/null 2>&1; then
        RESPONSE=$(curl -s http://localhost:8003/health)
        print_success "Video Service 正常运行: $RESPONSE"
    else
        print_warning "Video Service 未响应 (如果未配置 Video Service，可以忽略)"
    fi
    
    print_info "测试 API Gateway..."
    if curl -s -f http://localhost:8001/ > /dev/null 2>&1; then
        RESPONSE=$(curl -s http://localhost:8001/)
        print_success "API Gateway 正常运行: $RESPONSE"
    else
        print_warning "API Gateway 未响应"
    fi
}

# 运行端到端测试
run_e2e_test() {
    print_header "步骤 6: 运行端到端测试 (可选)"
    
    read -p "是否运行端到端测试? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "运行 AI Service 端到端测试..."
        docker exec -it tfboys-ai-service bash -c "cd /app && ./test_e2e.sh"
    else
        print_info "跳过端到端测试"
    fi
}

# 显示访问信息
show_access_info() {
    print_header "部署完成"
    
    echo -e "${GREEN}✅ TFBoys AI Service 测试环境部署成功!${NC}"
    echo ""
    echo "服务访问地址:"
    echo "  - API Gateway:  http://localhost:8001"
    echo "  - AI Service:   http://localhost:8002"
    echo "  - Video Service: http://localhost:8003"
    echo "  - Frontend:     http://localhost:3000 (如果启动)"
    echo ""
    echo "常用命令:"
    echo "  - 查看服务状态:  docker compose ps"
    echo "  - 查看日志:      docker compose logs -f"
    echo "  - 查看 AI 日志:  docker compose logs -f ai-service"
    echo "  - 停止服务:      docker compose stop"
    echo "  - 重启服务:      docker compose restart"
    echo "  - 删除服务:      docker compose down"
    echo ""
    echo "测试方法:"
    echo "  1. 使用脚本测试:  docker exec -it tfboys-ai-service ./test_e2e.sh"
    echo "  2. 手动 API 测试: 见 DOCKER_DEPLOYMENT_GUIDE.md"
    echo ""
    echo "详细文档: DOCKER_DEPLOYMENT_GUIDE.md"
    echo ""
}

# 主函数
main() {
    print_header "TFBoys AI Service Docker 部署"
    
    # 检查是否在项目根目录
    if [ ! -f "docker-compose.yml" ]; then
        print_error "请在项目根目录运行此脚本"
        exit 1
    fi
    
    # 执行部署步骤
    check_environment
    setup_env
    build_images
    start_services
    verify_services
    run_e2e_test
    show_access_info
}

# 运行主函数
main
