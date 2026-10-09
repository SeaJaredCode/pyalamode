from pyalamode import Err, Ok, Some, Vector
from examples.domains.domain import User, Lookup, display, optional_name, quotient, validated_pair

print(display(Lookup.Found(User("Ada", Vector.of("reader")))))
print(optional_name(Some("Ada")))
print(quotient(12, 3))
print(quotient(12, 0))
print(validated_pair(Err("number is required"), Err("label is required")))
print(validated_pair(Ok(12), Ok("Ada")))
