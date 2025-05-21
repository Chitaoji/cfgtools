"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Self

from .css import TREE_CSS_STYLE
from .saver import ConfigSaver
from .utils.htmltree import HTMLTreeMaker

if TYPE_CHECKING:
    from ._typing import ConfigFileFormat, ConfigObject, DataObject, ObjectTypeStr

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
    obj : ConfigObject
        Config object.
    fileformat : ConfigFileFormat
        File format.
    path : str | Path | None, optional
        File path, by default None.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file
        (if needed), by default None.

    Raises
    ------
    TypeError
        Raised when the type of config object is invalid.

    """

    def __new__(cls, obj: "ConfigObject", *args, **kwargs) -> Self:
        if isinstance(obj, dict):
            new_class = _DictConfigIOWrapper
        elif isinstance(obj, list):
            new_class = _ListConfigIOWrapper
        elif obj is None or isinstance(obj, (bool, int, float, str, bytes)):
            new_class = ConfigIOWrapper
        else:
            raise TypeError(
                f"invalid type of config object: {obj.__class__.__name__!r}"
            )
        return super().__new__(new_class)

    def __init__(
        self,
        obj: "ConfigObject",
        fileformat: "ConfigFileFormat",
        /,
        path: str | Path | None = None,
        encoding: str | None = None,
    ) -> None:
        self.obj = obj
        self.fileformat = fileformat
        self.overwrite_ok = True
        if path is None:
            self.path = None
        else:
            path = Path(path)
            self.path = path.absolute().relative_to(path.cwd()).as_posix()
        self.encoding = encoding

    def __getitem__(self, __key: "DataObject") -> Self:
        raise TypeError(f"{self.__obj_desc()} is not subscriptable")

    def __setitem__(self, __key: "DataObject", __value: "ConfigObject") -> None:
        raise TypeError(f"{self.__obj_desc()} does not support item assignment")

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
        info = (
            f"format: {self.fileformat!r} | path: {self.path!r} "
            f"| encoding: {self.encoding!r}"
        )
        divide_line = "-" * len(info)
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
            reprs = flat
        else:
            reprs = self.repr()
        return f"{reprs}\n{divide_line}\n{info}\n{divide_line}"

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
        main_maker.add(info, "i")
        return {"text/html": main_maker.make("cfgtools-tree", TREE_CSS_STYLE)}

    def __str__(self) -> str:
        return f"config({self.obj!r})"

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
        return f"{self.obj!r}"

    def keys(self) -> "Iterable[DataObject]":
        """Provide a view of the config object's keys if it's a dict."""
        raise TypeError(f"{self.__obj_desc()} has no attribute 'keys'")

    def values(self) -> "Iterable[ConfigObject]":
        """Provide a view of the config object's values if it's a dict."""
        raise TypeError(f"{self.__obj_desc()} has no attribute 'values'")

    def items(self) -> "Iterable[tuple[DataObject, ConfigObject]]":
        """Provide a view of the config object's items if it's a dict."""
        raise TypeError(f"{self.__obj_desc()} has no attribute 'items'")

    def append(self, __object: "ConfigObject") -> None:
        """Append object to the end of the config object if it's a list."""
        raise TypeError(f"{self.__obj_desc()} has no attribute 'append'")

    def extend(self, __object: "Iterable[ConfigObject]") -> None:
        """Extend the config object if it's a list."""
        raise TypeError(f"{self.__obj_desc()} has no attribute 'extend'")

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
            Raised when both path and `self.path` are None.
        FileFormatError
            Raised when the config file format is not supported.

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
                fileformat = self.fileformat
        encoding = self.encoding if encoding is None else encoding
        if fileformat in FORMAT_MAPPING:
            super().save(path, FORMAT_MAPPING[fileformat], encoding=encoding)
        else:
            raise FileFormatError(f"unsupported config file format: {fileformat!r}")

    def to_object(self) -> "ConfigObject":
        """Returns the config object without any wrapper."""
        return self.obj

    def to_html(self) -> HTMLTreeMaker:
        """Return an HTMLTreeMaker object for representing self."""
        return HTMLTreeMaker(repr(self.obj))

    def type(self) -> "ObjectTypeStr":
        """Return the type of the config object."""
        return self.obj.__class__.__name__

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

    def __obj_desc(self) -> str:
        return f"the config object of type {self.type()!r}"


class _DictConfigIOWrapper(ConfigIOWrapper):
    def __init__(self, obj: "ConfigObject", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: dict["DataObject", "ConfigObject"] = {}
        for k, v in self.obj.items():
            if k is not None and not isinstance(k, (bool, int, float, str, bytes)):
                raise TypeError(f"invalid type of dict key: {k.__class__.__name__!r}")
            if isinstance(v, ConfigIOWrapper):
                new_obj[k] = v
            else:
                new_obj[k] = ConfigIOWrapper(v, self.fileformat, encoding=self.encoding)
        self.obj = new_obj

    def __getitem__(self, __key: "DataObject") -> Self:
        return self.obj[__key]

    def __setitem__(self, __key: "DataObject", __value: "ConfigObject") -> None:
        if isinstance(__value, ConfigIOWrapper):
            self.obj[__key] = __value
        else:
            self.obj[__key] = ConfigIOWrapper(
                __value, self.fileformat, encoding=self.encoding
            )

    def __str__(self) -> str:
        return (
            "config({" + ", ".join({f"{k!r}: {str(v)}" for k, v in self.items()}) + "})"
        )

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "{\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for k, v in self.obj.items():
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

    def keys(self) -> Iterable["DataObject"]:
        return self.obj.keys()

    def values(self) -> Iterable["ConfigObject"]:
        return self.obj.values()

    def items(self) -> Iterable[tuple["DataObject", "ConfigObject"]]:
        return self.obj.items()

    def to_object(self) -> "ConfigObject":
        return {k: v.to_object() for k, v in self.obj.items()}

    def to_html(self) -> HTMLTreeMaker:
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
            return HTMLTreeMaker(flat)
        maker = HTMLTreeMaker('{<span class="closed"> ... }</span>')
        for k, v in self.obj.items():
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
    def __init__(self, obj: "ConfigObject", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: list["ConfigObject"] = []
        for x in self.obj:
            if isinstance(x, ConfigIOWrapper):
                new_obj.append(x)
            else:
                new_obj.append(
                    ConfigIOWrapper(x, self.fileformat, encoding=self.encoding)
                )
        self.obj = new_obj

    def __str__(self) -> str:
        return "config([" + ", ".join([str(x) for x in self.obj]) + "])"

    def __getitem__(self, __key: int) -> Self:
        return self.obj[__key]

    def repr(self, level: int = 0, /) -> str:
        seps = _sep(level + 1)
        string = "[\n"
        lines: list[str] = []
        max_line_width = self.get_max_line_width()
        for x in self.obj:
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

    def append(self, __object: "ConfigObject") -> None:
        if isinstance(__object, ConfigIOWrapper):
            self.obj.append(__object)
        else:
            self.obj.append(
                ConfigIOWrapper(__object, self.fileformat, encoding=self.encoding)
            )

    def extend(self, __iterable: Iterable["ConfigObject"]) -> None:
        if isinstance(__iterable, _ListConfigIOWrapper):
            self.obj.extend(__iterable.obj)
        else:
            self.obj.extend(
                ConfigIOWrapper(
                    list(__iterable), self.fileformat, encoding=self.encoding
                ).obj
            )

    def to_object(self) -> "ConfigObject":
        return [x.to_object() for x in self.obj]

    def to_html(self) -> HTMLTreeMaker:
        if len(flat := repr(self.to_object())) <= self.get_max_line_width():
            return HTMLTreeMaker(flat)
        maker = HTMLTreeMaker('[<span class="closed"> ... ]</span>')
        for x in self.obj:
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


class FileFormatError(Exception):
    """Raised when the file format is not supported."""
