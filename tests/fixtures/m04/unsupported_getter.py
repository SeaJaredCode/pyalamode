from pyalamode import record


@record
class Changing:
    value: int

    @property
    def current(self):
        return input()
