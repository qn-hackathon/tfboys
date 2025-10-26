#!/bin/bash
# 前端 Docker 构建和部署脚本

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

# 检查 Docker 是否安装
check_docker() {
    print_header "步骤 1: 环境检查"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    DOCKER_VERSION=$(docker --version)
    print_success "Docker 已安装: $DOCKER_VERSION"
}

# 构建 Docker 镜像
build_image() {
    print_header "步骤 2: 构建 Docker 镜像"
    
    print_info "开始构建前端 Docker 镜像..."
    docker build -t tfboys-frontend:latest .
    
    print_success "镜像构建完成"
}

# 运行容器
run_container() {
    print_header "步骤 3: 运行容器"
    
    # 停止并删除旧容器(如果存在)
    if docker ps -a | grep -q tfboys-frontend; then
        print_info "停止并删除旧容器..."
        docker stop tfboys-frontend 2>/dev/null || true
        docker rm tfboys-frontend 2>/dev/null || true
    fi
    
    print_info "启动前端容器..."
    docker run -d \
        --name tfboys-frontend \
        -p 3000:80 \
        tfboys-frontend:latest
    
    print_info "等待容器启动..."
    sleep 3
    
    print_success "容器启动完成"
}

# 验证部署
verify_deployment() {
    print_header "步骤 4: 验证部署"
    
    print_info "检查容器状态..."
    if docker ps | grep -q tfboys-frontend; then
        print_success "容器运行正常"
    else
        print_error "容器未运行"
        print_info "查看日志: docker logs tfboys-frontend"
        exit 1
    fi
    
    print_info "测试健康检查端点..."
    sleep 2
    if curl -s -f http://localhost:3000/health > /dev/null 2>&1; then
        HEALTH=$(curl -s http://localhost:3000/health)
        print_success "健康检查通过: $HEALTH"
    else
        print_error "健康检查失败"
        exit 1
    fi
    
    print_info "测试首页..."
    if curl -s -f http://localhost:3000/ > /dev/null 2>&1; then
        print_success "首页访问正常"
    else
        print_error "首页访问失败"
        exit 1
    fi
}

# 显示访问信息
show_info() {
    print_header "部署完成"
    
    echo -e "${GREEN}✅ 前端部署成功!${NC}"
    echo ""
    echo "访问地址:"
    echo "  - 前端应用: http://localhost:3000"
    echo "  - 健康检查: http://localhost:3000/health"
    echo ""
    echo "常用命令:"
    echo "  - 查看日志:   docker logs -f tfboys-frontend"
    echo "  - 查看状态:   docker ps | grep tfboys-frontend"
    echo "  - 停止容器:   docker stop tfboys-frontend"
    echo "  - 启动容器:   docker start tfboys-frontend"
    echo "  - 删除容器:   docker rm -f tfboys-frontend"
    echo "  - 删除镜像:   docker rmi tfboys-frontend:latest"
    echo ""
}

# 主函数
main() {
    print_header "TFBoys 前端 Docker 部署"
    
    # 检查是否在 frontend 目录
    if [ ! -f "package.json" ] || [ ! -f "Dockerfile" ]; then
        print_error "请在 frontend 目录运行此脚本"
        exit 1
    fi
    
    # 执行部署步骤
    check_docker
    build_image
    run_container
    verify_deployment
    show_info
}

# 运行主函数
main
