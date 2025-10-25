#!/bin/bash

#
# Video Service 快速测试脚本
# 用途: 自动化测试视频合成完整流程
#

set -e

echo "=========================================="
echo "Video Service 快速测试"
echo "=========================================="
echo ""

# 配置
BASE_URL="${VIDEO_SERVICE_URL:-http://localhost:8003}"
TEST_DATA_DIR="$(dirname "$0")"
MAX_WAIT=300
CHECK_INTERVAL=5

echo "📋 配置信息:"
echo "  - Video Service URL: $BASE_URL"
echo "  - 测试数据目录: $TEST_DATA_DIR"
echo "  - 最大等待时间: ${MAX_WAIT}秒"
echo ""

# 步骤 1: 健康检查
echo "步骤 1/4: 健康检查"
echo "----------------------------------------"
health_response=$(curl -s "${BASE_URL}/health")
if echo "$health_response" | grep -q "healthy"; then
    echo "✅ Video Service 运行正常"
else
    echo "❌ Video Service 未运行或异常"
    echo "响应: $health_response"
    exit 1
fi
echo ""

# 步骤 2: 检查测试数据
echo "步骤 2/4: 检查测试数据"
echo "----------------------------------------"
if [ ! -f "$TEST_DATA_DIR/test_request.json" ]; then
    echo "❌ test_request.json 不存在"
    exit 1
fi

for img in scene_1.jpg scene_2.jpg scene_3.jpg; do
    if [ -f "$TEST_DATA_DIR/$img" ]; then
        echo "✅ $img 存在"
    else
        echo "⚠️  $img 不存在"
    fi
done
echo ""

# 步骤 3: 创建视频合成任务
echo "步骤 3/4: 创建视频合成任务"
echo "----------------------------------------"
echo "提示: 请确保 test_request.json 中的图片和音频 URL 可访问"
echo ""

# 读取并显示请求内容
echo "请求内容 (前20行):"
head -20 "$TEST_DATA_DIR/test_request.json"
echo "..."
echo ""

read -p "是否继续提交任务? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "测试已取消"
    exit 0
fi

create_response=$(curl -s -X POST "${BASE_URL}/internal/video-synthesis/jobs" \
    -H "Content-Type: application/json" \
    -d @"$TEST_DATA_DIR/test_request.json")

echo "创建任务响应:"
echo "$create_response" | python3 -m json.tool 2>/dev/null || echo "$create_response"
echo ""

job_id=$(echo "$create_response" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['job_id'])" 2>/dev/null)

if [ -z "$job_id" ]; then
    echo "❌ 无法获取 job_id，任务创建可能失败"
    exit 1
fi

echo "✅ 任务已创建"
echo "Job ID: $job_id"
echo ""

# 步骤 4: 轮询任务状态
echo "步骤 4/4: 轮询任务状态"
echo "----------------------------------------"
echo "最大等待时间: ${MAX_WAIT}秒"
echo "检查间隔: ${CHECK_INTERVAL}秒"
echo ""

elapsed=0
while [ $elapsed -lt $MAX_WAIT ]; do
    status_response=$(curl -s "${BASE_URL}/internal/video-synthesis/jobs/${job_id}")
    status=$(echo "$status_response" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['status'])" 2>/dev/null)
    
    timestamp=$(date '+%H:%M:%S')
    echo "[$timestamp] 任务状态: $status"
    
    if [ "$status" = "completed" ]; then
        echo ""
        echo "=========================================="
        echo "✅ 任务完成！"
        echo "=========================================="
        echo ""
        echo "任务结果:"
        echo "$status_response" | python3 -m json.tool 2>/dev/null || echo "$status_response"
        echo ""
        
        # 提取视频 URL
        video_url=$(echo "$status_response" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['result']['video_url'])" 2>/dev/null)
        echo "视频文件: $video_url"
        echo ""
        echo "下一步操作:"
        echo "  1. 从容器复制视频: docker cp video-service:$video_url ./output.mp4"
        echo "  2. 查看视频信息: docker exec -it video-service ffprobe $video_url"
        echo ""
        exit 0
    elif [ "$status" = "failed" ]; then
        echo ""
        echo "=========================================="
        echo "❌ 任务失败！"
        echo "=========================================="
        echo ""
        echo "错误详情:"
        echo "$status_response" | python3 -m json.tool 2>/dev/null || echo "$status_response"
        echo ""
        exit 1
    elif [ "$status" = "processing" ]; then
        # 显示进度
        progress=$(echo "$status_response" | python3 -c "import sys, json; d = json.load(sys.stdin)['data']; print(f\"{d.get('progress', {}).get('current_scene', 0)}/{d.get('progress', {}).get('total_scenes', 0)}\")" 2>/dev/null)
        if [ -n "$progress" ]; then
            echo "  进度: $progress"
        fi
    fi
    
    sleep $CHECK_INTERVAL
    elapsed=$((elapsed + CHECK_INTERVAL))
done

echo ""
echo "=========================================="
echo "⏰ 超时"
echo "=========================================="
echo "任务未在 ${MAX_WAIT} 秒内完成"
echo "Job ID: $job_id"
echo ""
echo "请手动检查任务状态:"
echo "  curl ${BASE_URL}/internal/video-synthesis/jobs/${job_id}"
echo ""
exit 1
