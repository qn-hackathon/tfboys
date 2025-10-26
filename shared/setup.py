"""
TFBoys Shared Module Setup

共享模块安装配置文件
"""
from setuptools import setup, find_packages

setup(
    name="tfboys-shared",
    version="1.0.0",
    description="TFBoys项目共享模块 - 包含通用模型、客户端和工具",
    author="TFBoys Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "redis>=4.6.0,<5.0.0",  # 限制 Redis 版本以兼容 Celery 5.3.4
        "pydantic>=2.5.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
