# Design: `@tailrec`

Status: implemented on branch `sum-types`. The optional build-time loop rewrite is not implemented.
Authority: the owner's proposal ("closed unions, open sums, `@tailrec`, and a rename", work item 3) and `SPEC-sol6.1-composite.md`. There is no hidden tail-call transform: users opt in per function.

## Spelling

```python
from pyalamode import tailrec

@tailrec
def countdown_total(value: int, total: int = 0) -> int:
    if value <= 0:
        return total
    return countdown_total(value - 1, total + value)
```

`@tailrec` selects the function for checking exactly like `@fun`, including the `import pyalamode` / `@pyalamode.tailrec` spelling, and composes with `@effects(...)` in either order. Unlike `@fun`, it is a wrapper, in the same sense that `@record` transforms its class.

## Runtime

`pyalamode.tailrec` replaces the function with a driver:

1. A call from any frame other than the function's own body runs the body. While the body returns the private `_TailCall` continuation, the driver calls the body again with the continuation's arguments. Otherwise it returns the result.
2. A call made directly by the body frame (`sys._getframe(1).f_code is body`) is a tail call. It returns the continuation instead of recursing.

Each iteration is a fresh body frame, so stack depth is constant and a failure's traceback ends in the user's body. A 100,000-deep call completes under the default recursion limit of 1,000.

The proposal suggested a per-thread "driver active" flag. That would hand a continuation to any re-entrant caller while the driver runs, for example a callback that calls the function again. The caller-frame test is exact: a call from any other frame, including a callback, is an ordinary full call. It needs no thread state.

Driver metadata copies `__module__`, `__name__`, `__qualname__`, `__doc__` and `__annotations__`. `__wrapped__` is the body. Calling `__wrapped__` directly is unchecked misuse: its self calls return continuations.

## Static rules (PAL122)

- Every use of the function's own name in its body is the callee of a call in tail position: the direct value of `return`, through `if`/`elif`/`else`, `match` arms and conditional expressions. It is never inside `try` or `with` (including `borrow`), never an operand of an operation, never assigned, aliased or passed as a callback.
- Each tail call passes a complete positional argument list matching the signature, defaults permitted. Keyword-only, `*args` and `**kwargs` parameters are refused, and so are keyword or starred arguments in tail calls.
- The name must not be shadowed by a parameter or local binding.
- Nested functions or lambdas in the body may not reference any parameter. This conservatively covers the escaping-closure rule and keeps a future loop rewrite behavior-identical.
- Mutual recursion is refused: a `@tailrec` function may not reach itself through any other function.
- A module that rebinds `sys._getframe` invalidates the marker (PAL120), because the driver depends on it.

The remediation names the accumulator pattern: carry pending work in a parameter and `return name(...)` directly.

## Failures, contracts and guards

- A proven self tail call contributes no `RecursionError`, to the function or its callers. Other calls in the body keep their own failure bounds.
- `FunctionContract.tail_recursive` records the claim. It appears in cache entries and in wheel evidence for exported functions.
- Exports and debug guards: generated facades read defaults from the body through `__wrapped__`. Debug mode skips the return assertion on returns that contain a tail call, since those return the continuation; plain returns and parameters are still asserted.

## Not implemented

- The optional build-time loop rewrite (`while True:` with simultaneous parameter rebinding) under a policy key. The trampoline already gives identical behavior in plain Python and built artifacts. The rewrite would be a performance option recorded in build evidence.
- Mutual tail recursion.
