"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Literal

import loggings

from .iowrapper import ConfigIOWrapper

loggings.warning("this module is not intended to be imported at runtime")

DataObject = bool | int | float | str | bytes | None
UnwrappedConfigObject = (
    dict[DataObject, "UnwrappedConfigObject"]
    | list["UnwrappedConfigObject"]
    | DataObject
)
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
