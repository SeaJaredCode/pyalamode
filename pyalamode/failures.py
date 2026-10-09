"""Immutable conversion of a closed set of actual native exception identities.

No exception payload, dictionary, traceback, getter or formatting is observed.
Ordinary except targets remain real exceptions; the checker controls token scope.
"""

from .records import record as _record

__all__ = ["Failure", "failure_value"]


@_record
class Failure:
    __module__ = "pyalamode"
    category: str
    message: str


_NATIVE_FAILURES = (
    (ZeroDivisionError, "ZeroDivisionError", "division by zero"),
    (IndexError, "IndexError", "index out of range"),
    (KeyError, "KeyError", "key not found"),
    (ValueError, "ValueError", "invalid value"),
    (RecursionError, "RecursionError", "recursion limit reached"),
    (RuntimeError, "RuntimeError", "runtime operation failed"),
    (OSError, "OSError", "operating system operation failed"),
    (UnicodeError, "UnicodeError", "unicode operation failed"),
    (UnicodeDecodeError, "UnicodeError", "unicode operation failed"),
    (UnicodeEncodeError, "UnicodeError", "unicode operation failed"),
    (UnicodeTranslateError, "UnicodeError", "unicode operation failed"),
    (BlockingIOError, "OSError", "operating system operation failed"),
    (ChildProcessError, "OSError", "operating system operation failed"),
    (ConnectionError, "OSError", "operating system operation failed"),
    (BrokenPipeError, "OSError", "operating system operation failed"),
    (ConnectionAbortedError, "OSError", "operating system operation failed"),
    (ConnectionRefusedError, "OSError", "operating system operation failed"),
    (ConnectionResetError, "OSError", "operating system operation failed"),
    (FileExistsError, "OSError", "operating system operation failed"),
    (FileNotFoundError, "OSError", "operating system operation failed"),
    (InterruptedError, "OSError", "operating system operation failed"),
    (IsADirectoryError, "OSError", "operating system operation failed"),
    (NotADirectoryError, "OSError", "operating system operation failed"),
    (PermissionError, "OSError", "operating system operation failed"),
    (ProcessLookupError, "OSError", "operating system operation failed"),
    (TimeoutError, "OSError", "operating system operation failed"),
)


def failure_value(exception):
    """Copy an exact characterized builtin category into a fresh stable record."""
    kind = type(exception)
    for native, category, message in _NATIVE_FAILURES:
        if kind is native:
            return Failure(category, message)
    raise TypeError("failure_value requires an exact characterized builtin exception")
