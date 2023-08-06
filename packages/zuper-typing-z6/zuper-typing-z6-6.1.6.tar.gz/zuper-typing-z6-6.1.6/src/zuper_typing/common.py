from typing import Any

from .my_dict import make_CustomTuple, make_dict, make_list, make_set

__all__ = [
    "DictStrStr",
    "SetStr",
    "DictStrType",
    "DictStrObject",
    "ListStr",
    "DictStrAny",
    "empty_tuple",
    "EmptyTupleType",
]

DictStrStr = make_dict(str, str)
DictStrObject = make_dict(str, object)
DictStrAny = make_dict(str, Any)
DictStrType = make_dict(str, type)
SetStr = make_set(str)
ListStr = make_list(str)

EmptyTupleType = make_CustomTuple(())
empty_tuple = EmptyTupleType()
