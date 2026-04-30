from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json

load_dotenv()


class CodeReviewAgent:
    """代码审查Agent - 负责分析代码质量"""

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url=os.getenv('DEEPSEEK_BASE_URL')
        )
        self.model = "deepseek-reasoner"  # 使用推理模型

    def review_code(self, code: str, file_path: str = "") -> Dict[str, Any]:
        """审查代码并使用长链推理"""

        system_prompt = """你是一位资深的代码审查专家。你的任务是：
1. 分析代码的质量、可维护性和性能
2. 识别代码异味、潜在bug和反模式
3. 使用Chain-of-Thought逐步推理，给出具体的改进建议
4. 优先指出影响代码质量的关键问题

请按以下格式输出JSON：
{
    "overall_score": 1-10,
    "issues": [
        {
            "severity": "critical|major|minor",
            "type": "bug|performance|style|security|maintainability",
            "description": "问题描述",
            "suggestion": "改进建议"
        }
    ],
    "summary": "整体评价"
}"""

        user_prompt = f"""
请审查以下代码文件：{file_path}

```python
{code[:3000]}
```
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                timeout=30  # 设置超时时间
            )
            
            result = response.choices[0].message.content
            
            # 尝试多种格式提取JSON
            json_str = None
            
            # 格式1: ```json ... ```
            if '```json' in result:
                code_start = result.find('```json') + 7
                code_end = result.find('```', code_start)
                if code_end > code_start:
                    json_str = result[code_start:code_end].strip()
            
            # 格式2: ``` ... ```
            elif '```' in result:
                code_start = result.find('```') + 3
                # 跳过可能的语言标识
                if '\n' in result[code_start:code_start+20]:
                    code_start = result.find('\n', code_start) + 1
                code_end = result.find('```', code_start)
                if code_end > code_start:
                    json_str = result[code_start:code_end].strip()
            
            # 格式3: 直接是JSON
            else:
                json_str = result.strip()
            
            if not json_str:
                return {'error': '无法从响应中提取JSON', 'overall_score': 0, 'issues': [], 'summary': ''}
            
            # 解析JSON
            parsed = json.loads(json_str)
            
            # 验证必需字段
            if 'overall_score' not in parsed:
                parsed['overall_score'] = 0
            if 'issues' not in parsed:
                parsed['issues'] = []
            if 'summary' not in parsed:
                parsed['summary'] = ''
            
            # 验证分数范围
            if not isinstance(parsed['overall_score'], (int, float)):
                parsed['overall_score'] = 0
            else:
                parsed['overall_score'] = max(0, min(10, parsed['overall_score']))
            
            return parsed
            
        except json.JSONDecodeError as e:
            return {'error': f'JSON解析失败: {str(e)}', 'overall_score': 0, 'issues': [], 'summary': ''}
        except Exception as e:
            return {'error': f'API调用失败: {str(e)}', 'overall_score': 0, 'issues': [], 'summary': ''}