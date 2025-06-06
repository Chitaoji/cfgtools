"""
Contains the template class: ConfigTemplate.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
import sys
from typing import TYPE_CHECKING, Callable, Iterable, Self

from .css import TREE_CSS_STYLE
from .utils.htmltree import HTMLTreeMaker

if TYPE_CHECKING:
    from ._typing import BasicObj, DataObj, UnwrappedDataObj

NoneType = type(None)

__all__ = ["MAX_LINE_WIDTH"]


MAX_LINE_WIDTH = 88


class ConfigTemplate:
    """
    A wrapper for reading and writing config files.

    Parameters
    ----------
    data : DataObj
        The config data to be wrapped.
    fileformat : ConfigFileFormat, optional
        File format, by default None.
    path : str | Path | None, optional
        File path, by default None.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file
        (if needed), by default None.

    Raises
    ------
    TypeError
        Raised if the config data has invalid type.

    """

    valid_types = (str, int, float, bool, NoneType, type, Callable)
    constructor = object
    sub_constructors = {
        dict: lambda: _DictConfigTemplate,
        list: lambda: _ListConfigTemplate,
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
            raise TypeError(f"invalid type of data: {data.__class__.__name__}")
        return cls.constructor.__new__(new_class)

    def __init__(self, data: "DataObj") -> None:
        if isinstance(data, self.__class__):
            return
        if not isinstance(data, (dict, list)):
            self.__obj = data

    def __getitem__(self, __key: "BasicObj") -> Self:
        raise TypeError(f"{self.__desc()} is not subscriptable")

    def __setitem__(self, __key: "BasicObj", __value: "DataObj") -> None:
        raise TypeError(f"{self.__desc()} does not support item assignment")

    def __repr__(self) -> str:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            s = flat
        else:
            s = self.repr()
        return f"cfgtools.config({s})"

    def _repr_mimebundle_(self, *_, **__) -> dict[str, str]:
        maker = self.to_html()
        maker.setcls("t")
        main_maker = HTMLTreeMaker()
        main_maker.add(maker)
        return {"text/html": main_maker.make("cfgtools-tree", TREE_CSS_STYLE)}

    def __str__(self) -> str:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            return flat
        return self.repr()

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

    def keys(self) -> "Iterable[BasicObj]":
        """If the config data is a mapping, provide a view of its wrapped keys."""
        raise TypeError(f"{self.__desc()} has no method keys()")

    def values(self) -> "Iterable[DataObj]":
        """If the config data is a mapping, provide a view of its wrapped values."""
        raise TypeError(f"{self.__desc()} has no method 'values()'")

    def items(self) -> "Iterable[tuple[BasicObj, DataObj]]":
        """If the config data is a mapping, provide a view of its wrapped items."""
        raise TypeError(f"{self.__desc()} has no method 'items()'")

    def append(self, __object: "DataObj") -> None:
        """If the config data is a list, append to its end."""
        raise TypeError(f"{self.__desc()} has no method 'append()'")

    def extend(self, __object: "Iterable[DataObj]") -> None:
        """If the config data is a list, extend it."""
        raise TypeError(f"{self.__desc()} has no method 'extend()'")

    def unwrap(self) -> "UnwrappedDataObj":
        """Returns the unwrapped config data."""
        return self.__obj

    def unwrap_top_level(self) -> "DataObj":
        """Returns the config data, with only the top level unwrapped."""
        return self.__obj

    def to_ini_dict(self) -> dict:
        """Reformat the config data with `.ini` format, and returns a dict."""
        obj = self.unwrap()
        if isinstance(obj, dict):
            if all(isinstance(v, dict) for v in obj.values()):
                return {
                    k: {x: json.dumps(y) for x, y in v.items()} for k, v in obj.items()
                }
            return {"null": {k: json.dumps(v) for k, v in obj.items()}}
        return {"null": {"null": json.dumps(obj)}}

    def to_dict(self) -> dict["BasicObj", "UnwrappedDataObj"]:
        """Returns the unwrapped config data if it's a mapping."""
        raise TypeError(f"{self.__desc()} can't be converted into a dict")

    def to_list(self) -> list["UnwrappedDataObj"]:
        """Returns the unwrapped config data if it's a list."""
        raise TypeError(f"{self.__desc()} can't be converted into a list")

    def to_html(self) -> HTMLTreeMaker:
        """Return an HTMLTreeMaker object for representing self."""
        return HTMLTreeMaker(repr(self.__obj).replace(">", "&gt").replace("<", "&lt"))

    def get_max_line_width(self) -> int:
        """Get the module variable `MAX_LINE_WIDTH`."""
        return getattr(sys.modules[__name__.rpartition(".")[0]], "MAX_LINE_WIDTH")

    def __desc(self) -> str:
        return f"config object of type {self.unwrap_top_level().__class__.__name__}"


class _DictConfigTemplate(ConfigTemplate):
    constructor = ConfigTemplate
    sub_constructors = {}

    def __init__(self, obj: "DataObj", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: dict["BasicObj", "DataObj"] = {}
        for k, v in obj.items():
            if not isinstance(k, self.valid_types):
                raise TypeError(f"invalid type of key: {k.__class__.__name__}")
            if isinstance(v, self.constructor):
                new_obj[k] = v
            else:
                new_obj[k] = self.constructor(v)
        self.__obj = new_obj

    def __getitem__(self, __key: "BasicObj") -> Self:
        return self.__obj[__key]

    def __setitem__(self, __key: "BasicObj", __value: "DataObj") -> None:
        if isinstance(__value, self.constructor):
            self.__obj[__key] = __value
        else:
            self.__obj[__key] = self.constructor(__value)

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "{\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for k, v in self.__obj.items():
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
        return self.__obj.keys()

    def values(self) -> Iterable["DataObj"]:
        return self.__obj.values()

    def items(self) -> Iterable[tuple["BasicObj", "DataObj"]]:
        return self.__obj.items()

    def unwrap(self) -> "UnwrappedDataObj":
        return {k: v.unwrap() for k, v in self.__obj.items()}

    def unwrap_top_level(self) -> "DataObj":
        return self.__obj

    def to_dict(self) -> dict["BasicObj", "UnwrappedDataObj"]:
        return self.unwrap()

    def to_html(self) -> HTMLTreeMaker:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            return HTMLTreeMaker(flat)
        maker = HTMLTreeMaker('{<span class="closed"> ... }</span>')
        for k, v in self.__obj.items():
            node = v.to_html()
            if node.has_child():
                node.setval(f"{k!r}: {node.getval()}")
                tail = node.get(-1)
                tail.setval(f"{tail.getval()},")
            else:
                node.setval(f"{k!r}: {node.getval()},")
            maker.add(node)
        maker.add("}", "t")
        return maker


class _ListConfigTemplate(ConfigTemplate):
    constructor = ConfigTemplate
    sub_constructors = {}

    def __init__(self, obj: "DataObj", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: list["DataObj"] = []
        for x in obj:
            if isinstance(x, self.constructor):
                new_obj.append(x)
            else:
                new_obj.append(self.constructor(x))
        self.__obj = new_obj

    def __getitem__(self, __key: int) -> Self:
        return self.__obj[__key]

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "[\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for x in self.__obj:
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

    def append(self, __object: "DataObj") -> None:
        if isinstance(__object, self.constructor):
            self.__obj.append(__object)
        else:
            self.__obj.append(self.constructor(__object))

    def extend(self, __iterable: Iterable["DataObj"]) -> None:
        if isinstance(__iterable, self.__class__):
            self.__obj.extend(list(__iterable))
        else:
            self.__obj.extend(list(self.constructor(list(__iterable))))

    def unwrap(self) -> "UnwrappedDataObj":
        return [x.unwrap() for x in self.__obj]

    def unwrap_top_level(self) -> "DataObj":
        return self.__obj

    def to_list(self) -> list["UnwrappedDataObj"]:
        return self.unwrap()

    def to_html(self) -> HTMLTreeMaker:
        if len(flat := repr(self.unwrap())) <= self.get_max_line_width():
            return HTMLTreeMaker(flat)
        maker = HTMLTreeMaker('[<span class="closed"> ... ]</span>')
        for x in self.__obj:
            node = x.to_html()
            if node.has_child():
                node.setval(f"{node.getval()}")
                tail = node.get(-1)
                tail.setval(f"{tail.getval()},")
            else:
                node.setval(f"{node.getval()},")
            maker.add(node)
        maker.add("]", "t")
        return maker


def _sep(level: int) -> str:
    return "    " * level
