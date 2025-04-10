"""
Contains methods for reading config files: read_yaml(), read_pickle(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
import pickle
from pathlib import Path

import chardet
import yaml

from .iowrapper import ConfigIOWrapper

__all__ = ["detect_encoding", "read_yaml", "read_pickle", "read_json"]


def detect_encoding(path: str | Path) -> str:
    """
    Detect the encoding of a file.

    Parameters
    ----------
    path : str | Path
        File path.

    Returns
    -------
    str
        The name of the encoding used to encode the file.

    """
    with open(path, "rb") as f:
        test_line = f.readline()
    return chardet.detect(test_line)["encoding"]


def read_yaml(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read a yaml file.

    Parameters
    ----------
    path : str | Path
        Path of the yaml file.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    encoding = detect_encoding(path) if encoding is None else encoding
    with open(path, "r", encoding=encoding) as f:
        cfg = yaml.safe_load(f)
        cfg = {} if cfg is None else cfg
    return ConfigIOWrapper(cfg, "yaml", path=path, encoding=encoding)


def _try_read_yaml(
    path: str | Path, encoding: str | None = None
) -> ConfigIOWrapper | None:
    try:
        return read_yaml(path, encoding=encoding)
    except yaml.reader.ReaderError:
        return None


def read_pickle(path: str | Path) -> ConfigIOWrapper:
    """
    Read a pickle file.

    Parameters
    ----------
    path : str | Path
        Path of the pickle file.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    with open(path, "rb") as f:
        cfg = pickle.load(f)
        cfg = {} if cfg is None else cfg
    return ConfigIOWrapper(cfg, "pickle", path=path)


def _try_read_pickle(path: str | Path, **_) -> ConfigIOWrapper | None:
    try:
        return read_pickle(path)
    except pickle.UnpicklingError:
        return None


def read_json(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read a json file.

    Parameters
    ----------
    path : str | Path
        Path of the json file.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    encoding = detect_encoding(path) if encoding is None else encoding
    with open(path, "r", encoding=encoding) as f:
        cfg = json.load(f)
        cfg = {} if cfg is None else cfg
    return ConfigIOWrapper(cfg, "json", path=path, encoding=encoding)


def _try_read_json(
    path: str | Path, encoding: str | None = None
) -> ConfigIOWrapper | None:
    try:
        return read_json(path, encoding=encoding)
    except json.JSONDecodeError:
        return None


READING_METHOD_MAPPING = {
    "json": _try_read_json,
    "yaml": _try_read_yaml,
    "pickle": _try_read_pickle,
}
