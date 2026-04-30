import subprocess
import sys
from typing import Dict, Any


class TestRunner:
    """测试运行器"""

    def __init__(self, test_path: str = 'tests'):
        self.test_path = test_path

    def run_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=60
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Tests timed out after 60 seconds'}
        except Exception as e:
            return {'success': False, 'error': str(e)}