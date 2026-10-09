# mode: fun
from pyalamode import (effects, Effectful, Clock, State, IO, Random, Environment,
                      ClockCapability, StateCapability, IOCapability,
                      RandomCapability, EnvironmentCapability, borrow)


def elapsed(now_ns: int, baseline_ns: int) -> int:
    return now_ns - baseline_ns


@effects(Clock)
def read_clock(clock: ClockCapability) -> int:
    return clock.now_ns()


@effects(Clock)
def invoke(reader: Effectful[[ClockCapability], int, Clock], clock: ClockCapability) -> int:
    return reader(clock)


@effects(Clock, State)
def sample(clock: ClockCapability, counter: StateCapability) -> tuple[int, int]:
    with borrow(clock) as scoped:
        stamp = invoke(read_clock, scoped)
    count = counter.get()
    counter.set(count + 1)
    return (stamp, count)


@effects(IO)
def archive(io: IOCapability, title: str) -> None:
    io.write_text("sample.txt", title)


@effects(Random)
def draw(random: RandomCapability, bound: int) -> int:
    return random.below(bound)


@effects(Environment)
def caption(environment: EnvironmentCapability) -> str:
    return "run " + environment.get("NAME", "test")
