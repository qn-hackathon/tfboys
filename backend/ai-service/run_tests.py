#!/usr/bin/env python3
"""
AI Service 测试统一入口

使用方法:
    python run_tests.py                    # 运行所有测试
    python run_tests.py --unit             # 仅运行单元测试
    python run_tests.py --integration      # 仅运行集成测试
    python run_tests.py --cov              # 运行测试并生成覆盖率报告
"""
import sys
import os
import subprocess
import argparse


def run_tests(test_type=None, coverage=False, verbose=False):
    """
    运行测试
    
    Args:
        test_type: 测试类型 ('unit', 'integration', None表示全部)
        coverage: 是否生成覆盖率报告
        verbose: 是否显示详细输出
    """
    cmd = ["pytest"]
    
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
        print("🧪 Running unit tests...")
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
        print("🔗 Running integration tests...")
    else:
        print("🧪 Running all tests...")
    
    if coverage:
        cmd.extend([
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
        print("📊 Coverage report will be generated")
    
    if verbose:
        cmd.append("-vv")
    
    print(f"\n▶️  Command: {' '.join(cmd)}\n")

    # 使用脚本所在目录作为工作目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(cmd, cwd=script_dir)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        if coverage:
            print("📊 Coverage report generated at: htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="AI Service Test Runner")
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--cov",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    test_type = None
    if args.unit:
        test_type = "unit"
    elif args.integration:
        test_type = "integration"
    
    run_tests(
        test_type=test_type,
        coverage=args.cov,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
