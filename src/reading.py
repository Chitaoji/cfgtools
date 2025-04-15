"""
Contains methods for reading config files: read_yaml(), read_pickle(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
import pickle
from configparser import ConfigParser, MissingSectionHeaderError
from pathlib import Path

import yaml

from .iowrapper import ConfigIOWrapper

__all__ = ["detect_encoding", "read_yaml", "read_pickle", "read_json", "read_ini"]


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
    return json.detect_encoding(test_line)


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
    return ConfigIOWrapper(cfg, "json", path=path, encoding=encoding)


def _try_read_json(
    path: str | Path, encoding: str | None = None
) -> ConfigIOWrapper | None:
    try:
        return read_json(path, encoding=encoding)
    except json.JSONDecodeError:
        return None


def read_ini(path: str | Path, encoding: str | None = None) -> ConfigIOWrapper:
    """
    Read an ini file.

    Parameters
    ----------
    path : str | Path
        Path of the ini file.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    Returns
    --------
    ConfigIOWrapper
        A wrapper for reading and writing config files.

    """
    encoding = detect_encoding(path) if encoding is None else encoding
    parser = ConfigParser()
    parser.read(path, encoding=encoding)
    return ConfigIOWrapper(
        {
            s: {o: parser.get(s, o) for o in parser.options(s)}
            for s in parser.sections()
        },
        "ini",
        path=path,
        encoding=encoding,
    )


def _try_read_ini(
    path: str | Path, encoding: str | None = None
) -> ConfigIOWrapper | None:
    try:
        return read_ini(path, encoding=encoding)
    except MissingSectionHeaderError:
        return None


READING_METHOD_MAPPING = {
    "pickle": _try_read_pickle,
    "json": _try_read_json,
    "ini": _try_read_ini,
    "yaml": _try_read_yaml,
}
