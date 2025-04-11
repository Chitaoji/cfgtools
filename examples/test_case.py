"""Contains constructors for test data: contact_book(), etc."""

from typing import TYPE_CHECKING

from faker import Faker

from ..src import config

if TYPE_CHECKING:
    from ..src._typing import ConfigIOWrapper


__all__ = ["customer_data"]


def customer_data(
    number_of_customers: int = 20, seed: int | None = None
) -> "ConfigIOWrapper":
    """
    Returns a fake book of customers, including names, emails, phone
    numbers, addresses, and order records of the customers.

    Parameters
    ----------
    number_of_customers : int, optional
        Number of customers, by default 20.
    seed : int | None, optional
        Seed value, by default None.

    Returns
    -------
    ConfigIOWrapper
        Config object.

    """
    faker = Faker()
    faker.seed_instance(seed)
    book = {}
    for _ in range(number_of_customers):
        name = faker.name()
        book[name] = {
            "name": name,
            "email": faker.email(),
            "phone_number": faker.phone_number(),
            "address": [faker.city()] + faker.address().splitlines(),
            "order_records": [
                {
                    "order_id": faker.uuid4(),
                    "product_id": faker.md5(),
                    "quantity": faker.pyint(1, 1000),
                    "unit_price": faker.pyfloat(3, 2, True),
                    "date": str(faker.date_this_decade()),
                }
                for __ in range(faker.pyint(min_value=1, max_value=10))
            ],
        }
    return config(book)
