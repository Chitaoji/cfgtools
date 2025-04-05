"""
Contains methods for reading config files: read_yaml(), read_pickle(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import pickle
from pathlib import Path

import yaml

from .iowrapper import ConfigIOWrapper

__all__ = ["read_yaml", "read_pickle"]


def read_yaml(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read a yaml file.

    Parameters
    ----------
    path : str | Path
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
    return ConfigIOWrapper(cfg, "yaml", path=path, encoding=encoding)


def _try_read_yaml(
    path: str | Path, encoding: str | None = None
) -> ConfigIOWrapper | None:
    try:
        return read_yaml(path, encoding=encoding)
    except UnicodeDecodeError:
        return None


def read_pickle(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read a pickle file.

    Parameters
    ----------
    path : str | Path
        Yaml file path.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    with open(path, "rb", encoding=encoding) as f:
        cfg = pickle.load(f)
        cfg = {} if cfg is None else cfg
    return ConfigIOWrapper(cfg, "yaml", path=path, encoding=encoding)


def _try_read_pickle(
    path: str | Path, encoding: str | None = None
) -> ConfigIOWrapper | None:
    try:
        return read_pickle(path, encoding=encoding)
    except pickle.UnpicklingError:
        return None


READING_METHOD_MAPPING = {
    "yaml": _try_read_yaml,
    "yml": _try_read_yaml,
    "pickle": _try_read_pickle,
    "pkl": _try_read_pickle,
}
