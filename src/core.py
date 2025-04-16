"""
Contains the core of cfgtools: autoread(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING

from .iowrapper import SUFFIX_MAPPING, ConfigIOWrapper, FileFormatError
from .reading import READING_METHOD_MAPPING, detect_encoding

if TYPE_CHECKING:
    from ._typing import ConfigObject

__all__ = ["read_config", "config"]


def read_config(path: str | Path, /, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read a config file. The format of the file is automatically
    detected.

    Parameters
    ----------
    path : str | Path
        File path.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file
        (if needed), by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    encoding = detect_encoding(path) if encoding is None else encoding
    if (suffix := Path(path).suffix) in SUFFIX_MAPPING:
        default_method = SUFFIX_MAPPING[suffix]
        wrapper = READING_METHOD_MAPPING[default_method](path, encoding=encoding)
        if wrapper is not None:
            return wrapper
        for k, m in READING_METHOD_MAPPING.items():
            if k != default_method:
                if (wrapper := m(path, encoding=encoding)) is not None:
                    return wrapper
    else:
        for m in READING_METHOD_MAPPING.values():
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
