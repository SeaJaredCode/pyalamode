from pyalamode import (Vector, Task, TaskCapability, Clock, ClockCapability,
                       effects, task_map, task_map_with)


@effects(Task)
def prices(tasks: TaskCapability, values: Vector[int], fee: int) -> Vector[int]:
    def quote(value: int) -> int:
        return value + fee
    return task_map(tasks, quote, values)


@effects(Task, Clock)
def stamps(tasks: TaskCapability, clock: ClockCapability,
           values: Vector[int]) -> Vector[tuple[int, int]]:
    @effects(Clock)
    def stamp(view: ClockCapability, value: int) -> tuple[int, int]:
        return (value, view.now_ns())
    return task_map_with(tasks, clock, stamp, values)
