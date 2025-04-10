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
    from ._typing import Config

__all__ = ["read_config", "new_config", "read", "new"]


def read_config(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
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
        cfg = READING_METHOD_MAPPING[default_method](path, encoding=encoding)
        if cfg is not None:
            return cfg
        for k, m in READING_METHOD_MAPPING.items():
            if k != default_method:
                if (cfg := m(path, encoding=encoding)) is not None:
                    return cfg
    else:
        for m in READING_METHOD_MAPPING.values():
            if (cfg := m(path, encoding=encoding)) is not None:
                return cfg
    raise FileFormatError(f"failed to read config file: '{path}'")


def new_config(obj: "Config") -> ConfigIOWrapper:
    """
    Initialize a new config object.

    Parameters
    ----------
    obj : Config
        Config object.

    Returns
    -------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    return ConfigIOWrapper(obj, "json")


read = read_config
new = new_config
