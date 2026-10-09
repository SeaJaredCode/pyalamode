"""Typed customer calculations with persistent record updates."""
# mode: fun
from pyalamode import Vector, record, replace


@record
class Customer:
    name: str
    tags: Vector[str]


def tag_customer(customer: Customer, tag: str) -> Customer:
    tags = customer.tags.appended(tag)
    return replace(customer, tags=tags)


def tag_count(customer: Customer) -> int:
    return len(customer.tags)
