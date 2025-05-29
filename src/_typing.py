"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Literal

import loggerlib

from .iowrapper import ConfigIOWrapper

loggerlib.warning("this module is not intended to be imported at runtime")

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
