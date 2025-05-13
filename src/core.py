"""
Contains the core of cfgtools: autoread(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING

from .iowrapper import ConfigIOWrapper
from .reader import ConfigReader

if TYPE_CHECKING:
    from ._typing import ConfigFileFormat, ConfigObject

__all__ = ["read", "config"]


def read(
    path: str | Path,
    fileformat: "ConfigFileFormat | None" = None,
    /,
    encoding: str | None = None,
    overwrite_ok: bool = True,
) -> ConfigIOWrapper:
    """
    Read a config file and return a wrapper object. The format of the
    file is automatically detected.

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
    overwrite_ok : bool, optional
        Specifies whether the original path can be overwritten by the
        wrapper, by default True.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    wrapper = ConfigReader.read(path, fileformat, encoding=encoding)
    if not overwrite_ok:
        wrapper.lock()
    return wrapper


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
