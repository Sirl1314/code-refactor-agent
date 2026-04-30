from typing import Dict, Any, List
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tools.file_ops import FileOperations
from tools.ast_analyzer import ASTAnalyzer
from tools.git_ops import GitOperations
from tools.test_runner import TestRunner
from .code_reviewer import CodeReviewAgent
from .refactor_engine import RefactorAgent
from .test_generator import TestGeneratorAgent
import time
import json
from datetime import datetime


class Orchestrator:
    """主控Agent - 协调所有Agent工作"""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.file_ops = FileOperations()
        self.ast_analyzer = ASTAnalyzer()
        self.git_ops = GitOperations(repo_path)
        self.test_runner = TestRunner()
        self.review_agent = CodeReviewAgent()
        self.refactor_agent = RefactorAgent()
        self.test_agent = TestGeneratorAgent()

        self.results = {
            'reviewed_files': [],
            'refactors_applied': 0,
            'tests_generated': 0,
            'success_rate': 0,
            'errors': []
        }

    def run(self, target_file: str = None, auto_refactor: bool = False) -> Dict[str, Any]:
        """运行完整的审查和重构流程"""

        print("🚀 启动代码审查与重构Agent...")

        # 1. 获取目标文件
        if target_file:
            target_files = [target_file] if os.path.exists(target_file) else []
        else:
            target_files = self.file_ops.get_python_files(self.repo_path)

        if not target_files:
            return {'error': 'No Python files found'}

        print(f"📁 发现 {len(target_files)} 个Python文件")

        # 2. 创建重构分支
        branch_name = f"refactor/auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.git_ops.create_branch(branch_name)
        print(f"🌿 创建分支: {branch_name}")

        # 3. 审查每个文件
        for file_path in target_files[:5]:  # 限制处理5个文件避免Token超限
            print(f"\n🔍 审查文件: {file_path}")

            code = self.file_ops.read_file(file_path)
            if code.startswith('Error'):
                print(f"   ❌ {code}")
                continue

            # 静态分析
            stats = self.ast_analyzer.analyze_complexity(code)
            smells = self.ast_analyzer.find_code_smells(code)

            # AI审查
            review_result = self.review_agent.review_code(code, file_path)

            if 'error' not in review_result:
                issues = review_result.get('issues', [])

                print(f"   📊 复杂度: {stats.get('complexity_score', 0)}")
                print(f"   🐛 发现问题: {len(issues)}个")
                print(f"   💯 评分: {review_result.get('overall_score', 0)}/10")

                # 保存审查结果
                self.results['reviewed_files'].append({
                    'file': file_path,
                    'score': review_result.get('overall_score'),
                    'issues': len(issues),
                    'summary': review_result.get('summary', '')
                })

                # 4. 自动重构（如果启用）
                if auto_refactor and issues:
                    print(f"   🔧 开始重构...")
                    refactor_plan = self.refactor_agent.generate_refactor_plan(code, issues)

                    if refactor_plan.get('needs_refactor'):
                        refactored_code = self.refactor_agent.apply_refactor(
                            code,
                            refactor_plan['plan']
                        )

                        # 备份并应用重构
                        backup_path = self.file_ops.backup_file(file_path)
                        if backup_path:  # 检查备份是否成功
                            write_success = self.file_ops.write_file(file_path, refactored_code)
                            
                            if write_success:
                                self.results['refactors_applied'] += 1
                                print(f"   ✅ 重构完成，备份: {backup_path}")

                                # 5. 生成测试
                                print(f"   📝 生成单元测试...")
                                test_result = self.test_agent.generate_tests(refactored_code, file_path)

                                if test_result['success']:
                                    test_file_path = test_result['test_file']
                                    # 确保测试目录存在
                                    test_dir = os.path.dirname(test_file_path)
                                    if test_dir:
                                        os.makedirs(test_dir, exist_ok=True)
                                    self.file_ops.write_file(test_file_path, test_result['test_code'])
                                    self.results['tests_generated'] += 1
                                    print(f"   ✅ 测试生成: {test_file_path}")
                            else:
                                print(f"   ⚠️  写入失败，保持原文件")
                        else:
                            print(f"   ⚠️  备份失败，跳过重构")

                # 避免API限流
                time.sleep(1)
            else:
                print(f"   ❌ 审查失败: {review_result.get('error')}")
                self.results['errors'].append(review_result.get('error'))

        # 6. 运行测试验证
        print(f"\n🧪 运行测试验证...")
        test_results = self.test_runner.run_tests()

        if test_results['success']:
            print(f"   ✅ 所有测试通过")
            self.results['success_rate'] = 100
        else:
            print(f"   ❌ 测试失败")
            print(f"   {test_results.get('stderr', '')[:200]}")
            self.results['success_rate'] = 0
            
            # 测试失败时回滚重构
            if self.results['refactors_applied'] > 0:
                print(f"\n⚠️  测试失败，正在回滚重构...")
                self._rollback_refactors()

        # 7. 提交变更并创建PR
        if self.results['refactors_applied'] > 0 and self.results['success_rate'] == 100:
            commit_msg = f"🤖 Auto-refactor: Improved code quality\n\nIssues fixed: {sum(r.get('issues', 0) for r in self.results['reviewed_files'])}"
            if self.git_ops.commit_changes(commit_msg):
                print(f"   ✅ 提交成功")
                
                # 创建PR
                pr_result = self.git_ops.create_pull_request(
                    title="[Auto] Code Refactoring by AI Agent",
                    description=f"""
                    ## 🤖 AI Agent 自动重构

                    ### 变更内容
                    - 审查了 {len(self.results['reviewed_files'])} 个文件
                    - 应用了 {self.results['refactors_applied']} 处重构
                    - 生成了 {self.results['tests_generated']} 个测试文件

                    ### 质量指标
                    - 测试通过率: {self.results['success_rate']}%
                    """
                )
                print(f"\n🔀 PR已创建: {pr_result.get('pr_url', 'N/A')}")
            else:
                print(f"   ⚠️  提交失败，请手动检查")
        elif self.results['refactors_applied'] > 0:
            print(f"\n⚠️  由于测试失败，跳过提交和PR创建")

        # 8. 生成报告
        self._generate_report()

        return self.results

    def _rollback_refactors(self):
        """回滚所有重构，恢复备份文件"""
        import glob
        # 匹配所有备份文件（新格式：*.backup_*）
        backup_files = glob.glob(os.path.join(self.repo_path, '**/*.backup_*'), recursive=True)
        
        for backup_path in backup_files:
            # 提取原始文件路径（去掉 .backup_YYYYMMDD_HHMMSS）
            # 找到最后一个 .backup_ 的位置
            backup_marker = '.backup_'
            if backup_marker in backup_path:
                original_path = backup_path[:backup_path.rfind(backup_marker)]
            else:
                continue
            
            try:
                # 恢复备份
                content = self.file_ops.read_file(backup_path)
                if not content.startswith('Error'):
                    if self.file_ops.write_file(original_path, content):
                        print(f"   ✅ 已恢复: {original_path}")
                        # 删除备份文件
                        os.remove(backup_path)
                    else:
                        print(f"   ❌ 恢复失败: {original_path}")
            except Exception as e:
                print(f"   ❌ 回滚错误: {str(e)}")
    
    def _generate_report(self):
        """生成最终报告"""
        print("\n" + "=" * 60)
        print("📊 重构报告")
        print("=" * 60)
        print(f"✅ 审查文件: {len(self.results['reviewed_files'])}")
        print(f"🔧 应用重构: {self.results['refactors_applied']}")
        print(f"📝 生成测试: {self.results['tests_generated']}")
        print(f"🧪 测试通过率: {self.results['success_rate']}%")

        if self.results['errors']:
            print(f"⚠️  错误: {len(self.results['errors'])}")

        # 保存报告到文件
        report_file = f"refactor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 报告已保存: {report_file}")