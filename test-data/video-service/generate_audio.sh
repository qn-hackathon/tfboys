#!/bin/bash

echo "=========================================="
echo "生成测试音频文件"
echo "=========================================="
echo ""

# 检查 FFmpeg 是否已安装
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg 未安装"
    echo ""
    echo "请先安装 FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo ""
    exit 1
fi

# 进入脚本所在目录
cd "$(dirname "$0")"

echo "正在生成测试音频文件..."
echo ""

# 生成场景1音频 (3秒，440Hz 正弦波)
echo "生成 scene_1_audio.mp3 (3秒)..."
ffmpeg -f lavfi -i "sine=frequency=440:duration=3" \
  -ar 44100 -ac 2 -b:a 192k scene_1_audio.mp3 -y 2>&1 | tail -3
echo "✅ scene_1_audio.mp3"
echo ""

# 生成场景2音频 (4秒，523Hz 正弦波)
echo "生成 scene_2_audio.mp3 (4秒)..."
ffmpeg -f lavfi -i "sine=frequency=523:duration=4" \
  -ar 44100 -ac 2 -b:a 192k scene_2_audio.mp3 -y 2>&1 | tail -3
echo "✅ scene_2_audio.mp3"
echo ""

# 生成场景3音频 (5秒，659Hz 正弦波)
echo "生成 scene_3_audio.mp3 (5秒)..."
ffmpeg -f lavfi -i "sine=frequency=659:duration=5" \
  -ar 44100 -ac 2 -b:a 192k scene_3_audio.mp3 -y 2>&1 | tail -3
echo "✅ scene_3_audio.mp3"
echo ""

echo "=========================================="
echo "✅ 所有音频文件生成完成！"
echo "=========================================="
echo ""
echo "生成的文件："
ls -lh *.mp3 2>/dev/null || echo "未找到 mp3 文件"
echo ""
