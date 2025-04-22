"""
Contains methods for saving config files: _to_yaml(), _to_pickle(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
import pickle
from configparser import ConfigParser
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import yaml

if TYPE_CHECKING:
    from .iowrapper import ConfigIOWrapper

__all__ = []


def _to_yaml(
    obj: "ConfigIOWrapper", path: str | Path | None, encoding: str | None = None
) -> None:
    with open(path, "w", encoding=encoding) as f:
        yaml.safe_dump(obj.to_object(), f, sort_keys=False)


def _to_pickle(obj: "ConfigIOWrapper", path: str | Path | None, **_) -> None:
    with open(path, "wb") as f:
        pickle.dump(obj.to_object(), f)


def _to_json(
    obj: "ConfigIOWrapper", path: str | Path | None, encoding: str | None = None
) -> None:
    with open(path, "w", encoding=encoding) as f:
        json.dump(obj.to_object(), f)


def _to_ini(
    obj: "ConfigIOWrapper", path: str | Path | None, encoding: str | None = None
) -> None:
    parser = ConfigParser()
    parser.read_dict(obj.to_ini_dict())
    with open(path, "w", encoding=encoding) as f:
        parser.write(f)


def _to_text(
    obj: "ConfigIOWrapper", path: str | Path | None, encoding: str | None = None
) -> None:
    Path(path).write_text(repr(obj.to_object()), encoding=encoding)


def _to_bytes(obj: "ConfigIOWrapper", path: str | Path | None, **_) -> None:
    Path(path).write_bytes(repr(obj.to_object()))


WRITING_METHOD_MAPPING: dict[str, Callable[..., None]] = {
    "yaml": _to_yaml,
    "yml": _to_yaml,
    "pickle": _to_pickle,
    "pkl": _to_pickle,
    "json": _to_json,
    "ini": _to_ini,
    "text": _to_text,
    "txt": _to_text,
    "bytes": _to_bytes,
}
