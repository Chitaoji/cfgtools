"""
Contains typing classes.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import logging
from typing import Literal

from .iowrapper import ConfigIOWrapper

logging.warning(
    "importing from '._typing' - this module is not intended for direct import, "
    "therefore unexpected errors may occur"
)

DataObject = bool | int | float | str | None
ConfigObject = (
    dict[DataObject, "ConfigObject"]
    | list["ConfigObject"]
    | DataObject
    | ConfigIOWrapper
)
ConfigFileFormat = Literal["json", "yaml", "yml", "pickle", "pkl"]
