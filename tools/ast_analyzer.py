import ast
from typing import List, Dict, Any


class ASTAnalyzer:
    """AST代码分析工具"""

    @staticmethod
    def analyze_complexity(code: str) -> Dict[str, Any]:
        """分析代码复杂度"""
        try:
            tree = ast.parse(code)

            stats = {
                'functions': 0,
                'classes': 0,
                'imports': 0,
                'total_lines': len(code.splitlines()),
                'complexity_score': 0
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    stats['functions'] += 1
                    # 计算函数复杂度
                    complexity = sum(1 for n in ast.walk(node)
                                     if isinstance(n, (ast.If, ast.While, ast.For, ast.And, ast.Or)))
                    stats['complexity_score'] += complexity
                elif isinstance(node, ast.ClassDef):
                    stats['classes'] += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    stats['imports'] += 1

            return stats
        except SyntaxError as e:
            return {'error': f"Syntax error: {str(e)}"}

    @staticmethod
    def find_code_smells(code: str) -> List[Dict[str, Any]]:
        """识别代码坏味道"""
        smells = []
        lines = code.splitlines()

        for i, line in enumerate(lines, 1):
            # 过长的行（超过100字符）
            if len(line) > 100:
                smells.append({
                    'type': 'long_line',
                    'line': i,
                    'message': f'Line too long: {len(line)} characters',
                    'suggestion': 'Break line into multiple lines'
                })

            # 重复的代码模式（简化检测）
            if line.strip() and lines.count(line) > 2:
                smells.append({
                    'type': 'duplicate_code',
                    'line': i,
                    'message': 'Duplicate code pattern detected',
                    'suggestion': 'Extract to a function'
                })

            # TODO注释
            if 'TODO' in line or 'FIXME' in line:
                smells.append({
                    'type': 'todo_comment',
                    'line': i,
                    'message': 'TODO/FIXME comment found',
                    'suggestion': 'Address TODO before merging'
                })

        return smells