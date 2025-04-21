"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Self

from .saving import WRITING_METHOD_MAPPING

if TYPE_CHECKING:
    from ._typing import ConfigFileFormat, ConfigObject, DataObject, ObjectTypeStr

__all__ = ["FileFormatError"]

SUFFIX_MAPPING = {
    ".yaml": "yaml",
    ".yml": "yaml",
    ".pickle": "pickle",
    ".pkl": "pickle",
    ".json": "json",
    ".ini": "ini",
}
MAX_LINE_WIDTH = 88


class ConfigIOWrapper:
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
        elif obj is None or isinstance(obj, (bool, int, float, str)):
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
            raise TypeError(
                "failed to access method '.__enter__()' because the config "
                "object was not read from a file"
            )
        return self

    def __exit__(self, *args) -> None:
        self.save()

    def __repr__(self) -> str:
        header = (
            f"format: {self.fileformat!r} | path: {self.path!r} "
            f"| encoding: {self.encoding!r}"
        )
        divide_line = "-" * len(header)
        if len(flat := str(self.to_object())) <= MAX_LINE_WIDTH:
            reprs = flat
        else:
            reprs = self.repr()
        return f"{reprs}\n{divide_line}\n{header}\n{divide_line}"

    def _repr_mimebundle_(self, *_, **__) -> dict[str, str]:
        return {"text/html": self.to_html()}

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
                    "failed to save the config because no path is specified"
                )
            path = self.path
        if fileformat is None:
            if (suffix := Path(path).suffix) in SUFFIX_MAPPING:
                fileformat = SUFFIX_MAPPING[suffix]
            else:
                fileformat = self.fileformat
        encoding = self.encoding if encoding is None else encoding
        if fileformat in WRITING_METHOD_MAPPING:
            WRITING_METHOD_MAPPING[fileformat](self, path, encoding=encoding)
        else:
            raise FileFormatError(f"unsupported config file format: {fileformat!r}")

    def to_json(
        self, path: str | Path | None = None, /, encoding: str | None = None
    ) -> None:
        """Save the config in a json file. See `self.save()` for more details."""
        self.save(path, "json", encoding=encoding)

    def to_yaml(
        self, path: str | Path | None = None, /, encoding: str | None = None
    ) -> None:
        """Save the config in a yaml file. See `self.save()` for more details."""
        self.save(path, "yaml", encoding=encoding)

    def to_pickle(self, path: str | Path | None = None, /) -> None:
        """Save the config in a pickle file. See `self.save()` for more details."""
        self.save(path, "pickle")

    def to_ini(
        self, path: str | Path | None = None, /, encoding: str | None = None
    ) -> None:
        """Save the config in an ini file. See `self.save()` for more details."""
        self.save(path, "ini", encoding=encoding)

    def to_ini_dict(self) -> dict:
        """Reformat the config object with `.ini` format, and returns a dict."""
        obj = self.to_object()
        if isinstance(obj, dict):
            if all(isinstance(v, dict) for v in obj.values()):
                return {
                    k: {x: json.dumps(y) for x, y in v.items()} for k, v in obj.items()
                }
            return {"null": {k: json.dumps(v) for k, v in obj.items()}}
        return {"null": {"null": json.dumps(obj)}}

    def to_object(self) -> "ConfigObject":
        """Returns the config object without any wrapper."""
        return self.obj

    def to_html(self) -> str:
        """Return an HTML text for representing self."""
        return repr(self)

    def type(self) -> "ObjectTypeStr":
        """Return the type of the config object."""
        return self.obj.__class__.__name__

    def __obj_desc(self) -> str:
        return f"the config object of type {self.type()!r}"


def make_html_tree(obj: "ConfigObject") -> str:
    """
    Make an HTML tree.

    Parameters
    ----------
    tree : TextTree
        A python module / class / function / method.

    Returns
    -------
    str
        Html string.

    """
    tstyle = "<ul>"
    return f"{tstyle}\n{__get_li(obj)}\n</ul>"


def __get_li(tree: "TextTree", main: bool = True) -> str:
    triangle = ""
    if tree.is_dir() and tree.children:
        tchidren = "\n".join(__get_li(x) for x in tree.children)
        return (
            f'<li class="m"><details><summary>{triangle}{make_plain_text(tree.name)}'
            f'</summary>\n<ul class="m">\n{tchidren}\n</ul>\n</details></li>'
        )

    li_class = "m" if main else "s"
    ul_class = "m" if display_params.tree_style == "vertical" else "s"
    triangle = triangle if main else ""
    if tree.children:
        tchidren = "\n".join(
            __get_li(x, main=ul_class == "m")
            for x in tree.children
            if x.name != NULL and __is_public(x.name)
        )
        if tchidren:
            name = make_plain_text(tree.name) + (".py" if tree.is_file() else "")
            return (
                f'<li class="{li_class}"><details><summary>{triangle}{name}</summary>'
                f'\n<ul class="{ul_class}">\n{tchidren}\n</ul>\n</details></li>'
            )
    name = make_plain_text(tree.name) + (".py" if tree.is_file() else "")
    return f'<li class="{li_class}"><span>{name}</span></li>'


class _DictConfigIOWrapper(ConfigIOWrapper):
    def __init__(self, obj: "ConfigObject", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: dict["DataObject", "ConfigObject"] = {}
        for k, v in self.obj.items():
            if k is not None and not isinstance(k, (bool, int, float, str)):
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
        for k, v in self.obj.items():
            _head = lines[-1] if lines else ""
            _key = f"{k!r}: "
            _flat = repr(v.to_object())
            if lines and (len(_head) + len(_key) + len(_flat) + 2 <= MAX_LINE_WIDTH):
                lines[-1] += " " + _key + _flat + ","
            elif len(seps) + len(_key) + len(_flat) < MAX_LINE_WIDTH:
                lines.append(seps + _key + _flat + ",")
            else:
                _child = v.repr(level + 1)
                if lines and (
                    len(_head) + len(_key) + len(_child) + 2 <= MAX_LINE_WIDTH
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
        for x in self.obj:
            _head = lines[-1] if lines else ""
            _flat = repr(x.to_object())
            if lines and (len(_head) + len(_flat) + 2 <= MAX_LINE_WIDTH):
                lines[-1] += " " + _flat + ","
            elif len(_head) + len(_flat) < MAX_LINE_WIDTH:
                lines.append(seps + _flat + ",")
            else:
                _child = x.repr(level + 1)
                if lines and (len(_head) + len(_child) + 2 <= MAX_LINE_WIDTH):
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


def _sep(level: int) -> str:
    return "    " * level


class FileFormatError(Exception):
    """Raised when the file format is not supported."""
