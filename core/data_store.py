from typing import Dict, Optional, List, Any, TypeVar, Union, Type


# 定义Key类，用于创建唯一的存储键
class Key:
    def __init__(self, id: str):
        self.__id = id

    def __repr__(self):
        return self.__class__.__name__ + ":" + self.__id

    def __str__(self):
        return self.__repr__()


# 全局字典，用于存储键值对
_dict: Dict[str, Any] = {}
# 键类型到列表的映射，用于记录每个键类型对应的所有值
__key_class_map_list: Dict[str, List] = {}

# 泛型变量，用于表示任意类型的值
Value = TypeVar("Value")


# 内部函数，用于获取特定键类型对应的值列表
def __get_list(key_type: str):
    result = __key_class_map_list.get(key_type)
    if result is None:
        __key_class_map_list[key_type] = result = []
    return result


# 根据键获取值，如果键不存在，则返回None
def get(key: Key) -> Optional[Value]:
    return _dict.get(repr(key))


# 根据键获取值，如果键不存在，则抛出ValueError异常
def fetch(key: Key) -> Value:
    result = get(key)
    if result is None:
        raise ValueError(f"Entity {repr(key)} not found")
    return result


def set(key: Union[Key, str], value: Value) -> bool:
    """
    设置键的值并返回是否有更改。

    参数:
    - key: 键，可以是Key实例或字符串。如果键是Key实例，它会被转换为字符串。
    - value: 要设置的值。

    返回:
    - bool: 如果值有更改，返回True；否则返回False。
    """
    old_value = _dict.get(str(key))
    changed = value != old_value

    if isinstance(key, str):
        _dict[key] = value
    else:
        key = str(key)
        _dict[key] = value
        __get_list(key).append(value)

    return changed


# 删除键值对，如果键是字符串，则直接删除；如果键是Key实例，则从对应列表中移除值
def delete(key: Union[Key, str]):
    if isinstance(key, str):
        del _dict[key]
    else:
        value = get(key)
        if value is None:
            return
        key = str(key)
        del _dict[key]
        __get_list(key).remove(value)


# 获取特定键类型的所有值列表
def get_list(key_type: Type[Key]) -> List[Value]:
    return __get_list(key_type.__name__)
