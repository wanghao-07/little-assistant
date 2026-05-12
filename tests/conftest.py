# 新文件: tests/conftest.py
"""
Pytest 配置文件 - 全局 fixture 和配置
"""

import pytest
import os
import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_config():
    """测试配置"""
    return {
        "test_docs_path": "./docs",
        "test_timeout": 30,
    }
