from pyalamode import effects, IO, State, Clock, Random, Environment

@effects(IO, State, Clock, Random, Environment)
def integration() -> int:
    return print("effect declarations cannot characterize this operation")
