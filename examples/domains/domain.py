# mode: fun
from pyalamode import variant, case, record, Vector, Option, Some, Nothing
from pyalamode import Result, Ok, Err, accumulate, Failure, failure_value

@record
class User:
    name: str
    tags: Vector[str]

@variant
class Lookup:
    @case
    class Found:
        user: User
    @case
    class Missing:
        pass

def display(value: Lookup) -> str:
    match value:
        case Lookup.Found(user=User(name=name)):
            return name
        case Lookup.Missing():
            return "missing"

def optional_name(value: Option[str]) -> str:
    match value:
        case Some(value=name):
            return name
        case Nothing():
            return "anonymous"

def quotient(number: int, divisor: int) -> Result[int, Failure]:
    try:
        return Ok(number // divisor)
    except ZeroDivisionError as caught:
        return Err(failure_value(caught))

def validated_pair(number: Result[int, str], label: Result[str, str]) -> Result[tuple[int, str], Vector[str]]:
    return accumulate(number, label)
