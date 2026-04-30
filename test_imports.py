#!/usr/bin/env python3
"""测试所有模块的导入是否正常"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("测试模块导入...")
print("=" * 60)

try:
    from tools.file_ops import FileOperations
    print("✅ tools.file_ops.FileOperations - 成功")
except Exception as e:
    print(f"❌ tools.file_ops.FileOperations - 失败: {e}")

try:
    from tools.ast_analyzer import ASTAnalyzer
    print("✅ tools.ast_analyzer.ASTAnalyzer - 成功")
except Exception as e:
    print(f"❌ tools.ast_analyzer.ASTAnalyzer - 失败: {e}")

try:
    from tools.git_ops import GitOperations
    print("✅ tools.git_ops.GitOperations - 成功")
except Exception as e:
    print(f"❌ tools.git_ops.GitOperations - 失败: {e}")

try:
    from tools.test_runner import TestRunner
    print("✅ tools.test_runner.TestRunner - 成功")
except Exception as e:
    print(f"❌ tools.test_runner.TestRunner - 失败: {e}")

try:
    from agent.code_reviewer import CodeReviewAgent
    print("✅ agent.code_reviewer.CodeReviewAgent - 成功")
except Exception as e:
    print(f"❌ agent.code_reviewer.CodeReviewAgent - 失败: {e}")

try:
    from agent.refactor_engine import RefactorAgent
    print("✅ agent.refactor_engine.RefactorAgent - 成功")
except Exception as e:
    print(f"❌ agent.refactor_engine.RefactorAgent - 失败: {e}")

try:
    from agent.test_generator import TestGeneratorAgent
    print("✅ agent.test_generator.TestGeneratorAgent - 成功")
except Exception as e:
    print(f"❌ agent.test_generator.TestGeneratorAgent - 失败: {e}")

try:
    from agent.orchestrator import Orchestrator
    print("✅ agent.orchestrator.Orchestrator - 成功")
except Exception as e:
    print(f"❌ agent.orchestrator.Orchestrator - 失败: {e}")

print("=" * 60)
print("导入测试完成!")
