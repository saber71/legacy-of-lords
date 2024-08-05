import abc
from typing import List, Type, Callable, Dict


class BaseModule(abc.ABC):
    """
    基础模块类，定义了模块的基本结构和行为。
    """

    def __init__(self, name: str, description: str, *pre_modules: Type["BaseModule"]):
        """
        初始化方法，用于创建类的实例时设置初始值。

        参数:
        - name: str 模块的名称。
        - description: str 模块的描述信息。
        - pre_modules: BaseModule[] 该模块的前置模块
        """
        self.name = name
        self.description = description
        self.pre_modules = list(pre_modules)

    @abc.abstractmethod
    def install(self):
        """
        安装模块的抽象定义。

        此方法应在具体的子类中实现，以提供特定的安装逻辑。
        """
        pass

    @abc.abstractmethod
    def uninstall(self):
        """
        卸载模块的抽象方法。

        此方法负责卸载模块，具体的卸载逻辑由继承该类的子类实现。
        """
        pass

    @abc.abstractmethod
    def tick(self):
        """
        在具体子类中，它可以触发不同的行为，如更新状态或执行周期性任务。
        """
        pass


# 定义一个用于存储待执行tick函数的列表
__tick_list: List[Callable[[], None]] = []
# 定义一个用于存储已安装模块类的字典，键为模块类的id，值为模块实例
__class_dict: Dict[int, BaseModule] = {}
# 定义一个用于存储已安装模块实例的列表
__installed_modules: List[BaseModule] = []


# 递归地安装模块及其前置模块
def __recursive_module(module: BaseModule):
    """
    确保模块及其所有前置模块都被安装并添加到tick列表中。

    参数:
    - module: 当前要安装的模块

    返回值:
    无

    异常:
    - 如果前置模块未安装，则抛出异常
    """
    # 如果模块已安装，则无需重复安装
    if module in __installed_modules:
        return
    # 将当前模块添加到已安装模块列表中
    __installed_modules.append(module)
    # 遍历当前模块的所有前置模块
    for pre_module_class in module.pre_modules:
        # 通过前置模块类的id从字典中获取实际的模块实例
        pre_module = __class_dict.get(id(pre_module_class))
        # 如果前置模块不存在，则抛出异常
        if pre_module is None:
            raise Exception("前置模块未安装")
        # 递归地安装前置模块
        __recursive_module(pre_module)
    # 将当前模块的tick函数添加到待执行列表中
    __tick_list.append(module.tick)
    pass


# 安装一组模块
def install(modules: List[BaseModule]):
    """
    安装一组模块及其所有前置模块。

    参数:
    - modules: 需要安装的模块列表
    """
    # 将模块添加到类字典中，以便后续通过类id获取模块实例
    for module in modules:
        __class_dict[id(module.__class__)] = module
    # 遍历所有模块，递归安装
    for module in modules:
        __recursive_module(module)


def tick():
    """
    调用列表中的每个tick函数。
    """
    while True:
        for __tick in __tick_list:
            __tick()
