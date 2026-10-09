from pyalamode import Vector, fun, record, replace


@record
class Customer:
    tags: Vector[str]


@fun
def invalid(customer: Customer) -> Customer:
    return replace(customer, tags=["mutable"])
