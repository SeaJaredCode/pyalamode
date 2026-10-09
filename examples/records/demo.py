"""Explicit ordinary snapshots and exports; shell behavior is unchecked."""

from dataclasses import dataclass
from pyalamode import dataclass_adapter, freeze, thaw
from .core import Customer, tag_count, tag_customer


@dataclass
class CustomerDTO:
    name: str
    tags: list[str]


source = CustomerDTO("Jared", ["new"])
adapter = dataclass_adapter(CustomerDTO, Customer)
snapshot = freeze(source, exclusive=True, adapter=adapter, schema=Customer)
source.tags.append("changed in shell")
revised = tag_customer(snapshot, "vip")
exported = thaw(revised)
exported["tags"].append("export only")

print(snapshot)
print(revised)
print(tag_count(revised))
print(exported)
