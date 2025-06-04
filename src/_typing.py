"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Callable, Literal

import loggings

from .iowrapper import ConfigIOWrapper

loggings.warning("this module is not intended to be imported at runtime")

DataObj = str | int | float | bool | None
DataTpl = str | int | float | bool | None | type | Callable
UnwrappedConfigObj = (
    dict[DataObj, "UnwrappedConfigObj"] | list["UnwrappedConfigObj"] | DataObj
)
ConfigObj = dict[DataObj, "ConfigObj"] | list["ConfigObj"] | DataObj | ConfigIOWrapper
ConfigTpl = dict[DataTpl, "ConfigTpl"] | list["ConfigTpl"] | DataTpl | ConfigIOWrapper
ConfigFileFormat = Literal[
    "yaml", "yml", "pickle", "pkl", "json", "ini", "text", "txt", "bytes"
]
UnwrappedConfigTypeStr = Literal[
    "dict", "list", "bool", "int", "float", "str", "bytes", "NoneType"
]
