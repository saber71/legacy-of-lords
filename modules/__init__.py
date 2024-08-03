import importlib
import os.path

# 获取当前文件的目录
__directory = os.path.dirname(os.path.abspath(__file__))
# 列出目录中的所有文件和文件夹
__entries = os.listdir(__directory)

# 初始化一个空列表，用于存储模块实例
modules = []
# 遍历目录中的每个文件和文件夹
for entry in __entries:
    # 跳过特殊文件，如__init__.py
    if entry.startswith("__"):
        continue
    # 检查entry是否为目录
    dir = os.path.join(__directory, entry)
    if os.path.isdir(dir):
        # 如果是目录，则认为其为一个模块，尝试导入
        module = importlib.import_module(f"modules.{entry}")
        # 模块的入口是Module类实例
        modules.append(module.Module())
