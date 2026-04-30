# 🤖 AI 代码审查与重构 Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-green.svg)](https://deepseek.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📌 项目简介

基于 **DeepSeek API** 的智能代码审查与重构 Agent，能够自动扫描代码中的技术债，利用长链推理（Chain-of-Thought）分析代码异味，自动生成重构方案并运行单元测试进行闭环验证。

## 🎯 解决的核心痛点

- ❌ 人工代码审查耗时巨大，每天浪费 30% 时间
- ❌ 容易遗漏深层次的逻辑问题和代码异味
- ❌ 重构后无法保证功能不变
- ❌ 单元测试覆盖率低

## 🏗️ 核心架构


## 运行效果
╔══════════════════════════════════════════╗
║   🤖 AI代码审查与重构Agent v1.0          ║
║   基于DeepSeek API                       ║
╚══════════════════════════════════════════╝

🚀 启动代码审查与重构Agent...
📁 发现 14 个Python文件
🌿 创建分支: refactor/auto-20260430-123835

🔍 审查文件: ./main.py
   📊 复杂度: 15
   🐛 发现问题: 2个
   💯 评分: 7.5/10

============================================================
📊 重构报告
============================================================
✅ 审查文件: 14
🔧 应用重构: 3
📝 生成测试: 5
🧪 测试通过率: 100%