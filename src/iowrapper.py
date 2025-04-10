"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Self

from .saving import WRITING_METHOD_MAPPING

if TYPE_CHECKING:
    from ._typing import ConfigFileFormat, ConfigObject, DataObject

__all__ = []

SUFFIX_MAPPING = {
    ".yaml": "yaml",
    ".yml": "yaml",
    ".pickle": "pickle",
    ".pkl": "pickle",
    ".json": "json",
}


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
        if obj is None or isinstance(obj, dict):
            new_class = _DictConfigIOWrapper
        elif isinstance(obj, list):
            new_class = _ListConfigIOWrapper
        elif isinstance(obj, (bool, int, float, str)):
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
        self.obj = {} if obj is None else obj
        self.fileformat = fileformat
        self.path = path
        self.encoding = encoding

    def __getitem__(self, __key: "DataObject") -> Self:
        raise TypeError(f"{self.__obj_desc()} is not subscriptable")

    def __setitem__(self, __key: "DataObject", __value: "ConfigObject") -> None:
        raise TypeError(f"{self.__obj_desc()} does not support item assignment")

    def __enter__(self) -> Self:
        if self.path is None:
            raise TypeError(
                "failed to access the method '.__enter__()' because this wrapper "
                "is a children node of the original wrapper - try on the original "
                "wrapper instead"
            )
        return self

    def __exit__(self, *args) -> None:
        self.save()

    def __repr__(self) -> str:
        return f"{self.obj!r}"

    def __str__(self) -> str:
        return f"config({self.obj!r})"

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
            WRITING_METHOD_MAPPING[fileformat](
                self.to_object(), path, encoding=encoding
            )
        else:
            raise FileFormatError(f"unsupported config file format: {fileformat!r}")

    def type(self) -> str:
        """Return the type of the config object."""
        return self.obj.__class__.__name__

    def to_object(self) -> "ConfigObject":
        """Returns the config object without any wrapper."""
        return self.obj

    def __obj_desc(self) -> str:
        return f"the config object of type {self.type()!r}"


class _DictConfigIOWrapper(ConfigIOWrapper):
    def __init__(self, obj: "ConfigObject", *args, **kwargs) -> None:
        super().__init__(obj, *args, **kwargs)
        new_obj: dict["DataObject", "ConfigObject"] = {}
        for k, v in self.obj.items():
            if not isinstance(k, (bool, int, float, str, type(None))):
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


class FileFormatError(Exception):
    """Raised when file format is not supported."""
