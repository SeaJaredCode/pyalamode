"""Ordinary transport/unsafe shell; running it establishes no checked claim."""
from pyalamode import unsafe, freeze, Vector, fun
from .core import encode, content_key, recover, attachment_keys


@unsafe(scope="legacy invoice extraction", rationale="ordinary mutable integration output")
def legacy_amounts():
    return [10, 20, 30]


@fun
def add(total: int, amount: int) -> int:
    return total + amount


@fun
def total(amounts: Vector[int]) -> int:
    return amounts.fold(add, 0)


if __name__ == "__main__":
    transport = encode(b"bounded attachment")
    digest = content_key(b"bounded attachment")
    print("transport", transport)
    print("digest", digest.hex())
    print("recovered", recover(transport))
    print("noncanonical", recover(b"Zh=="))
    print("keys", attachment_keys(Vector.of(transport)))
    raw = legacy_amounts()
    stable = freeze(raw, exclusive=True, schema=Vector[int])
    raw[0] = 999
    print("snapshot total", total(stable))
