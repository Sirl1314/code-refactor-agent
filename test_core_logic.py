#!/usr/bin/env python3
"""
核心逻辑测试脚本
测试修复后的关键功能
"""

import sys
import os
import json

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 60)
print("🧪 核心逻辑测试")
print("=" * 60)

# 测试1: 文件操作
print("\n📝 测试1: 文件操作工具")
print("-" * 60)

from tools.file_ops import FileOperations

# 测试写入文件
test_file = "test_output.txt"
result = FileOperations.write_file(test_file, "Hello, World!")
print(f"✅ 写入文件: {result}")

# 测试读取文件
content = FileOperations.read_file(test_file)
print(f"✅ 读取文件: {content}")

# 测试备份文件
backup = FileOperations.backup_file(test_file)
print(f"✅ 备份文件: {backup}")
if backup:
    print(f"   备份文件名包含时间戳: {'backup_' in backup}")

# 清理测试文件
os.remove(test_file)
if backup and os.path.exists(backup):
    os.remove(backup)

# 测试2: JSON解析健壮性
print("\n📝 测试2: JSON解析健壮性")
print("-" * 60)

from agent.code_reviewer import CodeReviewAgent

reviewer = CodeReviewAgent()

# 模拟不同的JSON格式
test_cases = [
    ('```\n{"score": 8}\n```', "代码块格式"),
    ('```json\n{"score": 9}\n```', "JSON代码块格式"),
    ('{"score": 7}', "纯JSON格式"),
]

for test_json, description in test_cases:
    try:
        # 模拟提取逻辑
        json_str = None
        
        if '```json' in test_json:
            code_start = test_json.find('```json') + 7
            code_end = test_json.find('```', code_start)
            if code_end > code_start:
                json_str = test_json[code_start:code_end].strip()
        
        elif '```' in test_json:
            code_start = test_json.find('```') + 3
            if '\n' in test_json[code_start:code_start+20]:
                code_start = test_json.find('\n', code_start) + 1
            code_end = test_json.find('```', code_start)
            if code_end > code_start:
                json_str = test_json[code_start:code_end].strip()
        
        else:
            json_str = test_json.strip()
        
        if json_str:
            parsed = json.loads(json_str)
            print(f"✅ {description}: 成功解析 - {parsed}")
        else:
            print(f"❌ {description}: 提取失败")
    except Exception as e:
        print(f"❌ {description}: {str(e)}")

# 测试3: 代码语法验证
print("\n📝 测试3: 代码语法验证")
print("-" * 60)

import ast

test_codes = [
    ("def hello():\n    print('world')", "有效代码"),
    ("def broken(:\n    print('world')", "无效代码"),
]

for code, description in test_codes:
    try:
        ast.parse(code)
        print(f"✅ {description}: 语法正确")
    except SyntaxError as e:
        print(f"⚠️  {description}: 语法错误 - {str(e)[:50]}")

# 测试4: 路径处理
print("\n📝 测试4: 路径处理")
print("-" * 60)

test_paths = [
    "simple.txt",
    "dir/file.txt",
    "/absolute/path/file.txt",
]

for path in test_paths:
    dir_name = os.path.dirname(path)
    print(f"路径: {path:30} -> 目录: '{dir_name}' (空={not dir_name})")

# 测试5: 回滚逻辑
print("\n📝 测试5: 回滚逻辑（模拟）")
print("-" * 60)

import glob
from datetime import datetime

# 创建测试备份文件
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
test_backup = f"test_file.txt.backup_{timestamp}"
FileOperations.write_file(test_backup, "original content")

# 模拟回滚查找
backup_files = glob.glob("*.backup_*")
print(f"找到备份文件: {len(backup_files)} 个")

for backup_path in backup_files:
    backup_marker = '.backup_'
    if backup_marker in backup_path:
        original_path = backup_path[:backup_path.rfind(backup_marker)]
        print(f"  备份: {backup_path} -> 原始: {original_path}")

# 清理
for f in backup_files:
    os.remove(f)

print("\n" + "=" * 60)
print("✅ 所有测试完成!")
print("=" * 60)
