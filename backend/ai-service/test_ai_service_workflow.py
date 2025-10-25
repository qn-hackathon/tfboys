#!/usr/bin/env python3
"""
AI 服务真实流程测试脚本

本脚本测试 AI 服务的完整工作流程，包括：
- 文本分析：将小说文本解析为场景信息
- 图像生成：为场景生成对应的图像
- 配音生成：为场景旁白生成语音文件

使用方法:
    python test_ai_service_workflow.py --test text       # 测试文本分析流程
    python test_ai_service_workflow.py --test image      # 测试图像生成流程
    python test_ai_service_workflow.py --test voice      # 测试配音生成流程
    python test_ai_service_workflow.py --test all        # 测试完整工作流程
"""
import asyncio
import argparse
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.services.text_analyzer import TextAnalyzer
from app.services.image_generator import ImageGenerator
from app.services.voice_generator import VoiceGenerator
from app.config import settings
from shared.clients import init_local_storage_client, init_redis_client
from shared.enums import TTSVoice
from shared.models.scene import Scene


async def test_text_analysis():
    """测试文本分析流程"""
    print("=" * 60)
    print("📖 测试文本分析流程 (小说文本 → 场景和角色信息)")
    print("=" * 60)

    # 示例小说文本
    novel_text = """
    春天的早晨，校园里樱花盛开。小明走在林荫道上，看着花瓣飘落。
    他是一个黑色短发、蓝色眼睛的少年，身穿白色校服。
    阳光透过树叶洒在地面，微风吹过，带来花香。

    小明来到教室，同学们已经在座位上了。他的好朋友小红向他招手。
    小红是一个红色长发、棕色眼睛的少女，今天穿着粉色的连衣裙。
    "早上好！" 小红笑着说。
    """

    try:
        print(f"\n📝 输入文本长度: {len(novel_text)} 字符")
        print("\n🔄 正在执行文本分析流程...")

        analyzer = TextAnalyzer()
        scenes = await analyzer.analyze_novel(novel_text)

        print(f"\n✅ 文本分析流程完成！生成了 {len(scenes)} 个场景\n")

        for scene in scenes:
            print(f"场景 {scene['scene_index']}:")
            print(f"  描述: {scene['description'][:50]}...")
            print(f"  旁白: {scene['narration'][:50]}...")
            print()

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_image_generation():
    """测试图像生成流程"""
    print("=" * 60)
    print("🎨 测试图像生成流程 (角色和场景 → 图像文件)")
    print("=" * 60)

    # 初始化本地存储客户端
    init_local_storage_client("/tmp/tfboys")

    try:
        generator = ImageGenerator()

        # 测试1: 生成场景图像
        print("\n📸 流程测试 1: 场景图像生成")
        print("输入: 场景描述 → 输出: 场景图像")
        print("场景: 春天的校园，樱花飘落")

        scene_path = await generator.generate_scene_image(
            scene_description="春天的校园，樱花盛开，花瓣飘落，阳光透过树叶",
            scene_id="test_scene_001"
        )

        print(f"✅ 场景图像生成完成: {scene_path}")

        if os.path.exists(scene_path):
            file_size = os.path.getsize(scene_path)
            print(f"   文件大小: {file_size / 1024:.2f} KB")

        # 测试2: 不同宽高比
        print("\n📸 测试 2: 生成不同宽高比的图像")

        for ar in ["1:1", "16:9", "9:16"]:
            print(f"   测试 {ar} 宽高比...")
            test_path = await generator.generate_image(
                prompt="动漫风格的校园场景",
                ar=ar
            )
            if os.path.exists(test_path):
                print(f"   ✅ {ar} 图像生成成功")

        await generator.close()

        print("\n✅ 图像生成流程测试完成！")
        print(f"\n📁 生成的图像保存在: /tmp/tfboys/")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_voice_generation():
    """测试配音生成流程"""
    print("=" * 60)
    print("🎙️  测试配音生成流程 (文本 → 语音文件)")
    print("=" * 60)

    # 初始化本地存储客户端
    init_local_storage_client("/tmp/tfboys")

    try:
        generator = VoiceGenerator()

        # 测试1: 生成女声配音
        print("\n🎵 流程测试 1: 女声配音生成")
        print("输入: 文本 + 女声参数 → 输出: 女声语音文件")
        test_text_1 = "春天的早晨，校园里樱花盛开，微风吹过，花瓣如雪般飘落。"
        print(f"文本: {test_text_1}")

        audio_url_1, duration_1 = await generator.generate_voice(
            text=test_text_1,
            task_id="test_task",
            scene_id="scene_001",
            voice=TTSVoice.FEMALE
        )

        print(f"✅ 女声配音生成完成")
        print(f"   文件路径: {audio_url_1}")
        print(f"   时长: {duration_1:.2f} 秒")

        if os.path.exists(audio_url_1):
            file_size = os.path.getsize(audio_url_1)
            print(f"   文件大小: {file_size / 1024:.2f} KB")

        # 测试2: 生成男声配音
        print("\n🎵 流程测试 2: 男声配音生成")
        print("输入: 文本 + 男声参数 → 输出: 男声语音文件")
        test_text_2 = "小明来到教室，同学们已经在座位上了。"
        print(f"文本: {test_text_2}")

        audio_url_2, duration_2 = await generator.generate_voice(
            text=test_text_2,
            task_id="test_task",
            scene_id="scene_002",
            voice=TTSVoice.MALE
        )

        print(f"✅ 男声配音生成完成")
        print(f"   文件路径: {audio_url_2}")
        print(f"   时长: {duration_2:.2f} 秒")

        if os.path.exists(audio_url_2):
            file_size = os.path.getsize(audio_url_2)
            print(f"   文件大小: {file_size / 1024:.2f} KB")

        print("\n✅ 配音生成流程测试完成！")
        print(f"\n📁 生成的音频保存在: /tmp/tfboys/audio/")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    parser = argparse.ArgumentParser(description="AI 服务真实流程测试")
    parser.add_argument(
        "--test",
        choices=["text", "image", "voice", "all"],
        default="all",
        help="选择测试类型"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("🚀 AI 服务真实流程测试")
    print("=" * 60)
    print(f"\n配置信息:")
    print(f"  七牛 API Key: {settings.qiniu_api_key[:20]}..." if settings.qiniu_api_key else "  ⚠️  未配置 QINIU_API_KEY")
    print(f"  Redis URL: {settings.redis_url}")
    print()

    if not settings.qiniu_api_key:
        print("❌ 错误: 请先配置 QINIU_API_KEY 环境变量")
        print("\n配置方法:")
        print("  1. 编辑 backend/ai-service/.env 文件")
        print("  2. 设置 QINIU_API_KEY=your-api-key")
        print("  3. 重新运行测试")
        return 1

    results = []

    if args.test in ["text", "all"]:
        result = await test_text_analysis()
        results.append(("文本分析", result))

    if args.test in ["image", "all"]:
        result = await test_image_generation()
        results.append(("图像生成", result))

    if args.test in ["voice", "all"]:
        # 检查是否配置了 TTS API Key
        if settings.qiniu_api_key:
            result = await test_voice_generation()
            results.append(("配音生成", result))
        else:
            print("\n⚠️  跳过配音测试: 未配置 QINIU_API_KEY")
            print("    如需测试配音功能，请在 .env 文件中配置七牛云 API Key")

    # 打印测试摘要
    print("\n" + "=" * 60)
    print("📊 测试摘要")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n🎉 所有流程测试通过！AI 服务工作流程正常！")
        return 0
    else:
        print("\n⚠️  部分流程测试失败，请检查配置和网络连接")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
