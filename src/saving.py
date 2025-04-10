"""
Contains methods for saving config files: _to_yaml(), _to_pickle(), etc.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import json
import pickle
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from ._typing import Config

__all__ = []


def _to_yaml(
    obj: "Config", path: str | Path | None, encoding: str | None = None
) -> None:
    with open(path, "w", encoding=encoding) as f:
        yaml.safe_dump(obj, f, sort_keys=False)


def _to_pickle(
    obj: "Config", path: str | Path | None, encoding: str | None = None
) -> None:
    with open(path, "wb", encoding=encoding) as f:
        pickle.dump(obj, f)


def _to_json(
    obj: "Config", path: str | Path | None, encoding: str | None = None
) -> None:
    with open(path, "w", encoding=encoding) as f:
        json.dump(obj, f)


WRITING_METHOD_MAPPING = {
    "yaml": _to_yaml,
    "yml": _to_yaml,
    "pickle": _to_pickle,
    "pkl": _to_pickle,
    "json": _to_json,
}
