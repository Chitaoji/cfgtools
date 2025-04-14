"""Contains examples."""

import lazyr

VERBOSE = 3

lazyr.register("faker", verbose=VERBOSE)

# pylint: disable=wrong-import-position
from . import test_case

__all__ = ["test_case"]
