"""Ordinary provider setup; recorded interfaces keep their declared effects."""
from pyalamode import recorded_clock, recorded_io, recorded_random, recorded_environment, state
from .core import archive, caption, draw, elapsed, sample

clock = recorded_clock((1_000_000, 1_000_100))
counter = state(0)
random = recorded_random((3,))
environment = recorded_environment((("NAME", "demo"),))
io = recorded_io((), allowed_ops=("read_text", "write_text"))
first = sample(clock, counter)
second = sample(clock, counter)
title = caption(environment)
archive(io, title)
print(first, second, elapsed(second[0], first[0]), draw(random, 10), io.read_text("sample.txt"))
