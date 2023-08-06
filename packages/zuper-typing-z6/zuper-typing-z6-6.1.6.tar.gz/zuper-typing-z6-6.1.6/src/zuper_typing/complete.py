from zuper_commons.types import ZTypeError
from zuper_typing import (
    asdict_not_recursive,
    is_CustomDict,
    is_CustomList,
    is_CustomSet,
    is_CustomTuple,
    is_dataclass_instance,
)


class NotCompleteType(ZTypeError):
    pass


def check_complete_types(x: object, **kwargs):
    try:
        if isinstance(x, dict):
            T = type(x)
            if not is_CustomDict(type(x)):
                raise NotCompleteType("Found", T=T)
            for k, v in x.items():
                check_complete_types(v, k=k)
        if isinstance(x, list):
            T = type(x)
            if not is_CustomList(type(x)):
                raise NotCompleteType("Found", T=T)
            for i, v in enumerate(x):
                check_complete_types(v, i=i)
        if isinstance(x, tuple):
            T = type(x)
            if not is_CustomTuple(type(x)):
                raise NotCompleteType("Found", T=T)
            for i, v in enumerate(x):
                check_complete_types(v, i=i)
        if isinstance(x, set):
            T = type(x)
            if not is_CustomSet(type(x)):
                raise NotCompleteType("Found", T=T)
            for i, v in enumerate(x):
                check_complete_types(v, i=i)
        elif is_dataclass_instance(x):
            for k, v in asdict_not_recursive(x).items():
                check_complete_types(x=v, field=k, ob=x)
    except NotCompleteType as e:
        raise NotCompleteType(x=x, **kwargs) from e
