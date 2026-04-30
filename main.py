#!/usr/bin/env python3
"""
智能代码审查与重构Agent
基于DeepSeek API的自动化代码质量提升工具
"""

import argparse
import sys
import os
from dotenv import load_dotenv
from agent.orchestrator import Orchestrator

# 加载环境变量
load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description='AI-powered Code Review and Refactoring Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 审查整个项目
  python main.py --repo-path ./my-project

  # 审查单个文件
  python main.py --file ./src/main.py

  # 审查并自动重构
  python main.py --repo-path ./my-project --auto-refactor

  # 只生成测试
  python main.py --file ./src/utils.py --generate-tests
        """
    )

    parser.add_argument('--repo-path', type=str, default='.',
                        help='Git仓库路径（默认: 当前目录）')
    parser.add_argument('--file', type=str,
                        help='指定单个文件进行审查')
    parser.add_argument('--auto-refactor', action='store_true',
                        help='自动应用重构建议')
    parser.add_argument('--generate-tests', action='store_true',
                        help='生成单元测试')

    args = parser.parse_args()

    # 检查API密钥
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("❌ 错误: 请设置 DEEPSEEK_API_KEY 环境变量")
        print("   在 .env 文件中添加: DEEPSEEK_API_KEY=sk-xxx")
        sys.exit(1)

    print("""
    ╔══════════════════════════════════════════╗
    ║   🤖 AI代码审查与重构Agent v1.0          ║
    ║   基于DeepSeek API                       ║
    ╚══════════════════════════════════════════╝
    """)

    # 初始化主控Agent
    orchestrator = Orchestrator(args.repo_path)

    # 运行
    try:
        results = orchestrator.run(
            target_file=args.file,
            auto_refactor=args.auto_refactor or args.generate_tests
        )

        print("\n✨ 处理完成!")

        # 返回状态码
        if results.get('success_rate', 0) == 100:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 致命错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()