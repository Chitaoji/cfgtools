"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Literal

import loggings

from .iowrapper import ConfigIOWrapper

loggings.warning("this module is not intended to be imported at runtime")

DataObj = bool | int | float | str | bytes | None
UnwrappedConfigObj = (
    dict[DataObj, "UnwrappedConfigObj"] | list["UnwrappedConfigObj"] | DataObj
)
ConfigObj = dict[DataObj, "ConfigObj"] | list["ConfigObj"] | DataObj | ConfigIOWrapper
ConfigTypeObj = (
    dict[DataObj, "ConfigTypeObj"] | list["ConfigTypeObj"] | DataObj | ConfigIOWrapper
)
ConfigFileFormat = Literal[
    "yaml", "yml", "pickle", "pkl", "json", "ini", "text", "txt", "bytes"
]
UnwrappedConfigTypeStr = Literal[
    "dict", "list", "bool", "int", "float", "str", "bytes", "NoneType"
]
