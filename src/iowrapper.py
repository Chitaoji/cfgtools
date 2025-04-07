"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Self

from .saving import WRITING_METHOD_MAPPING

if TYPE_CHECKING:
    from ._typing import Config, ConfigFileFormat, Data

__all__ = ["ConfigIOWrapper"]

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
    obj : Config
        Config object.
    fmt : ConfigFileFormat
        File format.
    path : str | Path | None, optional
        File path, by default None.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file
        (if needed), by default None.

    """

    def __init__(
        self,
        obj: "Config",
        fmt: "ConfigFileFormat",
        path: str | Path | None = None,
        encoding: str | None = None,
    ) -> None:
        self.obj = obj
        self.fmt = fmt
        self.path = path
        self.encoding = encoding

    def __getitem__(self, __key: "Data") -> "Config":
        if isinstance(self.obj, (list, dict)):
            return ConfigIOWrapper(self.obj[__key], self.fmt, encoding=self.encoding)
        raise TypeError(f"{self.__obj_desc()} is not subscriptable")

    def __setitem__(self, __key: "Data", __value: "Config"):
        if isinstance(self.obj, (list, dict)):
            self.obj[__key] = __value
        else:
            raise TypeError(f"{self.__obj_desc()} does not support item assignment")

    def __repr__(self) -> str:
        return repr(self.obj)

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

    def save(
        self,
        path: str | Path | None = None,
        __format: "ConfigFileFormat | None" = None,
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
        __format : ConfigFileFormat | None, optional
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
        if __format is None:
            if (suffix := Path(path).suffix) in SUFFIX_MAPPING:
                __format = SUFFIX_MAPPING[suffix]
            else:
                __format = self.fmt
        encoding = self.encoding if encoding is None else encoding
        if __format in WRITING_METHOD_MAPPING:
            WRITING_METHOD_MAPPING[__format](self.obj, path, encoding=encoding)
        else:
            raise FileFormatError(f"unsupported config file format: {__format!r}")

    def keys(self) -> "Iterable[Data]":
        """Provide a view of the config object's keys if it's a dict."""
        if isinstance(self.obj, dict):
            return self.obj.keys()
        raise TypeError(f"{self.__obj_desc()} is not a dict")

    def values(self) -> "Iterable[Config]":
        """Provide a view of the config object's values if it's a dict."""
        if isinstance(self.obj, dict):
            return self.obj.values()
        raise TypeError(f"{self.__obj_desc()} is not a dict")

    def items(self) -> "Iterable[tuple[Data, Config]]":
        """Provide a view of the config object's items if it's a dict."""
        if isinstance(self.obj, dict):
            return self.obj.items()
        raise TypeError(f"{self.__obj_desc()} is not a dict")

    def append(self, __object: "Config") -> None:
        """Append object to the end of the config object if it's a list."""
        if isinstance(self.obj, list):
            return self.obj.append(__object)
        raise TypeError(f"{self.__obj_desc()} is not a list")

    def extend(self, __object: "Iterable[Config]") -> None:
        """Extend the config object if it's a list."""
        if isinstance(self.obj, list):
            return self.obj.extend(__object)
        raise TypeError(f"{self.__obj_desc()} is not a list")

    def type(self) -> str:
        """Return the type of the config object."""
        return self.obj.__class__.__name__

    def __obj_desc(self) -> str:
        return f"the config object (of type {self.type()!r})"


class FileFormatError(Exception):
    """Raised when file format is not supported."""
