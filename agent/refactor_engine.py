from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import json

load_dotenv()


class RefactorAgent:
    """重构引擎Agent - 负责执行代码重构"""

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url=os.getenv('DEEPSEEK_BASE_URL')
        )
        self.model = "deepseek-chat"

    def generate_refactor_plan(self, code: str, issues: List[Dict]) -> Dict[str, Any]:
        """生成重构计划"""

        system_prompt = """你是一个代码重构专家。根据代码审查发现的问题，生成详细的重构计划。
计划应该：
1. 按优先级排序重构任务
2. 确保重构不改变代码功能
3. 给出具体的重构步骤
4. 提供重构后的代码示例"""

        user_prompt = f"""
原始代码：
```python
{code[:2000]}
```

发现的问题：
{json.dumps(issues, indent=2, ensure_ascii=False)}

请生成重构计划。
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            if '```json' in result:
                code_start = result.find('```json') + 7
                code_end = result.find('```', code_start)
                result = result[code_start:code_end].strip()
            
            plan = json.loads(result)
            return {
                'needs_refactor': plan.get('needs_refactor', False),
                'plan': plan
            }
        except Exception as e:
            return {'error': str(e), 'needs_refactor': False, 'plan': {}}

    def apply_refactor(self, code: str, plan: Dict[str, Any]) -> str:
        """应用重构计划"""
        system_prompt = """你是一个代码重构专家。根据重构计划，对代码进行重构。
要求：
1. 保持代码功能不变
2. 提高代码质量和可读性
3. 返回完整的重构后代码"""
        
        user_prompt = f"""
原始代码：
```python
{code}
```

重构计划：
{json.dumps(plan, indent=2, ensure_ascii=False)}

请返回重构后的完整代码。
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                timeout=60  # 重构可能需要更长时间
            )
            
            refactored_code = response.choices[0].message.content
            
            # 尝试多种格式提取代码
            extracted_code = None
            
            # 格式1: ```python ... ```
            if '```python' in refactored_code:
                code_start = refactored_code.find('```python') + 9
                code_end = refactored_code.find('```', code_start)
                if code_end > code_start:
                    extracted_code = refactored_code[code_start:code_end].strip()
            
            # 格式2: ``` ... ```
            elif '```' in refactored_code:
                code_start = refactored_code.find('```') + 3
                # 跳过可能的语言标识
                if '\n' in refactored_code[code_start:code_start+20]:
                    code_start = refactored_code.find('\n', code_start) + 1
                code_end = refactored_code.find('```', code_start)
                if code_end > code_start:
                    extracted_code = refactored_code[code_start:code_end].strip()
            
            # 格式3: 直接使用响应内容
            else:
                extracted_code = refactored_code.strip()
            
            if not extracted_code:
                print("⚠️  警告: 无法从响应中提取代码，返回原始代码")
                return code
            
            # 验证代码语法
            try:
                import ast
                ast.parse(extracted_code)
                print("✅ 重构代码语法验证通过")
                return extracted_code
            except SyntaxError as e:
                print(f"⚠️  警告: 重构代码有语法错误: {str(e)}")
                print("   返回原始代码")
                return code
            
        except Exception as e:
            print(f"Error applying refactor: {str(e)}")
            return code