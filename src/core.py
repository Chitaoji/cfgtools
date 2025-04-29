"""
Contains the core of cfgtools: autoread(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING

from .iowrapper import FORMAT_MAPPING, ConfigIOWrapper, FileFormatError
from .reader import READER_MAPPING, TRY_READER_MAPPING, detect_encoding

if TYPE_CHECKING:
    from ._typing import ConfigFileFormat, ConfigObject

__all__ = ["read_config", "config"]


def read_config(
    path: str | Path,
    fileformat: "ConfigFileFormat | None" = None,
    /,
    encoding: str | None = None,
) -> ConfigIOWrapper:
    """
    Read a config file. The format of the file is automatically
    detected.

    Parameters
    ----------
    path : str | Path
        File path.
    fileformat : ConfigFileFormat | None, optional
        File format, by default None. If not specified, the file
        format will be automatically detected.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file
        (if needed), by default None. If not specified, the encoding
        will be automatically detected.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    encoding = detect_encoding(path) if encoding is None else encoding
    if fileformat is not None:
        if fileformat not in FORMAT_MAPPING:
            raise FileFormatError(f"unsupported config file format: {fileformat!r}")
        return READER_MAPPING[FORMAT_MAPPING[fileformat]](path, encoding=encoding)
    else:
        for m in TRY_READER_MAPPING.values():
            if (wrapper := m(path, encoding=encoding)) is not None:
                return wrapper
    raise FileFormatError(f"failed to read the config file: '{path}'")


def config(obj: "ConfigObject" = None, /) -> ConfigIOWrapper:
    """
    Initialize a new config object.

    Parameters
    ----------
    obj : ConfigObject, optional
        Config object, by default None.

    Returns
    -------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    return ConfigIOWrapper(obj, "json")
