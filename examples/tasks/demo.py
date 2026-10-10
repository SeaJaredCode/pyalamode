"""Ordinary runtime demonstration; executing it supplies no source evidence."""
import json

from pyalamode import Vector, controlled_tasks, live_tasks, recorded_clock
from .core import prices, stamps


def main():
    values = Vector.of(10, 20, 30)
    quoted = prices(live_tasks(2), values, 2)
    stamped = stamps(controlled_tasks((2, 0, 1)), recorded_clock((300, 100, 200)), values)
    try:
        remaining = recorded_clock((300, 100, 200))
        stamps(controlled_tasks((2, 0, 1), cancel_after=2), remaining, Vector.of(10, 20, 30))
    except RuntimeError as error:
        cancelled = str(error)
    print(json.dumps({"prices": list(quoted), "stamps": list(stamped),
                      "cancelled": cancelled, "after_cancel_clock": remaining.now_ns()},
                     sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
