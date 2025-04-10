"""Contains constructors for test data: contact_book(), etc."""

from typing import TYPE_CHECKING

from faker import Faker

from ..src import config

if TYPE_CHECKING:
    from ..src._typing import ConfigIOWrapper


__all__ = ["contact_book"]


def contact_book(number_of_people: int = 20) -> "ConfigIOWrapper":
    """
    Returns a fake contact book.

    Parameters
    ----------
    number_of_people : int, optional
        Number of people on the contact book, by default 20.

    Returns
    -------
    ConfigIOWrapper
        Config object.

    """
    faker = Faker()
    book = {}
    for _ in range(number_of_people):
        name = faker.name()
        book[name] = {
            "name": name,
            "email": faker.email(),
            "phone_number": faker.phone_number(),
            "address": [faker.city()] + faker.address().splitlines(),
            "mac_addresses": {
                faker.port_number(): faker.mac_address()
                for __ in range(faker.pyint(min_value=1, max_value=10))
            },
        }
    return config(book)
