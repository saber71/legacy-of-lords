import abc
from typing import *

from pydantic import BaseModel

# 定义一个泛型变量Payload，用于表示事件的数据载荷
Payload = TypeVar("Payload")


class Event(Generic[Payload], abc.ABC):
    """
    定义一个事件基类，用于创建具体事件类的模板。

    参数:
    - data: Payload类型，事件的具体数据。
    - stoppable: bool类型，默认为True，表示事件是否可以被停止传播。
    """

    def __init__(self, data: Payload, stoppable: bool = True):
        # 初始化事件的名称、数据和是否可停止传播的属性
        self.name = self.__class__.__name__
        self.data = data
        self.__stoppable = stoppable
        self.__stop = False

    # 定义stop属性的getter方法，用于获取事件是否停止传播的状态
    @property
    def stop(self):
        return self.__stop

    # 定义stop属性的setter方法，用于设置事件是否停止传播的状态，但只有当事件是可停止时才能设置
    @stop.setter
    def stop(self, value: bool):
        if self.__stoppable:
            self.__stop = value


# 定义一个泛型变量EventInstance，用于表示事件实例，它是一个事件的具体实现
EventInstance = TypeVar("EventInstance", bound=Event)
# 定义一个类型别名EventListenerFn，用于表示事件监听器的回调函数
EventListenerFn = Callable[[EventInstance], None]


class EventListener(BaseModel):
    """
    定义一个事件监听器类，包含回调函数、是否仅执行一次以及优先级属性。

    属性:
    - fn: EventListenerFn类型，事件的回调函数。
    - once: bool类型，表示事件监听器是否仅执行一次。
    - priority: int类型，表示事件监听器的优先级。
    """

    fn: EventListenerFn
    once: bool
    priority: int


class EventBus:
    """
    定义一个事件总线类，用于管理和分发事件。

    属性:
    - __listeners: 一个字典，用于存储事件类型和对应的监听器列表。
    """

    __listeners: Dict[str, List[EventListener]]

    def __init__(self):
        # 初始化事件总线的监听器字典
        self.__listeners = {}

    def clear(self):
        """
        清空所有事件监听器。
        """
        self.__listeners = {}
        return self

    def emit(self, event: EventInstance):
        """
        触发一个事件，通知所有注册的监听器。

        参数:
        - event: EventInstance类型，要触发的事件实例。
        """
        # 获取事件的监听器列表
        listeners = self.__listeners.get(event.name)
        if listeners is not None:
            for listener in listeners:
                listener.fn(event)
                if event.stop:
                    break

    def on(
        self,
        event_type: Type[EventInstance],
        callback: EventListenerFn,
        once: bool = False,
        priority: int = 0,
    ):
        """
        注册一个事件监听器。

        参数:
        - event_type: Type[EventInstance]类型，事件的类型。
        - callback: EventListenerFn类型，事件的回调函数。
        - once: bool类型，默认为False，表示监听器是否仅执行一次。
        - priority: int类型，默认为0，表示监听器的优先级。

        返回:
        - 返回事件总线实例，支持链式调用。
        """
        # 获取或初始化事件的监听器列表
        listeners = self.__listeners.get(event_type.__name__)
        if listeners is None:
            listeners = []
            self.__listeners[event_type.__name__] = listeners
        # 添加新的监听器，并根据优先级进行排序
        listeners.append(EventListener(fn=callback, once=once, priority=priority))
        if priority != 0:
            listeners.sort(key=lambda x: x.priority, reverse=True)
        return self

    def off(self, event_type: Type[EventInstance], callback: EventListenerFn = None):
        """
        移除一个或多个事件监听器。

        参数:
        - event_type: Type[EventInstance]类型，事件的类型。
        - callback: EventListenerFn类型，要移除的监听器的回调函数，可选。

        返回:
        - 返回事件总线实例，支持链式调用。
        """
        # 获取事件的监听器列表
        listeners = self.__listeners.get(event_type.__name__)
        if listeners is not None:
            # 移除指定的监听器或清空所有监听器
            if callback is None:
                self.__listeners[event_type.__name__] = []
            else:
                self.__listeners[event_type.__name__] = [
                    listener for listener in listeners if listener.fn != callback
                ]
        return self


# 初始化全局的事件总线实例
event_bus = EventBus()
