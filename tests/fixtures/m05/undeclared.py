from pyalamode import fun, ClockCapability

@fun
def quote(clock: ClockCapability) -> int:
    return clock.now_ns()
