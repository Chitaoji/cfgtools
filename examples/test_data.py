"""Contains constructors for test data: contact_book(), etc."""

from typing import TYPE_CHECKING

from ..src import config

if TYPE_CHECKING:
    from ..src._typing import ConfigIOWrapper


__all__ = ["contact_book"]


def contact_book() -> "ConfigIOWrapper":
    """Returns a fake contact book."""
    return config(None)
