"""
Contains typing classes.

NOTE: this module is not intended to be directly imported.

"""

import logging
from typing import Literal

from .iowrapper import ConfigIOWrapper

logging.getLogger(__name__).warning(
    "importing from '%s' - this module is not intended to be directly imported, "
    "therefore unexpected errors may occur",
    __name__,
)

DataObject = bool | int | float | str | bytes | None
ConfigObject = (
    dict[DataObject, "ConfigObject"]
    | list["ConfigObject"]
    | DataObject
    | ConfigIOWrapper
)
ConfigFileFormat = Literal[
    "yaml", "yml", "pickle", "pkl", "json", "ini", "text", "txt", "bytes"
]
ObjectTypeStr = Literal[
    "dict", "list", "bool", "int", "float", "str", "bytes", "NoneType"
]
