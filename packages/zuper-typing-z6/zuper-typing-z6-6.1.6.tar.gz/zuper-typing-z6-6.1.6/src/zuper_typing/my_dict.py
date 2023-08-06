from typing import Any, cast, ClassVar, Dict, List, Set, Tuple, Type, TypeVar

from zuper_commons.types import ZTypeError, ZValueError
from .aliases import TypeLike
from .annotations_tricks import (
    get_Dict_args,
    get_Dict_name_K_V,
    get_List_arg,
    get_Set_arg,
    get_Set_name_V,
    get_tuple_types,
    is_Dict,
    is_FixedTuple,
    is_List,
    is_Set,
    is_Tuple,
    name_for_type_like,
)

_V = TypeVar("_V")
_K = TypeVar("_K")

_X = TypeVar("_X")
_Y = TypeVar("_Y")
_Z = TypeVar("_Z")

__all__ = [
    "MyBytes",
    "MyStr",
    "get_ListLike_arg",
    "get_FixedTupleLike_args",
    "get_CustomTuple_args",
    "get_CustomDict_args",
    "get_CustomList_arg",
    "get_CustomSet_arg",
    "get_Dict_args",
    "get_DictLike_args",
    "get_Dict_name_K_V",
    "get_List_arg",
    "get_DictLike_name",
    "get_ListLike_name",
    "get_Set_arg",
    "get_Set_name_V",
    "get_SetLike_arg",
    "get_SetLike_name",
    "is_ListLike",
    "is_CustomDict",
    "is_CustomList",
    "is_CustomSet",
    "is_CustomTuple",
    "is_Dict",
    "is_DictLike",
    "is_DictLike_canonical",
    "is_FixedTupleLike",
    "is_List",
    "is_ListLike_canonical",
    "is_Set",
    "is_SetLike",
    "is_SetLike_canonical",
    "make_list",
    "make_CustomTuple",
    "make_dict",
    "make_set",
    "CustomTuple",
    "CustomDict",
    "CustomList",
    "CustomSet",
    "lift_to_customtuple",
    "lift_to_customtuple_type",
    "is_TupleLike",
    "get_FixedTupleLike_args",
    "get_FixedTupleLike_name",
]


class MyBytes(bytes):
    pass


class MyStr(str):
    pass


class CustomSet(set):
    __set_type__: ClassVar[type]

    def __hash__(self) -> Any:
        try:
            return self._cached_hash
        except AttributeError:
            try:
                h = self._cached_hash = hash(tuple(sorted(self)))
            except TypeError:  # pragma: no cover
                h = self._cached_hash = hash(tuple(self))
            return h


ATT_LIST_TYPE = "__list_type__"


class CustomList(list):
    __list_type__: ClassVar[type]

    def __hash__(self) -> Any:  # pragma: no cover
        try:
            return self._cached_hash
        except AttributeError:  # pragma: no cover
            h = self._cached_hash = hash(tuple(self))
            return h

    def __getitem__(self, i):
        T = type(self)
        if isinstance(i, slice):
            # noinspection PyArgumentList
            return T(list.__getitem__(self, i))
        return list.__getitem__(self, i)

    def __add__(self, other):
        r = super().__add__(other)
        T = type(self)
        # noinspection PyArgumentList
        return T(r)


check_tuple_values = True


class CustomTuple(tuple):
    __tuple_types__: ClassVar[Tuple[type, ...]]

    def __new__(cls, *all_args):
        if not all_args:
            args = ()
        else:
            (args,) = all_args
        from .subcheck import value_liskov

        if check_tuple_values:
            for i, (a, T) in enumerate(zip(args, cls.__tuple_types__)):
                can = value_liskov(a, T)
                if not can:
                    msg = f"Entry #{i} does not pass the liskov test."
                    raise ZValueError(
                        msg, args=args, __tuple_types__=cls.__tuple_types__, i=i, a=a, T=T, can=can
                    )
        # logger.info('hello', __tuple_types__=cls.__tuple_types__, args=args)
        # noinspection PyTypeChecker
        return tuple.__new__(cls, args)

    def __hash__(self) -> Any:  # pragma: no cover
        try:
            return self._cached_hash
        except AttributeError:  # pragma: no cover
            h = self._cached_hash = hash(tuple(self))
            return h

    def __getitem__(self, i):

        if isinstance(i, slice):
            vals = super().__getitem__(i)
            types = self.__tuple_types__[i]
            T2 = make_CustomTuple(types)
            # noinspection PyArgumentList
            return T2(vals)

        else:
            return super().__getitem__(i)

    def __add__(self, other):
        vals = super().__add__(other)
        if isinstance(other, CustomTuple):
            types2 = type(other).__tuple_types__
        else:
            types2 = (Any,) * len(other)

        T2 = make_CustomTuple(self.__tuple_types__ + types2)
        # noinspection PyArgumentList
        return T2(vals)


class CustomDict(dict):
    __dict_type__: ClassVar[Tuple[type, type]]

    def __hash__(self) -> Any:
        try:
            return self._cached_hash
        except AttributeError:
            pass

        try:
            it = tuple(sorted(self.items()))
        except TypeError:
            it = tuple(self.items())

        try:
            h = self._cached_hash = hash(tuple(it))
        except TypeError as e:
            msg = "Cannot compute hash"
            raise ZTypeError(msg, it=it) from e
        return h

    def copy(self: _X) -> _X:
        return type(self)(self)


def get_CustomSet_arg(x: Type[CustomSet]) -> TypeLike:
    assert is_CustomSet(x), x
    return x.__set_type__


def get_CustomList_arg(x: Type[CustomList]) -> TypeLike:
    assert is_CustomList(x), x
    if not hasattr(x, ATT_LIST_TYPE):
        msg = "CustomList without __list_type__?"
        raise ZValueError(msg, x=type(x), x2=str(x), d=x.__dict__)
    return getattr(x, ATT_LIST_TYPE)


def get_CustomDict_args(x: Type[CustomDict]) -> Tuple[TypeLike, TypeLike]:
    assert is_CustomDict(x), x
    return x.__dict_type__


def get_CustomTuple_args(x: Type[CustomTuple]) -> Tuple[TypeLike, ...]:
    assert is_CustomTuple(x), x
    return x.__tuple_types__


def is_CustomSet(x: TypeLike) -> bool:
    return isinstance(x, type) and (x is not CustomSet) and issubclass(x, CustomSet)


def is_CustomList(x: TypeLike) -> bool:
    return isinstance(x, type) and (x is not CustomList) and issubclass(x, CustomList)


def is_CustomDict(x: TypeLike) -> bool:
    return isinstance(x, type) and (x is not CustomDict) and issubclass(x, CustomDict)


def is_CustomTuple(x: TypeLike) -> bool:
    return isinstance(x, type) and (x is not CustomTuple) and issubclass(x, CustomTuple)


def is_SetLike(x: TypeLike) -> bool:
    return (x is set) or is_Set(x) or is_CustomSet(x)


def is_ListLike(x: TypeLike) -> bool:
    return (x is list) or is_List(x) or is_CustomList(x)


def is_DictLike(x: TypeLike) -> bool:
    return (x is dict) or is_Dict(x) or is_CustomDict(x)


def is_ListLike_canonical(x: Type[List]) -> bool:
    return is_CustomList(x)


def is_DictLike_canonical(x: Type[Dict]) -> bool:
    return is_CustomDict(x)


def is_SetLike_canonical(x: Type[Set]) -> bool:
    return is_CustomSet(x)


def get_SetLike_arg(x: Type[Set[_V]]) -> Type[_V]:
    if x is set:
        return Any

    if is_Set(x):
        return get_Set_arg(x)

    if is_CustomSet(x):
        x = cast(Type[CustomSet], x)
        return get_CustomSet_arg(x)

    assert False, x


def get_ListLike_arg(x: Type[List[_V]]) -> Type[_V]:
    if x is list:
        return Any

    if is_List(x):
        return get_List_arg(x)

    if is_CustomList(x):
        # noinspection PyTypeChecker
        return get_CustomList_arg(x)

    assert False, x


def get_DictLike_args(x: Type[Dict[_K, _V]]) -> Tuple[Type[_K], Type[_V]]:
    assert is_DictLike(x), x
    if is_Dict(x):
        return get_Dict_args(x)
    elif is_CustomDict(x):
        x = cast(Type[CustomDict], x)
        return get_CustomDict_args(x)
    elif x is dict:
        return Any, Any
    else:
        assert False, x


def get_DictLike_name(T: Type[Dict]) -> str:
    assert is_DictLike(T)
    K, V = get_DictLike_args(T)
    return get_Dict_name_K_V(K, V)


def get_ListLike_name(x: Type[List]) -> str:
    V = get_ListLike_arg(x)
    return "List[%s]" % name_for_type_like(V)


def get_SetLike_name(x: Type[Set]) -> str:
    v = get_SetLike_arg(x)
    return "Set[%s]" % name_for_type_like(v)


Q_ = TypeVar("Q_")
K_ = TypeVar("K_")
V_ = TypeVar("V_")


class Caches:
    use_cache = True
    make_set_cache: Dict[Type[Q_], Type[CustomSet]] = {}
    make_list_cache: Dict[Type[Q_], Type[CustomList]] = {}
    make_dict_cache: Dict[Tuple[Type[K_], Type[V_]], Type[CustomDict]] = {}
    make_tuple_cache: Dict[Tuple[TypeLike, ...], Type[CustomTuple]] = {}


def assert_good_typelike(x: TypeLike) -> None:
    if isinstance(x, type):
        return
    # if is_dataclass(type(x)):
    #     n = type(x).__name__
    #     if n in ["Constant"]:
    #         raise AssertionError(x)


def make_list(V_: Type[_X]) -> Type[List[Type[_X]]]:
    if Caches.use_cache:
        if V_ in Caches.make_list_cache:
            return Caches.make_list_cache[V_]

    assert_good_typelike(V_)

    class MyType(type):
        def __eq__(self, other) -> bool:
            V2 = getattr(self, "__list_type__")
            if is_List(other):
                return V2 == get_List_arg(other)
            res2 = (
                isinstance(other, type)
                and issubclass(other, CustomList)
                and other.__list_type__ == V2
            )
            return res2

        def __hash__(cls) -> Any:  # pragma: no cover
            return 1  # XXX
            # logger.debug(f'here ___eq__ {self} {other} {issubclass(other, CustomList)} = {res}')

    def copy(self: _X) -> _X:
        return type(self)(self)

    attrs = {"__list_type__": V_, "copy": copy}

    # name = get_List_name(V)
    name = "List[%s]" % name_for_type_like(V_)

    res = MyType(name, (CustomList,), attrs)

    setattr(res, "EMPTY", res([]))
    Caches.make_list_cache[V_] = res
    add_class_to_module(res)
    # noinspection PyTypeChecker
    return res


def add_class_to_module(C: type) -> None:
    """ Adds the class to the module's dictionary, so that Pickle can save it. """
    name = C.__name__
    g = globals()
    # from . import logger
    # logger.info(f'added class {name}')
    g[name] = C


def lift_to_customtuple(vs: tuple):

    ts = tuple(type(_) for _ in vs)
    T = make_CustomTuple(ts)
    return T(vs)


def lift_to_customtuple_type(vs: tuple, T: type):
    ts = tuple(T for _ in vs)
    T = make_CustomTuple(ts)
    return T(vs)


def make_CustomTuple(Vs: Tuple[TypeLike, ...]) -> Type[Tuple]:
    # if len(Vs) == 2:
    #     from zuper_lang.lang import Constant, EXP, EV
    #     if Vs[0] is Constant and Vs[1] is EV:
    #         raise ZValueError(Vs=Vs)
    if Caches.use_cache:
        if Vs in Caches.make_tuple_cache:
            return Caches.make_tuple_cache[Vs]

    for _ in Vs:
        assert_good_typelike(_)

    ATT_TUPLE_TYPES = "__tuple_types__"

    class MyTupleType(type):
        def __eq__(self, other) -> bool:
            V2 = getattr(self, ATT_TUPLE_TYPES)
            if is_FixedTupleLike(other):
                return V2 == get_FixedTupleLike_args(other)
            res2 = (
                isinstance(other, type)
                and issubclass(other, CustomTuple)
                and getattr(other, ATT_TUPLE_TYPES) == V2
            )
            return res2

        def __hash__(cls) -> Any:  # pragma: no cover
            return 1  # XXX
            # logger.debug(f'here ___eq__ {self} {other} {issubclass(other, CustomList)} = {res}')

    def copy(self: _X) -> _X:
        return type(self)(self)

    attrs = {ATT_TUPLE_TYPES: Vs, "copy": copy}

    # name = get_List_name(V)
    s = ",".join(name_for_type_like(_) for _ in Vs)
    name = "Tuple[%s]" % s

    res = MyTupleType(name, (CustomTuple,), attrs)

    # setattr(res, "EMPTY", res())
    Caches.make_tuple_cache[V_] = res
    add_class_to_module(res)
    # noinspection PyTypeChecker
    return res


def make_set(V: TypeLike) -> Type[CustomSet]:
    if Caches.use_cache:
        if V in Caches.make_set_cache:
            return Caches.make_set_cache[V]

    assert_good_typelike(V)

    class MyType(type):
        def __eq__(self, other) -> bool:
            V2 = getattr(self, "__set_type__")
            if is_Set(other):
                return V2 == get_Set_arg(other)
            res2 = (
                isinstance(other, type)
                and issubclass(other, CustomSet)
                and other.__set_type__ == V2
            )
            return res2

        def __hash__(cls) -> Any:  # pragma: no cover
            return 1  # XXX

    def copy(self: _X) -> _X:
        return type(self)(self)

    attrs = {"__set_type__": V, "copy": copy}
    name = get_Set_name_V(V)
    res = MyType(name, (CustomSet,), attrs)
    setattr(res, "EMPTY", res([]))
    Caches.make_set_cache[V] = res
    add_class_to_module(res)
    # noinspection PyTypeChecker
    return res


# from . import logger
# def make_dict(K: Type[X], V: Type[Y]) -> Type[Dict[Type[X], Type[Y]]]:
def make_dict(K: TypeLike, V: TypeLike) -> type:  # Type[CustomDict]:
    key = (K, V)
    if Caches.use_cache:

        if key in Caches.make_dict_cache:
            return Caches.make_dict_cache[key]

    assert_good_typelike(K)
    assert_good_typelike(V)

    class MyType(type):
        def __eq__(self, other) -> bool:
            K2, V2 = getattr(self, "__dict_type__")
            if is_Dict(other):
                K1, V1 = get_Dict_args(other)
                return K2 == K1 and V2 == V1
            res2 = (
                isinstance(other, type)
                and issubclass(other, CustomDict)
                and other.__dict_type__ == (K2, V2)
            )
            return res2

        def __hash__(cls) -> Any:  # pragma: no cover
            return 1  # XXX

    if isinstance(V, str):  # pragma: no cover
        msg = f"Trying to make dict with K = {K!r} and V = {V!r}; I need types, not strings."
        raise ValueError(msg)
    # warnings.warn('Creating dict', stacklevel=2)

    attrs = {"__dict_type__": (K, V)}
    name = get_Dict_name_K_V(K, V)

    res = MyType(name, (CustomDict,), attrs)

    setattr(res, "EMPTY", res({}))
    Caches.make_dict_cache[key] = res

    # noinspection PyUnresolvedReferences
    # import zuper_typing.my_dict
    #
    # zuper_typing.my_dict.__dict__[res.__name__] = res
    # noinspection PyTypeChecker
    add_class_to_module(res)
    return res


def is_TupleLike(x: TypeLike) -> bool:
    return is_Tuple(x) or x is tuple or is_CustomTuple(x)


def is_FixedTupleLike(x: TypeLike) -> bool:

    return is_FixedTuple(x) or is_CustomTuple(x)


def get_FixedTupleLike_args(x: Type[Tuple]) -> Tuple[TypeLike, ...]:
    assert is_FixedTupleLike(x), x
    if is_FixedTuple(x):
        x = cast(Type[Tuple], x)
        return get_tuple_types(x)

    if is_CustomTuple(x):
        x = cast(Type[CustomTuple], x)
        return get_CustomTuple_args(x)
    assert False, x


def get_FixedTupleLike_name(V: Type[Tuple]) -> str:
    return "Tuple[%s]" % ",".join(name_for_type_like(_) for _ in get_FixedTupleLike_args(V))
