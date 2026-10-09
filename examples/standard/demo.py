"""Ordinary Python integration, with independently reported provider setup."""
from pyalamode import Vector, recorded_io, recorded_clock, recorded_environment, borrow
from .core import (prices, running_totals, groups, adjusted, wire, unwire, show,
                   read_prices, timestamp, configuration)

print(prices("10,20,30"))
print(prices("10,bad,30"))
values = Vector.of(10, 20, 30)
print(show(running_totals(values)))
print(groups(Vector.of(3, 2, 5, 4)))
print(show(adjusted(values, 2)))
print(unwire(wire("Ada — café")))
files = recorded_io((("prices.txt", "10,20,30"),), allowed_ops=("read_text", "write_text"))
clock = recorded_clock((123456789,))
environment = recorded_environment((("CAMPAIGN", "autumn"),))
with borrow(files) as source:
    imported_prices = read_prices(source, "prices.txt")
observed_time = timestamp(clock)
observed_config = configuration(environment, "CAMPAIGN")
print(imported_prices)
print(observed_time)
print(observed_config)
