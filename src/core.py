"""
Contains the core of cfgtools: autoread(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path

from .iowrapper import SUFFIX_MAPPING, ConfigIOWrapper, FileFormatError
from .reading import READING_METHOD_MAPPING

__all__ = ["autoread"]


def autoread(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Open a config file. The format of the file is automatically
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
