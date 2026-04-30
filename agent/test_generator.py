from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, Any
import re

load_dotenv()

class TestGeneratorAgent:
    """测试生成Agent - 负责生成单元测试"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url=os.getenv('DEEPSEEK_BASE_URL')
        )
        self.model = "deepseek-chat"
    
    def generate_tests(self, code: str, file_path: str) -> Dict[str, Any]:
        """为代码生成单元测试"""
        system_prompt = "你是一个单元测试专家。根据代码生成pytest单元测试。要求覆盖正常路径、边界情况和异常处理。"
        
        user_prompt = f"为以下代码生成单元测试：\n```python\n{code}\n```"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            test_code = response.choices[0].message.content
            if '```python' in test_code:
                code_start = test_code.find('```python') + 9
                code_end = test_code.find('```', code_start)
                test_code = test_code[code_start:code_end].strip()
            
            return {
                'success': True,
                'test_code': test_code,
                'test_file': f"tests/test_{os.path.basename(file_path)}"
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'test_code': ''}
