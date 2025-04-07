"""
Contains typing classes.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

import logging
from typing import Literal

logging.warning(
    "importing from '._typing' - this module is not intended for direct import, "
    "therefore unexpected errors may occur"
)

Data = int | float | str
Config = dict[Data, "Config"] | list["Config"] | Data
ConfigFileFormat = Literal["yaml", "yml", "pickle", "pkl"]
