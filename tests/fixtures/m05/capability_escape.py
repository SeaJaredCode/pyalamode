from pyalamode import effects, Clock, ClockCapability

@effects(Clock)
def quote(clock: ClockCapability) -> int:
    retained = (clock,)
    return 1
