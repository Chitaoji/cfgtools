"""Contains examples."""

import lazyr

VERBOSE = 0

lazyr.register("faker.Faker", verbose=VERBOSE)

# pylint: disable=wrong-import-position
from . import test_case

__all__ = ["test_case"]
