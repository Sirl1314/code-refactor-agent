import os
from typing import List, Dict, Any
from datetime import datetime


class FileOperations:
    """文件操作工具集"""

    @staticmethod
    def read_file(file_path: str) -> str:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(file_path: str, content: str) -> bool:
        """写入文件内容"""
        try:
            # 确保目录存在
            dir_name = os.path.dirname(file_path)
            if dir_name:  # 只有在有目录路径时才创建
                os.makedirs(dir_name, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file: {str(e)}")
            return False

    @staticmethod
    def get_python_files(directory: str) -> List[str]:
        """获取目录下所有Python文件"""
        py_files = []
        for root, dirs, files in os.walk(directory):
            if '__pycache__' in root or 'venv' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))
        return py_files

    @staticmethod
    def backup_file(file_path: str) -> str:
        """创建文件备份（带时间戳）"""
        # 使用时间戳避免覆盖
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{file_path}.backup_{timestamp}"
        
        content = FileOperations.read_file(file_path)
        if content.startswith('Error'):
            print(f"⚠️  警告: 无法读取文件进行备份: {file_path}")
            return ""
        
        success = FileOperations.write_file(backup_path, content)
        if success:
            return backup_path
        else:
            return ""