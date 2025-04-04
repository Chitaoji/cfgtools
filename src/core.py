"""
Contains the core of cfgtools: autoread(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path

import yaml

from .iowrapper import ConfigIOWrapper

__all__ = ["autoread", "read_yaml"]


def autoread(path: Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Open a config file. The format of the file is automatically
    detected.

    Parameters
    ----------
    path : Path
        Yaml file path.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    return read_yaml(path, encoding=encoding)


def read_yaml(path: Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read a yaml file.

    Parameters
    ----------
    path : Path
        Yaml file path.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    with open(path, "r", encoding=encoding) as f:
        cfg = yaml.safe_load(f)
        cfg = {} if cfg is None else cfg
    return ConfigIOWrapper(cfg, path=path, encoding=encoding)
