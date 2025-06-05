"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Callable, Literal

import loggings

from .iowrapper import ConfigIOWrapper

loggings.warning("this module is not intended to be imported at runtime")

BasicObj = str | int | float | bool | None | type | Callable
UnwrappedDataObj = (
    dict[BasicObj, "UnwrappedDataObj"] | list["UnwrappedDataObj"] | BasicObj
)
DataObj = dict[BasicObj, "DataObj"] | list["DataObj"] | BasicObj | ConfigIOWrapper
ConfigFileFormat = Literal[
    "yaml", "yml", "pickle", "pkl", "json", "ini", "text", "txt", "bytes"
]
