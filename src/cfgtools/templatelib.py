"""
Contains the template class: ConfigTemplate.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Iterable, Iterator, Literal, Self

from htmlmaster import HTMLTreeMaker

from .css import TREE_CSS_STYLE

if TYPE_CHECKING:
    from ._typing import BasicObj, DataObj, UnwrappedDataObj
    from .iowrapper import ConfigIOWrapper

NoneType = type(None)

__all__ = ["MAX_LINE_WIDTH", "ANY", "RETURN", "YIELD", "NEVER"]


MAX_LINE_WIDTH = 88


@dataclass(unsafe_hash=True)
class Flag:
    """Template flag."""

    name: str

    def __repr__(self) -> str:
        return self.name


ANY = Flag("ANY")
RETURN = Flag("RETURN")
YIELD = Flag("YIELD")
NEVER = Flag("NEVER")


class ConfigTemplate:
    """
    A template for matching config objects.

    Parameters
    ----------
    data : DataObj
        Template data.

    Raises
    ------
    TypeError
        Raised if the template data has invalid type.

    """

    valid_types = (str, int, float, bool, NoneType, type, Callable, Flag)
    constructor = object
    sub_constructors = {
        dict: lambda: DictConfigTemplate,
        list: lambda: ListConfigTemplate,
    }

    def __new__(cls, data: "DataObj", *args, **kwargs) -> Self:
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            new_class = cls.sub_constructors[dict]()
        elif isinstance(data, list):
            new_class = cls.sub_constructors[list]()
        elif isinstance(data, cls.valid_types):
            new_class = cls
        else:
            raise TypeError(f"invalid type of data: {data.__class__.__name__!r}")
        return cls.constructor.__new__(new_class)

    def __init__(self, data: "DataObj") -> None:
        self.__status: Literal["", "d", "a", "r"] = ""
        if isinstance(data, self.__class__):
            return
        if not isinstance(data, (dict, list)):
            self.__obj = data

    def __getitem__(self, key: "BasicObj", /) -> Self:
        raise TypeError(f"{self.__desc()} is not subscriptable")

    def __setitem__(self, key: "BasicObj", value: "DataObj", /) -> None:
        raise TypeError(f"{self.__desc()} does not support item assignment")

    def __delitem__(self, key: "BasicObj", /) -> None:
        raise TypeError(f"cannot delete {self.__desc()}")

    def __repr__(self) -> str:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            s = flat
        else:
            s = self.repr()
        return f"cfgtools.template({s})"

    def _repr_mimebundle_(self, *_, **__) -> dict[str, str]:
        return {"text/html": self.to_html().make()}

    def __str__(self) -> str:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            return flat
        return self.repr()

    def __len__(self) -> int:
        raise TypeError(f"{self.__desc()} has no len()")

    def __contains__(self, key: "BasicObj", /) -> bool:
        raise TypeError(f"{self.__desc()} is not iterable")

    def __iter__(self) -> Iterator["DataObj"]:
        raise TypeError(f"{self.__desc()} is not iterable")

    def __bool__(self) -> bool:
        return True

    def __eq__(self, value: Self, /) -> bool:
        return isinstance(value, self.__class__) and self.unwrap() == value.unwrap()

    def repr(self, level: int = 0, /) -> str:
        """
        Represent self.

        Parameters
        ----------
        level : int, optional
            Depth level, by default 0.

        Returns
        -------
        str
            A representation of self.

        """
        _ = level
        return repr(self.__obj)

    def view_change(self) -> str:
        """View the change of self since initialized."""
        return repr(self.__obj)

    def keys(self) -> "Iterable[BasicObj]":
        """If the data is a mapping, provide a view of its wrapped keys."""
        raise TypeError(f"{self.__desc()} has no method keys()")

    def values(self) -> "Iterable[ConfigTemplate]":
        """If the data is a mapping, provide a view of its wrapped values."""
        raise TypeError(f"{self.__desc()} has no method values()")

    def items(self) -> Iterable[tuple["BasicObj", "ConfigTemplate"]]:
        """If the data is a mapping, provide a view of its wrapped items."""
        raise TypeError(f"{self.__desc()} has no method items()")

    def append(self, obj: "DataObj", /) -> None:
        """If the data is a list, append to its end."""
        raise TypeError(f"{self.__desc()} has no method append()")

    def extend(self, iterable: "Iterable[DataObj]", /) -> None:
        """If the data is a list, extend it."""
        raise TypeError(f"{self.__desc()} has no method extend()")

    def copy(self) -> Self:
        """Copy an instance of self."""
        constructor = self.__class__ if self.constructor is object else self.constructor
        return constructor(self.unwrap())

    def unwrap(self) -> "UnwrappedDataObj":
        """Returns the unwrapped data."""
        return self.__obj

    def unwrap_top_level(self) -> "DataObj":
        """Returns the data, with only the top level unwrapped."""
        return self.__obj

    def isinstance(self, cls: type) -> bool:
        """Returns is self instance of cls."""
        return isinstance(self.__obj, cls)

    def to_dict(self) -> dict["BasicObj", "UnwrappedDataObj"]:
        """Returns the unwrapped data if it's a mapping."""
        raise TypeError(f"{self.__desc()} can't be converted into a dict")

    def to_list(self) -> list["UnwrappedDataObj"]:
        """Returns the unwrapped data if it's a list."""
        raise TypeError(f"{self.__desc()} can't be converted into a list")

    def to_html(self) -> HTMLTreeMaker:
        """Return an HTMLTreeMaker object for representing self."""
        maker = self.get_html_node()
        maker.setcls("t")
        main_maker = HTMLTreeMaker()
        main_maker.add(maker)
        main_maker.setstyle(TREE_CSS_STYLE)
        main_maker.set_maincls("cfgtools-tree")
        return main_maker

    def get_html_node(self) -> HTMLTreeMaker:
        """
        Return a plain HTMLTreeMaker object for representing the current
        node.

        """
        return HTMLTreeMaker(repr(self.__obj).replace(">", "&gt").replace("<", "&lt"))

    def get_max_line_width(self) -> int:
        """Get the module variable `MAX_LINE_WIDTH`."""
        return getattr(sys.modules[__name__.rpartition(".")[0]], "MAX_LINE_WIDTH")

    def match(self, template: "DataObj", /) -> Self | None:
        """Match the template from the top level."""
        raise TypeError("can't match on a template")

    def fullmatch(self, template: "DataObj", /) -> Self | None:
        """Match the whole template from the top level."""
        raise TypeError("can't match on a template")

    def safematch(self, template: "DataObj", /) -> Self:
        """
        Match the whole template from the top level. Differences to
        `self.fullmatch()` that the result will always be an instance
        of self.

        NOTE: 'RETURN' tags and 'YIELD' tags are not supported in this
        method.

        """
        raise TypeError("can't match on a template")

    def search(self, template: "DataObj", /) -> Self | None:
        """Search for the template at any level."""
        raise TypeError("can't search on a template")

    def fill(
        self,
        constructor: type["ConfigIOWrapper"],
        wrapper: "ConfigIOWrapper | None" = None,
    ) -> "ConfigIOWrapper":
        """Fill the template with an iowrapper."""
        if isinstance(self.__obj, type):
            if wrapper is not None and wrapper.isinstance(self.__obj):
                return wrapper.copy()
            return constructor(self.__obj())
        if isinstance(self.__obj, Callable):
            if wrapper is not None and self.__obj(wrapper):
                return wrapper.copy()
            return constructor(None)
        if wrapper is None:
            return constructor(self.__obj)
        return wrapper.copy()

    def has_flag(self, flag: Flag, /) -> bool:
        """Returns whether the template includes template flags."""
        return self.__obj == flag

    def replace_flags(
        self, recorder: dict[str, "DataObj"] | None = None, /
    ) -> dict[str, "DataObj"]:
        """Replace all the template flags with callables."""
        if recorder is None:
            recorder = {}
        if not isinstance(self.__obj, Flag):
            return recorder

        if self.__obj == ANY:
            self.__obj = lambda x: True
        elif self.__obj == NEVER:
            self.__obj = lambda x: False
        elif self.__obj == RETURN:
            self.__obj = lambda x: bool(recorder.setdefault("RETURN", x)) or True
        elif self.__obj == YIELD:
            self.__obj = (
                lambda x: bool(recorder.update(YIELD=recorder.get("YIELD", []) + [x]))
                or True
            )
        return recorder

    def mark_as_deleted(self) -> None:
        """Mark self as deleted."""
        if self.is_template():
            raise TypeError("cannot delete a template")
        self.__status = "d"

    def mark_as_added(self) -> None:
        """Mark self as added."""
        if self.is_template():
            raise TypeError("cannot delete a template")
        self.__status = "a"

    def mark_as_replaced(self, new_value: Self, /) -> None:
        """Mark self as replaced."""
        if self.is_template():
            raise TypeError("cannot replace a template")
        self.__status = "r"

    def is_deleted(self) -> bool:
        """If self is marked as deleted."""
        return self.__status == "d"

    def is_present(self) -> bool:
        """If self is marked as deleted."""
        return self.__status != "d"

    def is_template(self) -> bool:
        """If self is a template."""
        return "Template" in self.__class__.__name__

    def __desc(self) -> str:
        return f"config object of type {self.unwrap_top_level().__class__.__name__!r}"


class DictConfigTemplate(ConfigTemplate):
    """Template of dict."""

    constructor = ConfigTemplate
    sub_constructors = {}

    def __init__(self, obj: "DataObj", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: dict["BasicObj", ConfigTemplate] = {}
        for k, v in obj.items():
            if not isinstance(k, self.valid_types):
                raise TypeError(f"invalid type of key: {k.__class__.__name__!r}")
            if isinstance(v, self.constructor):
                new_obj[k] = v
            else:
                new_obj[k] = self.constructor(v)
        self.__obj = new_obj

    def __getitem__(self, key: "BasicObj", /) -> Self:
        value = self.__obj[key]
        if value.is_deleted():
            raise KeyError(f"{key!r}")
        return value

    def __setitem__(self, key: "BasicObj", value: "DataObj", /) -> None:
        if not isinstance(value, self.constructor):
            value = self.constructor(value)
        value.mark_as_added()
        if key in self.__obj:
            self.__obj[key].mark_as_replaced(value)
        else:
            self.__obj[key] = value

    def __delitem__(self, key: "BasicObj", /) -> None:
        self.__obj[key].mark_as_deleted()

    def __len__(self) -> int:
        return len(self.unwrap_top_level())

    def __contains__(self, key: "BasicObj", /) -> bool:
        if key in self.__obj and self.__obj[key].is_present():
            return True
        return False

    def __iter__(self) -> Iterator["DataObj"]:
        return iter(self.unwrap_top_level())

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "{\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for k, v in self.__obj.items():
            if v.is_deleted():
                continue
            _head = lines[-1] if lines else ""
            _key = f"{k!r}: "
            _flat = repr(v.unwrap())
            if lines and (len(_head) + len(_key) + len(_flat) + 2 <= max_line_width):
                lines[-1] += " " + _key + _flat + ","
            elif len(seps) + len(_key) + len(_flat) < max_line_width:
                lines.append(seps + _key + _flat + ",")
            else:
                _child = v.repr(level + 1)
                if lines and (
                    len(_head) + len(_key) + len(_child) + 2 <= max_line_width
                ):
                    lines[-1] += " " + _key + _child + ","
                else:
                    lines.append(seps + _key + _child + ",")
        string += "\n".join(lines) + f"\n{_sep(level)}" "}"
        return string

    def keys(self) -> Iterable["BasicObj"]:
        return self.unwrap_top_level().keys()

    def values(self) -> Iterable["ConfigTemplate"]:
        return self.unwrap_top_level().values()

    def items(self) -> Iterable[tuple["BasicObj", "ConfigTemplate"]]:
        return self.unwrap_top_level().items()

    def unwrap(self) -> "UnwrappedDataObj":
        return {k: v.unwrap() for k, v in self.__obj.items() if v.is_present()}

    def unwrap_top_level(self) -> "DataObj":
        return {k: v for k, v in self.__obj.items() if v.is_present()}

    def isinstance(self, cls: type) -> bool:
        return isinstance(self.__obj, cls)

    def to_dict(self) -> dict["BasicObj", "UnwrappedDataObj"]:
        return self.unwrap()

    def get_html_node(self) -> HTMLTreeMaker:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            return HTMLTreeMaker(flat)
        maker = HTMLTreeMaker('{<span class="closed"> ... }</span>')
        for k, v in self.items():
            node = v.get_html_node()
            if node.has_child():
                node.setval(f"{k!r}: {node.getval()}")
                tail = node.get(-1)
                tail.setval(f"{tail.getval()},")
            else:
                node.setval(f"{k!r}: {node.getval()},")
            maker.add(node)
        maker.add("}", "t")
        return maker

    def fill(
        self,
        constructor: type["ConfigIOWrapper"],
        wrapper: "ConfigIOWrapper | None" = None,
    ) -> "ConfigIOWrapper":
        if not wrapper.isinstance(dict):
            return constructor({k: v.fill(constructor) for k, v in self.items()})

        new_data = {}
        for kt, vt in self.items():
            for k, v in wrapper.items():
                if constructor(k).match(kt):
                    new_data[k] = vt.fill(constructor, v)
                    break
            else:
                new_data[self.constructor(kt).fill(constructor).unwrap()] = vt.fill(
                    constructor
                )

        return constructor(new_data)

    def has_flag(self, flag: Flag, /) -> bool:
        return any(k == flag or v.has_flag(flag) for k, v in self.items())

    def replace_flags(
        self, recorder: dict[str, "DataObj"] | None = None, /
    ) -> dict[str, "DataObj"]:
        if recorder is None:
            recorder = {}

        for v in self.values():
            v.replace_flags(recorder)

        return recorder


class ListConfigTemplate(ConfigTemplate):
    """Template of list."""

    constructor = ConfigTemplate
    sub_constructors = {}

    def __init__(self, obj: "DataObj", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: list[ConfigTemplate] = []
        for x in obj:
            if isinstance(x, self.constructor):
                new_obj.append(x)
            else:
                new_obj.append(self.constructor(x))
        self.__obj = new_obj

    def __getitem__(self, key: int, /) -> Self:
        value = self.__obj[key]
        if value.is_deleted():
            raise KeyError(f"{key!r}")
        return value

    def __setitem__(self, key: int, value: "DataObj", /) -> None:
        if not isinstance(value, self.constructor):
            value = self.constructor(value)
        value.mark_as_added()
        if key in self.__obj:
            self.__obj[key].mark_as_replaced(value)
        else:
            self.__obj[key] = value

    def __delitem__(self, key: int, /) -> None:
        self.__obj[key].mark_as_deleted()

    def __len__(self) -> int:
        return len(self.unwrap_top_level())

    def __contains__(self, value: "BasicObj", /) -> bool:
        return value in self.unwrap_top_level()

    def __iter__(self) -> Iterator["DataObj"]:
        return iter(self.unwrap_top_level())

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "[\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for x in self.__obj:
            if x.is_deleted():
                continue
            _head = lines[-1] if lines else ""
            _flat = repr(x.unwrap())
            if lines and (len(_head) + len(_flat) + 2 <= max_line_width):
                lines[-1] += " " + _flat + ","
            elif len(_head) + len(_flat) < max_line_width:
                lines.append(seps + _flat + ",")
            else:
                _child = x.repr(level + 1)
                if lines and (len(_head) + len(_child) + 2 <= max_line_width):
                    lines[-1] += " " + _child + ","
                else:
                    lines.append(seps + _child + ",")
        string += "\n".join(lines) + f"\n{_sep(level)}" + "]"
        return string

    def append(self, obj: "DataObj", /) -> None:
        if not isinstance(obj, self.constructor):
            obj = self.constructor(obj)
        obj.mark_as_added()
        self.__obj.append(obj)

    def extend(self, iterable: Iterable["DataObj"], /) -> None:
        if not isinstance(iterable, self.__class__):
            iterable = self.constructor(list(iterable))
        for x in iterable:
            x.mark_as_added()
        self.__obj.extend(list(iterable))

    def unwrap(self) -> "UnwrappedDataObj":
        return [x.unwrap() for x in self.__obj if x.is_present()]

    def unwrap_top_level(self) -> "DataObj":
        return [x for x in self.__obj if x.is_present()]

    def isinstance(self, cls: type) -> bool:
        return isinstance(self.__obj, cls)

    def to_list(self) -> list["UnwrappedDataObj"]:
        return self.unwrap()

    def get_html_node(self) -> HTMLTreeMaker:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            return HTMLTreeMaker(flat)
        maker = HTMLTreeMaker('[<span class="closed"> ... ]</span>')
        for x in self:
            node = x.get_html_node()
            if node.has_child():
                node.setval(f"{node.getval()}")
                tail = node.get(-1)
                tail.setval(f"{tail.getval()},")
            else:
                node.setval(f"{node.getval()},")
            maker.add(node)
        maker.add("]", "t")
        return maker

    def has_flag(self, flag: Flag, /) -> bool:
        return any(x.has_flag() for x in self)

    def replace_flags(
        self, recorder: dict[str, "DataObj"] | None = None, /
    ) -> dict[str, "DataObj"]:
        if recorder is None:
            recorder = {}

        for x in self:
            x.replace_flags(recorder)

        return recorder

    def fill(
        self,
        constructor: type["ConfigIOWrapper"],
        wrapper: "ConfigIOWrapper | None" = None,
    ) -> "ConfigIOWrapper":
        if not wrapper.isinstance(list):
            return constructor([x.fill(constructor) for x in self])

        new_data = []
        len_wrapper = len(wrapper)
        for i, xt in enumerate(self):
            if i < len_wrapper:
                new_data.append(xt.fill(constructor, wrapper[i]))
            else:
                new_data.append(xt.fill(constructor))

        return constructor(new_data)


def _sep(level: int) -> str:
    return "    " * level
