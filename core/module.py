import abc
from typing import Any


class BaseModule(abc.ABC):
    """
    基础模块类，定义了模块的基本结构和行为。
    """

    def __init__(self, name: str, description: str, *pre_modules: Any):
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
