"""Bounded eager tasks with stable messages and input-ordered stable results.

Runtime checks exact representations and data; fixed callable contracts,
unchanged dependencies and stable captures remain checked source/caller
obligations. The native backend is pinned to CPython 3.13.1 standard GIL. No
application audit/trace/profile/monitoring hook may add unknown behavior.
"""

import _thread
from .effects import Task, _new, _exact, _live, _invalid, _capability_family, borrow
from . import collections as _collections

__all__ = ["live_tasks", "controlled_tasks", "task_map", "task_map_with"]


def live_tasks(workers, /, *, max_tasks=256):
    """Ordinary setup: exact workers1..4/max_tasks1..256, no worker starts."""
    _exact(workers, int, "workers")
    _exact(max_tasks, int, "max_tasks")
    if not 1 <= workers <= 4 or not 1 <= max_tasks <= 256:
        raise ValueError("tasks: workers require 1..4 and max_tasks require 1..256")
    return _new(Task, "live", (workers, max_tasks, None, None, _thread.get_ident()))


def controlled_tasks(order, /, *, cancel_after=None):
    """Ordinary setup: fixed exact permutation and successful-prefix cutoff."""
    _exact(order, tuple, "order")
    if len(order) > 256:
        raise ValueError("tasks: controlled order exceeds 256 messages")
    for position, value in enumerate(order):
        _exact(value, int, "order[" + str(position) + "]")
        if not 0 <= value < len(order) or value in order[:position]:
            raise ValueError("tasks: controlled order requires an exact input-index permutation")
    if cancel_after is not None:
        _exact(cancel_after, int, "cancel_after")
        if not 0 <= cancel_after <= len(order):
            raise ValueError("tasks: cancel_after is outside the controlled order")
    return _new(Task, "controlled", (1, len(order), order, cancel_after, _thread.get_ident()))


def _launch(callback, handle):
    # Preallocated handle is already tracked, including an interrupted launch.
    _thread.start_joinable_thread(callback, handle=handle, daemon=False)


def _join(handle):
    handle.join()


def _runner(callback, message, slot):
    def run():
        try:
            value = callback(message)
            _collections._validate(value, "result")
            slot[1] = value
            slot[0] = True
        except BaseException as error:
            slot[1] = error
    return run


def _join_handles(entries, primary, recover=True):
    """Initial-all then one retry, with a finite recovery for loop interruption."""
    try:
        for entry in entries:
            handle, attempts, done = entry
            if handle.ident and attempts == 0:
                entry[1] = 1
                try:
                    _join(handle)
                    entry[2] = True
                except BaseException as error:
                    if primary is None:
                        primary = error
        for entry in entries:
            handle, attempts, done = entry
            if handle.ident and attempts == 1 and not done:
                entry[1] = 2
                try:
                    _join(handle)
                    entry[2] = True
                except BaseException as error:
                    if primary is None:
                        primary = error
    except BaseException as error:
        if primary is None:
            primary = error
        if recover:
            return _join_handles(entries, primary, False)
        # A second loop-level interruption is the disclosed process boundary.
        # Attempts remain bounded, and unresolved handles revoke the provider.
    unresolved = any(entry[0].ident and not entry[2] for entry in entries)
    return primary, unresolved


def _parallel(provider, callback, items, results):
    workers = provider.data[0]
    for start in range(0, len(items), workers):
        handles = []
        slots = []
        primary = None
        try:
            for index in range(start, min(start + workers, len(items))):
                slot = [False, None]
                slots.append((index, slot))
                handle = _thread._ThreadHandle()
                handles.append([handle, 0, False])
                _launch(_runner(callback, items[index], slot), handle)
            primary, unresolved = _join_handles(handles, primary)
            if unresolved:
                object.__setattr__(provider, "index", 2)
            if primary is not None:
                raise primary
            # Slots are input-ordered, independently of callback completion.
            for index, slot in slots:
                if slot[0] is not True:
                    raise slot[1]
                results[index] = slot[1]
        except BaseException as error:
            if primary is None:
                primary = error
            # Cover the first coordinator interruption at Python loop/state
            # transitions as well as native launch/join calls. Revoke before
            # cleanup so a repeated interruption cannot restore an active token.
            object.__setattr__(provider, "index", 2)
            primary, unresolved = _join_handles(handles, primary)
            if not unresolved:
                object.__setattr__(provider, "index", 1)
            raise primary
        finally:
            # Drop coordinator references, without mutating a slot still owned
            # by a worker if repeated native interruption prevented its join.
            handles.clear()
            slots.clear()


def _serial(provider, callback, items, results, capability):
    order, cutoff = provider.data[2:4]
    if provider.mode == "live":
        order = range(len(items))
        cutoff = len(items)
    elif cutoff is None:
        cutoff = len(order)
    for position in range(cutoff):
        index = order[position]
        if capability is None:
            result = callback(items[index])
            _collections._validate(result, "result")
        else:
            with borrow(capability) as scoped:
                result = callback(scoped, items[index])
                _collections._validate(result, "result")
        results[index] = result
    if cutoff < len(items):
        raise RuntimeError("tasks: configured cancellation boundary reached")


def _map(tasks, capability, callback, messages, with_capability):
    provider = _live(tasks, Task)
    results = []
    try:
        object.__setattr__(provider, "index", 1)
        if with_capability:
            family = _capability_family(type(capability))
            if family is None or family == Task:
                _invalid("capability", "expected one exact pre-M13 effect capability")
            _live(capability, family)
        _collections._function(callback)
        if type(messages) is not _collections.Vector:
            _collections._invalid("messages", "expected exact Vector")
        _collections._validate(messages, "messages")
        items = _collections._storage(messages, "_items", "messages")
        workers, maximum, order, _, _ = provider.data
        if len(items) > maximum or order is not None and len(items) != len(order):
            raise ValueError("tasks: message count differs from provider bounds/order")
        if with_capability and provider.mode == "live" and workers != 1:
            raise ValueError("tasks: capability lending requires live workers=1")
        results = [None] * len(items)
        if provider.mode == "live" and workers > 1:
            _parallel(provider, callback, items, results)
        else:
            _serial(provider, callback, items, results, capability)
        result = _collections._new(_collections.Vector, "_items", tuple(results))
        _collections._validate(result, "result")
        return result
    finally:
        results.clear()
        if provider.index != 2:
            object.__setattr__(provider, "index", 0)


def task_map(tasks, callback, messages, /):
    """Map one fixed checked callback; publish only the complete ordered Vector."""
    return _map(tasks, None, callback, messages, False)


def task_map_with(tasks, capability, callback, messages, /):
    """Serial map with a fresh logical external-capability borrow per callback."""
    return _map(tasks, capability, callback, messages, True)
