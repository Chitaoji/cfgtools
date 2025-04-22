"""
Contains methods for saving config files: _to_yaml(), _to_pickle(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
import pickle
import sys
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
    Path(path).write_text(json.dumps(obj.to_object()), encoding=encoding)


def _to_bytes(
    obj: "ConfigIOWrapper", path: str | Path | None, encoding: str | None = None
) -> None:
    if encoding is None:
        encoding = sys.getdefaultencoding()
    Path(path).write_bytes(bytes(json.dumps(obj.to_object()), encoding=encoding))


SAVING_METHOD_MAPPING: dict[str, Callable[..., None]] = {
    "pickle": _to_pickle,
    "ini": _to_ini,
    "json": _to_json,
    "yaml": _to_yaml,
    "text": _to_text,
    "bytes": _to_bytes,
}
