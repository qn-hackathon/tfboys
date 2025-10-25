#!/usr/bin/env python3
"""
七牛 AI Token API 功能测试脚本

使用方法:
    python test_qiniu_integration.py --test text     # 测试文本分析
    python test_qiniu_integration.py --test image    # 测试图像生成
    python test_qiniu_integration.py --test all      # 测试所有功能
"""
import asyncio
import argparse
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.services.text_analyzer import TextAnalyzer
from app.services.image_generator import ImageGenerator
from app.config import settings
from shared.clients import init_local_storage_client


async def test_text_analysis():
    """测试文本分析功能"""
    print("=" * 60)
    print("🧪 测试文本分析 (七牛 AI 推理 API - DeepSeek-V3)")
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
        print("\n正在调用七牛 AI 推理 API...")

        analyzer = TextAnalyzer()
        scenes = await analyzer.analyze_novel(novel_text)

        print(f"\n✅ 分析成功！生成了 {len(scenes)} 个场景\n")

        for scene in scenes:
            print(f"场景 {scene['scene_index']}:")
            print(f"  描述: {scene['description'][:50]}...")
            print(f"  旁白: {scene['narration'][:50]}...")
            print(f"  角色数: {len(scene.get('characters', []))}")
            for char in scene.get('characters', []):
                print(f"    - {char['name']}: {char['description'][:30]}...")
            print()

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_image_generation():
    """测试图像生成功能"""
    print("=" * 60)
    print("🎨 测试图像生成 (七牛文生图 API - Gemini 2.5 Flash)")
    print("=" * 60)

    # 初始化本地存储客户端
    init_local_storage_client("/tmp/tfboys")

    try:
        generator = ImageGenerator()

        # 测试1: 生成角色图像
        print("\n📸 测试 1: 生成角色设定图")
        print("角色: 小明 (黑色短发，蓝色眼睛的少年)")

        image_path = await generator.generate_character_image(
            character_name="小明",
            character_description="少年，黑色短发，蓝色眼睛，身穿白色校服"
        )

        print(f"✅ 图像已生成: {image_path}")

        # 验证文件是否存在
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path)
            print(f"   文件大小: {file_size / 1024:.2f} KB")

        # 测试2: 生成场景图像
        print("\n📸 测试 2: 生成场景图像")
        print("场景: 春天的校园，樱花飘落")

        scene_path = await generator.generate_scene_image(
            scene_description="春天的校园，樱花盛开，花瓣飘落，阳光透过树叶",
            scene_id="test_scene_001",
            character_context="小明: 黑色短发蓝色眼睛的少年"
        )

        print(f"✅ 场景图像已生成: {scene_path}")

        if os.path.exists(scene_path):
            file_size = os.path.getsize(scene_path)
            print(f"   文件大小: {file_size / 1024:.2f} KB")

        # 测试3: 不同宽高比
        print("\n📸 测试 3: 生成不同宽高比的图像")

        for ar in ["1:1", "16:9", "9:16"]:
            print(f"   测试 {ar} 宽高比...")
            test_path = await generator.generate_image(
                prompt="动漫风格的校园场景",
                ar=ar
            )
            if os.path.exists(test_path):
                print(f"   ✅ {ar} 图像生成成功")

        await generator.close()

        print("\n✅ 所有图像生成测试通过！")
        print(f"\n📁 生成的图像保存在: /tmp/tfboys/")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    parser = argparse.ArgumentParser(description="七牛 AI Token API 功能测试")
    parser.add_argument(
        "--test",
        choices=["text", "image", "all"],
        default="all",
        help="选择测试类型"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("🚀 七牛 AI Token API 功能测试")
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

    # 打印测试摘要
    print("\n" + "=" * 60)
    print("📊 测试摘要")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n🎉 所有测试通过！七牛 API 集成成功！")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查配置和网络连接")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
