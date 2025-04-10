"""Imports from 'src' and 'examples'. This file will be exlcuded from the package."""

from . import examples, src
from .examples import *
from .src import *

__all__: list[str] = []
__all__.extend(src.__all__)
__all__.extend(examples.__all__)
