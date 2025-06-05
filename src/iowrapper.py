"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterable, Self

from .css import TREE_CSS_STYLE
from .saver import ConfigSaver
from .utils.htmltree import HTMLTreeMaker

if TYPE_CHECKING:
    from ._typing import BasicObj, ConfigFileFormat, DataObj, UnwrappedDataObj
NoneType = type(None)

__all__ = ["FileFormatError", "MAX_LINE_WIDTH"]


SUFFIX_MAPPING = {
    ".yaml": "yaml",
    ".yml": "yaml",
    ".pickle": "pickle",
    ".pkl": "pickle",
    ".json": "json",
    ".ini": "ini",
    ".txt": "text",
    ".bytes": "bytes",
}
FORMAT_MAPPING = {
    "yaml": "yaml",
    "yml": "yaml",
    "pickle": "pickle",
    "pkl": "pickle",
    "json": "json",
    "ini": "ini",
    "text": "text",
    "txt": "text",
    "bytes": "bytes",
}
MAX_LINE_WIDTH = 88


class ConfigIOWrapper(ConfigSaver):
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

    valid_types = (str, int, float, bool, NoneType)
    constructor = object
    sub_constructors = {
        dict: lambda: _DictConfigIOWrapper,
        list: lambda: _ListConfigIOWrapper,
    }
    is_template = False

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
            raise TypeError(f"invalid config type: {data.__class__.__name__}")
        return cls.constructor.__new__(new_class)

    def __init__(
        self,
        data: "DataObj",
        fileformat: "ConfigFileFormat | None" = None,
        /,
        path: str | Path | None = None,
        encoding: str | None = None,
    ) -> None:
        if isinstance(data, self.__class__):
            return
        self.__obj = data
        self.fileformat = fileformat
        self.overwrite_ok = True
        if path is None:
            self.path = None
        else:
            path = Path(path)
            self.path = path.absolute().relative_to(path.cwd()).as_posix()
        self.encoding = encoding

    def __getitem__(self, __key: "BasicObj") -> Self:
        raise TypeError(f"{self.__desc()} is not subscriptable")

    def __setitem__(self, __key: "BasicObj", __value: "DataObj") -> None:
        raise TypeError(f"{self.__desc()} does not support item assignment")

    def __enter__(self) -> Self:
        if self.path is None:
            raise TypeError("no default file path, please run self.set_path() first")
        if not self.overwrite_ok:
            raise TypeError(
                "overwriting the original path is not allowed, please run "
                "self.unlock() first"
            )
        self.lock()
        return self

    def __exit__(self, *args) -> None:
        self.unlock()
        self.save()

    def __repr__(self) -> str:
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
            s = flat
        else:
            s = self.repr()
        return f"cfgtools.config({s})"

    def _repr_mimebundle_(self, *_, **__) -> dict[str, str]:
        maker = self.to_html()
        if isinstance(maker, list):
            merged_html = HTMLTreeMaker()
            merged_html.add(maker)
            maker = merged_html
        info = (
            f"format: {self.fileformat!r} | path: {self.path!r} "
            f"| encoding: {self.encoding!r}"
        )
        maker.setcls("t")
        main_maker = HTMLTreeMaker()
        main_maker.add(maker)
        if not self.is_template:
            main_maker.add(info, "i")
        return {"text/html": main_maker.make("cfgtools-tree", TREE_CSS_STYLE)}

    def __str__(self) -> str:
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
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

    def match(self, template: "DataObj", /) -> Self | None:
        """Match the template from the top level."""
        if self.is_template:
            raise TypeError("can't match on a template")
        if isinstance(template, ConfigIOWrapper):
            if not template.is_template:
                raise TypeError("expected a config template")
        else:
            template = ConfigTemplate(template)
        match template.type():
            case "list":
                pass
            case "dict":
                pass
            case "type":
                if isinstance(self.__obj, template.to_object()):
                    return self
            case "function":
                if template.to_object()(self.__obj):
                    return self
            case _:
                if self.__obj == template.to_object():
                    return self
        return None

    def save(
        self,
        path: str | Path | None = None,
        fileformat: "ConfigFileFormat | None" = None,
        /,
        encoding: str | None = None,
    ) -> None:
        """
        Save the config.

        Parameters
        ----------
        path : str | Path | None, optional
            File path, by default None. If not specified, use `self.path`
            instead.
        fileformat : ConfigFileFormat | None, optional
            File format to save, by default None. If not specified, the
            file format will be automatically decided.
        encoding : str | None, optional
            The name of the encoding used to decode or encode the file
            (if needed), by default None. If not specified, use
            `self.encoding` instead.

        Raises
        ------
        ValueError
            Raised if both `path` and `self.path` are None.
        FileFormatError
            Raised if the file format is not supported.
        TypeError
            Raised if `self.overwrite_ok` is False.

        """
        if path is None:
            if self.path is None:
                raise ValueError(
                    "no default file path, please specify the path or run "
                    "self.set_path() first"
                )
            if not self.overwrite_ok:
                raise TypeError(
                    "overwriting the original path is not allowed, please run "
                    "self.unlock() first"
                )
            path = self.path
        if fileformat is None:
            if (suffix := Path(path).suffix) in SUFFIX_MAPPING:
                fileformat = SUFFIX_MAPPING[suffix]
            else:
                fileformat = "json" if self.fileformat is None else self.fileformat
        encoding = self.encoding if encoding is None else encoding
        if fileformat in FORMAT_MAPPING:
            super().save(path, FORMAT_MAPPING[fileformat], encoding=encoding)
        else:
            raise FileFormatError(f"unsupported config file format: {fileformat!r}")

    def to_object(self) -> "UnwrappedDataObj":
        """Returns the unwrapped config data."""
        return self.__obj

    def to_dict(self) -> dict["BasicObj", "UnwrappedDataObj"]:
        """Returns the unwrapped config data if it's a mapping."""
        raise TypeError(f"{self.__desc()} can't be converted into a dict")

    def to_list(self) -> list["UnwrappedDataObj"]:
        """Returns the unwrapped config data if it's a list."""
        raise TypeError(f"{self.__desc()} can't be converted into a list")

    def to_html(self) -> HTMLTreeMaker:
        """Return an HTMLTreeMaker object for representing self."""
        return HTMLTreeMaker(repr(self.__obj).replace(">", "&gt").replace("<", "&lt"))

    def type(self) -> type["DataObj"]:
        """Return the type of the unwrapped data"""
        return self.__obj.__class__

    def set_path(self, path: str | Path) -> None:
        """Set the path."""
        if not self.overwrite_ok:
            raise TypeError(
                "set_path() is not allowed when the instance is locked, "
                "please run self.unlock() first"
            )
        self.path = path

    def lock(self) -> None:
        """Lock the original path so that it can not be overwritten."""
        self.overwrite_ok = False

    def unlock(self) -> None:
        """Unlock the original path so that it can be overwritten."""
        self.overwrite_ok = True

    def get_max_line_width(self) -> int:
        """Get the module variable `MAX_LINE_WIDTH`."""
        return getattr(sys.modules[__name__.rpartition(".")[0]], "MAX_LINE_WIDTH")

    def __desc(self) -> str:
        return f"config object of type {self.type().__name__}"


class _DictConfigIOWrapper(ConfigIOWrapper):
    constructor = ConfigIOWrapper
    sub_constructors = {}

    def __init__(self, obj: "DataObj", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: dict["BasicObj", "DataObj"] = {}
        for k, v in obj.items():
            if not isinstance(k, self.valid_types):
                raise TypeError(f"invalid key type: {k.__class__.__name__}")
            if isinstance(v, self.constructor):
                new_obj[k] = v
            else:
                new_obj[k] = self.constructor(
                    v, self.fileformat, encoding=self.encoding
                )
        self.__obj = new_obj

    def __getitem__(self, __key: "BasicObj") -> Self:
        return self.__obj[__key]

    def __setitem__(self, __key: "BasicObj", __value: "DataObj") -> None:
        if isinstance(__value, self.constructor):
            self.__obj[__key] = __value
        else:
            self.__obj[__key] = self.constructor(
                __value, self.fileformat, encoding=self.encoding
            )

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "{\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for k, v in self.__obj.items():
            _head = lines[-1] if lines else ""
            _key = f"{k!r}: "
            _flat = repr(v.to_object())
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

    def to_object(self) -> "UnwrappedDataObj":
        return {k: v.to_object() for k, v in self.__obj.items()}

    def to_dict(self) -> dict["BasicObj", "UnwrappedDataObj"]:
        return self.to_object()

    def to_html(self) -> HTMLTreeMaker:
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
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


class _ListConfigIOWrapper(ConfigIOWrapper):
    constructor = ConfigIOWrapper
    sub_constructors = {}

    def __init__(self, obj: "DataObj", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: list["DataObj"] = []
        for x in obj:
            if isinstance(x, self.constructor):
                new_obj.append(x)
            else:
                new_obj.append(
                    self.constructor(x, self.fileformat, encoding=self.encoding)
                )
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
            _flat = repr(x.to_object())
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
            self.__obj.append(
                self.constructor(__object, self.fileformat, encoding=self.encoding)
            )

    def extend(self, __iterable: Iterable["DataObj"]) -> None:
        if isinstance(__iterable, self.__class__):
            self.__obj.extend(list(__iterable))
        else:
            self.__obj.extend(
                list(
                    self.constructor(
                        list(__iterable), self.fileformat, encoding=self.encoding
                    )
                )
            )

    def to_object(self) -> "UnwrappedDataObj":
        return [x.to_object() for x in self.__obj]

    def to_list(self) -> list["UnwrappedDataObj"]:
        return self.to_object()

    def to_html(self) -> HTMLTreeMaker:
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
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


class ConfigTemplate(ConfigIOWrapper):
    """A template for matching config objects."""

    valid_types = (str, int, float, bool, NoneType, type, Callable)
    constructor = object
    sub_constructors = {
        dict: lambda: _DictConfigTemplate,
        list: lambda: _ListConfigTemplate,
    }
    is_template = True


class _DictConfigTemplate(ConfigTemplate):
    constructor = ConfigTemplate
    sub_constructors = {}


class _ListConfigTemplate(ConfigTemplate):
    constructor = ConfigTemplate
    sub_constructors = {}


class FileFormatError(Exception):
    """Raised if the file format is not supported."""
