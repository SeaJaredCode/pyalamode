"""Bounded ordinary runtime controls; callable/capture evidence is static work.

Test coordination and fault substitution are ordinary Python, explicitly outside
the checked task callback contract. Event timeouts bound tests, not scheduling.
"""

import _thread
import importlib
import json
import sys
import threading
import typing
import unittest
from types import GenericAlias
from unittest.mock import patch

from pyalamode import (
    Task, TaskCapability, effects, Effectful, Vector, Map, OrderedMap, Set,
    record, Some, Nothing, Ok, Err, borrow, live_tasks, controlled_tasks,
    task_map, task_map_with,
)
from pyalamode.effects import (
    IO, State, Clock, Random, Environment, IOCapability, StateCapability,
    ClockCapability, RandomCapability, EnvironmentCapability, recorded_io,
    state, recorded_clock, recorded_random, recorded_environment,
)
from pyalamode.builders import vector_build
from pyalamode.boundaries import validate_data
from pyalamode.task_contracts import (
    TASK_VERSION, TASK_NAMES, TASK_OPERATIONS, TASK_SETUPS, TASK_FOUNDATIONS,
    TASK_ORDERING, TASK_CANCELLATION, TASK_FAILURE, TASK_LIFETIME,
    operation_catalog, operation_contract, setup_catalog, setup_contract,
)

runtime = importlib.import_module("pyalamode.tasks")
effect_runtime = importlib.import_module("pyalamode.effects")
FULL_IO = ("read_text", "write_text")


class Hooks:
    calls = []

    def __getattribute__(self, name):
        Hooks.calls.append("attribute")
        return object.__getattribute__(self, name)

    def __call__(self, *args):
        Hooks.calls.append("call")
        raise AssertionError("foreign callback")

    def __iter__(self):
        Hooks.calls.append("iter")
        raise AssertionError("foreign iterator")

    def __hash__(self):
        Hooks.calls.append("hash")
        raise AssertionError("foreign hash")

    def __eq__(self, other):
        Hooks.calls.append("eq")
        raise AssertionError("foreign equality")

    def __repr__(self):
        Hooks.calls.append("repr")
        raise AssertionError("foreign representation")


class IntSubclass(int):
    pass


class TupleSubclass(tuple):
    pass


class StrSubclass(str):
    pass


class Abort(BaseException):
    pass


@record
class Message:
    name: str
    values: Vector[int]


def stored(value):
    assert type(value) is Vector
    items = object.__getattribute__(value, "_items")
    assert type(items) is tuple
    return items


def forged(items):
    value = object.__new__(Vector)
    object.__setattr__(value, "_items", items)
    return value


def identity(value):
    return value


class RuntimeTasks(unittest.TestCase):
    def setUp(self):
        Hooks.calls.clear()

    def same_error(self, error, call):
        try:
            call()
        except BaseException as observed:
            self.assertIs(observed, error)
        else:
            self.fail("expected retained exception object")

    def test_identity_declarations_and_annotation_boundaries(self):
        self.assertEqual(Task, "Task")
        self.assertIs(type(Task), str)
        def function(value=3):
            return value
        function.marker = "before"
        before = (function.__code__, function.__defaults__, dict(function.__dict__))
        self.assertIs(effects(Task)(function), function)
        self.assertEqual(before, (function.__code__, function.__defaults__, function.__dict__))
        annotation = Effectful[[TaskCapability, int], Vector[int], Task]
        self.assertIs(type(annotation), GenericAlias)
        self.assertEqual(annotation.__args__, ((TaskCapability, int), Vector[int], Task))
        self.assertIs(Effectful[[int], int, Task].__origin__, Effectful)
        for families in ((Task, Task), ("Future",), (True,), (Hooks(),), (StrSubclass(Task),)):
            with self.assertRaises(TypeError):
                effects(*families)
        for make in (lambda: Effectful[[TaskCapability], int, State],
                     lambda: Effectful[[int], TaskCapability, Task],
                     lambda: Effectful[[tuple[TaskCapability]], int, Task],
                     lambda: Effectful[[typing.Callable[[TaskCapability], int]], int, Task]):
            with self.assertRaises(TypeError):
                make()
        with self.assertRaises(TypeError):
            validate_data(live_tasks(1), ("int",))
        self.assertEqual(Hooks.calls, [])

    def test_setup_exact_types_bounds_and_no_callbacks(self):
        with patch.object(runtime, "_launch", side_effect=AssertionError("setup launched")):
            for workers in (1, 4):
                for maximum in (1, 256):
                    self.assertIs(type(live_tasks(workers, max_tasks=maximum)), TaskCapability)
            for order in ((), (0,), (2, 0, 1)):
                self.assertIs(type(controlled_tasks(order)), TaskCapability)
            for value in (True, IntSubclass(1), Hooks(), "1"):
                with self.assertRaises(TypeError):
                    live_tasks(value)
                with self.assertRaises(TypeError):
                    live_tasks(1, max_tasks=value)
            for value in (-1, 0, 5):
                with self.assertRaises(ValueError):
                    live_tasks(value)
            for value in (-1, 0, 257):
                with self.assertRaises(ValueError):
                    live_tasks(1, max_tasks=value)
            for value in ([], Hooks(), TupleSubclass((0,)), (True,), (IntSubclass(0),)):
                with self.assertRaises(TypeError):
                    controlled_tasks(value)
            for value in ((0, 0), (1,), (-1,), tuple(range(257))):
                with self.assertRaises(ValueError):
                    controlled_tasks(value)
            for value in (True, IntSubclass(0), Hooks(), "0"):
                with self.assertRaises(TypeError):
                    controlled_tasks((0,), cancel_after=value)
            for value in (-1, 2):
                with self.assertRaises(ValueError):
                    controlled_tasks((0,), cancel_after=value)
        self.assertEqual(Hooks.calls, [])

    def test_empty_serial_order_sequential_reuse_and_aliases(self):
        owner = _thread.get_ident()
        calls = []
        def callback(value):
            calls.append((value, _thread.get_ident()))
            return value + 1
        provider = live_tasks(1)
        self.assertEqual(stored(task_map(provider, callback, Vector())), ())
        self.assertEqual(stored(task_map(controlled_tasks((), cancel_after=0), callback, Vector())), ())
        with patch.object(runtime, "_launch", side_effect=AssertionError("serial launch")):
            first = task_map(provider, callback, Vector.of(3, 1, 2))
            second = task_map(provider, callback, Vector.of(3, 1, 2))
        self.assertEqual(stored(first), (4, 2, 3))
        self.assertEqual(stored(second), (4, 2, 3))
        self.assertIsNot(first, second)
        self.assertEqual(calls, [(value, owner) for value in (3, 1, 2, 3, 1, 2)])
        shared = Vector.of(11, 12)
        result = task_map(provider, lambda value: shared, Vector.of(0, 1))
        self.assertTrue(all(value is shared for value in stored(result)))
        self.assertEqual(stored(shared), (11, 12))

    def test_nested_stable_families_and_canonical_invalid_path(self):
        values = Vector.of(None, True, 7, "text", b"bytes", (2, "x"),
                           Vector.of(3), OrderedMap.of(("b", 2), ("a", 1)),
                           Map.of(("b", Vector.of(2)), ("a", Vector.of(1))),
                           Set.of(2, 1), Message("item", Vector.of(5)),
                           Some(9), Nothing(), Ok("yes"), Err("no"))
        result = task_map(live_tasks(2), identity, values)
        self.assertEqual(stored(result), stored(values))
        self.assertTrue(all(left is right for left, right in zip(stored(result), stored(values))))
        self.assertEqual(stored(task_map(live_tasks(1), identity, result)), stored(result))
        invalid_map = object.__new__(Map)
        object.__setattr__(invalid_map, "_entries", (("z", []), ("a", [])))
        with self.assertRaisesRegex(TypeError, r"messages\[0\]\.entries\['a'\]\.value"):
            task_map(live_tasks(2), identity, forged((invalid_map,)))

    def test_invalid_messages_reject_before_user_or_native_hooks(self):
        builders = []
        vector_build(lambda builder: builders.append(builder))
        with borrow(state(1)) as view:
            pass
        cycle = object.__new__(Vector)
        object.__setattr__(cycle, "_items", (cycle,))
        called = []
        def callback(value):
            called.append(value)
            return 1
        bad = ([], Hooks(), state(1), live_tasks(1), view, builders[0], identity, IntSubclass(3), cycle)
        provider = live_tasks(2)
        with patch.object(runtime, "_launch", side_effect=AssertionError("invalid message launched")):
            for value in bad:
                with self.assertRaises(TypeError):
                    task_map(provider, callback, forged(((value,),)))
            for value in ([], Hooks(), object.__new__(Vector), forged([])):
                with self.assertRaises(TypeError):
                    task_map(provider, callback, value)
        self.assertEqual(called, [])
        self.assertEqual(Hooks.calls, [])
        self.assertEqual(stored(task_map(provider, identity, Vector.of(2))), (2,))

    def test_callable_result_limits_without_annotation_capture_inference(self):
        provider = live_tasks(1)
        for callback in (Hooks(), [].append):
            with self.assertRaises(TypeError):
                task_map(provider, callback, Vector.of(1))
        with self.assertRaises(TypeError):
            task_map(provider, lambda: 1, Vector.of(1))
        builders = []
        vector_build(lambda builder: builders.append(builder))
        for result in ([], Hooks(), state(1), live_tasks(1), builders[0], identity):
            with self.assertRaises(TypeError):
                task_map(provider, lambda value: result, Vector.of(1))
        captured = []
        def ordinary(value=Hooks()):
            captured.append(value)
            return value + 1
        ordinary.__annotations__ = {"value": Hooks(), "return": Hooks()}
        self.assertEqual(stored(task_map(provider, ordinary, Vector.of(1, 2))), (2, 3))
        self.assertEqual(captured, [1, 2])
        self.assertEqual(Hooks.calls, [])

    def test_actual_concurrent_waves_and_input_order(self):
        barrier = threading.Barrier(2, timeout=5)
        second_done = threading.Event()
        events = []
        lock = threading.Lock()
        owner = _thread.get_ident()
        def callback(value):
            with lock:
                events.append(("start", value, _thread.get_ident()))
            if value < 2:
                barrier.wait()
                if value == 0:
                    self.assertTrue(second_done.wait(5))
                else:
                    with lock:
                        events.append(("done", value, _thread.get_ident()))
                    return value * 10
            with lock:
                if value >= 2:
                    self.assertEqual({item[1] for item in events if item[0] == "done" and item[1] < 2}, {0, 1})
                events.append(("done", value, _thread.get_ident()))
            return value * 10
        real_launch = runtime._launch
        launched = []
        def launch(run, handle):
            index = len(launched)
            launched.append(handle)
            def completed_runner():
                run()
                if index == 1:
                    second_done.set()
            real_launch(completed_runner, handle)
        with patch.object(runtime, "_launch", launch):
            self.assertEqual(stored(task_map(live_tasks(2), callback, Vector.of(0, 1, 2, 3))), (0, 10, 20, 30))
        self.assertEqual(sorted(value for kind, value, ident in events if kind == "start"), [0, 1, 2, 3])
        self.assertTrue(all(ident != owner for kind, value, ident in events))
        self.assertLess(next(i for i, event in enumerate(events) if event[:2] == ("done", 1)),
                        next(i for i, event in enumerate(events) if event[:2] == ("done", 0)))

    def test_live_four_workers_and_maximum_cardinality(self):
        barrier = threading.Barrier(4, timeout=5)
        lock = threading.Lock()
        counts = [0, 0]
        def callback(value):
            with lock:
                counts[0] += 1
                counts[1] = max(counts)
            try:
                barrier.wait()
                return value + 1
            finally:
                with lock:
                    counts[0] -= 1
        self.assertEqual(stored(task_map(live_tasks(4), callback, Vector.of(0, 1, 2, 3, 4, 5, 6, 7))), tuple(range(1, 9)))
        self.assertEqual(counts, [0, 4])
        values = Vector.of(*range(256))
        self.assertEqual(stored(task_map(live_tasks(4), lambda value: value * value, values)), tuple(value * value for value in range(256)))
        self.assertEqual(stored(values), tuple(range(256)))
        with patch.object(runtime, "_launch", side_effect=AssertionError("oversize launched")):
            with self.assertRaises(ValueError):
                task_map(live_tasks(4), identity, Vector.of(*range(257)))

    def test_live_failure_selects_lowest_input_index_and_cleans_wave(self):
        first, second = ValueError("input0"), RuntimeError("input1")
        second_finished = threading.Event()
        events = []
        lock = threading.Lock()
        def callback(value):
            if value == 0:
                self.assertTrue(second_finished.wait(5))
            with lock:
                events.append(value)
            if value == 1:
                raise second
            if value == 0:
                raise first
            return value
        provider = live_tasks(2)
        real_launch = runtime._launch
        launched = []
        def launch(run, handle):
            index = len(launched)
            launched.append(handle)
            def completed_runner():
                run()
                if index == 1:
                    second_finished.set()
            real_launch(completed_runner, handle)
        with patch.object(runtime, "_launch", launch):
            self.same_error(first, lambda: task_map(provider, callback, Vector.of(0, 1, 2, 3)))
        self.assertEqual(events, [1, 0])
        self.assertEqual(stored(task_map(provider, identity, Vector.of(4))), (4,))
        events.clear()
        def later_failure(value):
            with lock:
                events.append(value)
            if value == 2:
                raise first
            return value
        self.same_error(first, lambda: task_map(provider, later_failure, Vector.of(0, 1, 2, 3, 4)))
        self.assertEqual(sorted(events), [0, 1, 2, 3])

    def test_controlled_order_is_exact_and_repeatable(self):
        events = []
        provider = controlled_tasks((2, 0, 1))
        def callback(value):
            events.append(value)
            return value * 2
        with patch.object(runtime, "_launch", side_effect=AssertionError("controlled launch")):
            for _ in range(2):
                self.assertEqual(stored(task_map(provider, callback, Vector.of(1, 2, 3))), (2, 4, 6))
        self.assertEqual(events, [3, 1, 2, 3, 1, 2])

    def test_controlled_cancellation_edges_and_validation_precedence(self):
        for cutoff, expected in ((0, []), (2, [3, 1]), (3, [3, 1, 2]), (None, [3, 1, 2])):
            calls = []
            provider = controlled_tasks((2, 0, 1), cancel_after=cutoff)
            def callback(value):
                calls.append(value)
                return value
            for _ in range(2):
                calls.clear()
                if cutoff in (0, 2):
                    with self.assertRaisesRegex(RuntimeError, "^tasks: configured cancellation boundary reached$"):
                        task_map(provider, callback, Vector.of(1, 2, 3))
                else:
                    self.assertEqual(stored(task_map(provider, callback, Vector.of(1, 2, 3))), (1, 2, 3))
                self.assertEqual(calls, expected)
        provider = controlled_tasks((0,), cancel_after=0)
        with self.assertRaises(TypeError):
            task_map(provider, identity, forged(([],)))
        with self.assertRaises(ValueError):
            task_map(provider, identity, Vector())
        self.assertEqual(stored(task_map(controlled_tasks((), cancel_after=0), identity, Vector())), ())

    def test_controlled_first_scheduled_failure_before_cutoff(self):
        error = ValueError("scheduled2")
        calls = []
        def callback(value):
            calls.append(value)
            if value == 2:
                raise error
            return value
        provider = controlled_tasks((1, 2, 0), cancel_after=2)
        self.same_error(error, lambda: task_map(provider, callback, Vector.of(1, 2, 3)))
        self.assertEqual(calls, [2])
        calls.clear()
        def invalid_result(value):
            calls.append(value)
            return [] if value == 3 else value
        with self.assertRaises(TypeError):
            task_map(provider, invalid_result, Vector.of(1, 2, 3))
        self.assertEqual(calls, [2, 3])

    def test_external_families_use_fresh_serial_borrows(self):
        for tasks in (live_tasks(1), controlled_tasks((1, 0))):
            views = []
            def check_view(view):
                self.assertTrue(all(view is not previous for previous in views))
                views.append(view)
            cap = state(0)
            def update(view, value):
                check_view(view)
                view.set(view.get() + value)
                return view.get()
            expected = (1, 3) if object.__getattribute__(tasks, "_provider").mode == "live" else (3, 2)
            with patch.object(runtime, "_launch", side_effect=AssertionError("loan launch")):
                self.assertEqual(stored(task_map_with(tasks, cap, update, Vector.of(1, 2))), expected)
            self.assertEqual(cap.get(), 3)
            for view in views:
                with self.assertRaises(RuntimeError):
                    view.get()
        rows = (
            (recorded_io((), allowed_ops=FULL_IO), lambda view, value: (view.write_text(str(value), "written"), view.read_text(str(value)))[1], ("written", "written")),
            (recorded_clock((10, 20)), lambda view, value: view.now_ns(), (20, 10)),
            (recorded_random((2, 1)), lambda view, value: view.below(5), (1, 2)),
            (recorded_environment((("NAME", "value"),)), lambda view, value: view.get("NAME", "fallback"), ("value", "value")),
        )
        for cap, callback, expected in rows:
            self.assertEqual(stored(task_map_with(controlled_tasks((1, 0)), cap, callback, Vector.of(1, 2))), expected)
        for workers in (2, 3, 4):
            cap = state(7)
            with self.assertRaises(ValueError):
                task_map_with(live_tasks(workers), cap, lambda view, value: view.set(9), Vector.of(1))
            self.assertEqual(cap.get(), 7)
        with self.assertRaises(TypeError):
            task_map_with(live_tasks(1), live_tasks(1), lambda cap, value: value, Vector.of(1))

    def test_external_loan_closes_on_every_exit_and_keeps_effects(self):
        for error in (ValueError("callback"), Abort("abort"), KeyboardInterrupt("interrupt")):
            cap, views, contexts = state(0), [], []
            def callback(view, value):
                views.append(view)
                nested = borrow(view)
                contexts.append(nested)
                views.append(nested.__enter__())
                view.set(value)
                raise error
            with borrow(cap) as outer:
                self.same_error(error, lambda: task_map_with(live_tasks(1), outer, callback, Vector.of(3)))
                self.assertEqual(outer.get(), 3)
                for view in views:
                    with self.assertRaises(RuntimeError):
                        view.get()
                for context in contexts:
                    context.__exit__(None, None, None)
            self.assertEqual(cap.get(), 3)
        cap = recorded_io((), allowed_ops=FULL_IO)
        views = []
        def write(view, value):
            views.append(view)
            view.write_text("completed", str(value))
            return value
        with self.assertRaises(RuntimeError):
            task_map_with(controlled_tasks((0, 1), cancel_after=1), cap, write, Vector.of(7, 8))
        self.assertEqual(cap.read_text("completed"), "7")
        with self.assertRaises(RuntimeError):
            views[0].read_text("completed")
        invalid_cap = state(0)
        def invalid_result(view, value):
            view.set(5)
            views.append(view)
            return view
        with self.assertRaises(TypeError):
            task_map_with(live_tasks(1), invalid_cap, invalid_result, Vector.of(1))
        with self.assertRaises(RuntimeError):
            views[-1].get()
        self.assertEqual(invalid_cap.get(), 5)

    def test_task_lifetime_reentry_owner_and_opaque_interfaces(self):
        tasks = live_tasks(1)
        with self.assertRaises(TypeError):
            TaskCapability()
        with self.assertRaises(TypeError):
            type("Child", (TaskCapability,), {})
        with self.assertRaises(AttributeError):
            tasks._provider = None
        with self.assertRaises(AttributeError):
            del tasks._lease
        self.assertEqual(repr(tasks), "TaskCapability(<opaque>)")
        for bad in (Hooks(), state(1), object.__new__(TaskCapability)):
            with self.assertRaises(TypeError):
                task_map(bad, identity, Vector.of(1))
        context = borrow(tasks)
        scoped = context.__enter__()
        nested = borrow(scoped)
        dependent = nested.__enter__()
        self.assertEqual(stored(task_map(dependent, identity, Vector.of(1))), (1,))
        errors = []
        def other_thread():
            for call in (lambda: task_map(tasks, Hooks(), Hooks()), lambda: context.__exit__(None, None, None)):
                try:
                    call()
                except BaseException as error:
                    errors.append(error)
        thread = threading.Thread(target=other_thread)
        thread.start(); thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual([type(error) for error in errors], [RuntimeError, RuntimeError])
        self.assertEqual(stored(task_map(scoped, identity, Vector.of(2))), (2,))
        context.__exit__(None, None, None)
        for view in (scoped, dependent):
            with self.assertRaises(RuntimeError):
                task_map(view, identity, Vector.of(1))
        nested.__exit__(None, None, None)
        def reenter(value):
            with self.assertRaises(RuntimeError):
                task_map(tasks, Hooks(), Hooks())
            with self.assertRaises(RuntimeError):
                borrow(tasks)
            return value
        self.assertEqual(stored(task_map(tasks, reenter, Vector.of(3))), (3,))
        self.assertEqual(Hooks.calls, [])
        self.assertEqual(stored(task_map(tasks, identity, Vector.of(4))), (4,))

    def test_baseexception_identity_joined_without_native_unraisable(self):
        for error in (Abort("abort"), SystemExit(17), KeyboardInterrupt("interrupt")):
            for workers in (1, 2):
                done = []
                def callback(value):
                    done.append(value)
                    if value == 0:
                        raise error
                    return value
                with patch.object(sys, "unraisablehook") as hook:
                    tasks = live_tasks(workers)
                    self.same_error(error, lambda: task_map(tasks, callback, Vector.of(0, 1, 2)))
                    self.assertEqual(sorted(done), [0] if workers == 1 else [0, 1])
                    hook.assert_not_called()
                self.assertEqual(stored(task_map(tasks, identity, Vector.of(5))), (5,))

    def test_coordinator_launch_faults_join_every_actual_start(self):
        real_launch, real_join = runtime._launch, runtime._join
        for mode in ("before_first", "before_second", "after_actual_start"):
            error = Abort(mode)
            attempted, joined, completed = [], [], []
            def launch(callback, handle):
                attempted.append(handle)
                if mode == "before_first" or mode == "before_second" and len(attempted) == 2:
                    raise error
                real_launch(callback, handle)
                if mode == "after_actual_start":
                    raise error
            def join(handle):
                joined.append(handle)
                real_join(handle)
            def callback(value):
                completed.append(value)
                return value
            tasks = live_tasks(2)
            with patch.object(runtime, "_launch", launch), patch.object(runtime, "_join", join):
                self.same_error(error, lambda: task_map(tasks, callback, Vector.of(0, 1, 2)))
            actual = [handle for handle in attempted if handle.ident]
            self.assertEqual(joined, actual)
            self.assertTrue(all(handle.is_done() for handle in actual))
            self.assertEqual(completed, [] if mode == "before_first" else [0])
            self.assertEqual(stored(task_map(tasks, identity, Vector.of(7))), (7,))

        # Ordinary fault substitution at the inner Python loop transition,
        # after a genuine first start and before the next native launch.
        error = Abort("loop transition")
        handles, joined = [], []
        def launch(callback, handle):
            handles.append(handle)
            real_launch(callback, handle)
        def join(handle):
            joined.append(handle)
            real_join(handle)
        def interrupted_range(*arguments):
            if len(arguments) != 2:
                return range(*arguments)
            def indices():
                yield arguments[0]
                raise error
            return indices()
        tasks = live_tasks(2)
        with patch.object(runtime, "range", interrupted_range, create=True), patch.object(runtime, "_launch", launch), patch.object(runtime, "_join", join):
            self.same_error(error, lambda: task_map(tasks, identity, Vector.of(0, 1, 2)))
        self.assertEqual(joined, handles)
        self.assertEqual(len(handles), 1)
        self.assertTrue(handles[0].is_done())
        self.assertEqual(stored(task_map(tasks, identity, Vector.of(7))), (7,))

    def test_coordinator_initial_joins_then_single_retry_and_revocation(self):
        real_launch, real_join = runtime._launch, runtime._join
        for unresolved in (False, True):
            tasks = live_tasks(2)
            handles, calls = [], []
            primary, secondary = Abort("first coordinator"), RuntimeError("later cleanup")
            def launch(callback, handle):
                handles.append(handle)
                real_launch(callback, handle)
            def join(handle):
                index = handles.index(handle)
                calls.append(index)
                # Real termination is observed even when the ordinary seam
                # models a coordinator exception after the native join.
                real_join(handle)
                if calls.count(index) == 1 or unresolved and index == 0:
                    raise primary if len(calls) == 1 else secondary
            with borrow(tasks) as view:
                with patch.object(runtime, "_launch", launch), patch.object(runtime, "_join", join):
                    self.same_error(primary, lambda: task_map(view, identity, Vector.of(0, 1, 2)))
                self.assertEqual(calls, [0, 1, 0, 1])
                self.assertTrue(all(handle.is_done() for handle in handles))
                if unresolved:
                    with self.assertRaisesRegex(RuntimeError, "permanently revoked"):
                        task_map(view, identity, Vector.of(8))
                else:
                    self.assertEqual(stored(task_map(view, identity, Vector.of(8))), (8,))
            if unresolved:
                with self.assertRaisesRegex(RuntimeError, "permanently revoked"):
                    task_map(tasks, identity, Vector.of(8))
            else:
                self.assertEqual(stored(task_map(tasks, identity, Vector.of(8))), (8,))

    def test_detached_closed_catalog_and_exact_lookups(self):
        self.assertEqual(TASK_VERSION, "pyalamode.tasks-v1")
        self.assertEqual(TASK_NAMES, {"live_tasks", "controlled_tasks", "task_map", "task_map_with"})
        self.assertEqual(TASK_OPERATIONS, {"task_map", "task_map_with"})
        self.assertEqual(TASK_SETUPS, {"live_tasks", "controlled_tasks"})
        self.assertEqual(TASK_FOUNDATIONS["_thread"], {"_ThreadHandle", "get_ident", "start_joinable_thread"})
        self.assertEqual(TASK_FOUNDATIONS["sys"], {"addaudithook"})
        operations, setups = operation_catalog(), setup_catalog()
        self.assertEqual(len(operations), 2)
        self.assertEqual(len(setups), 2)
        self.assertEqual([row["identity"] for row in operations], ["pyalamode.tasks.task_map", "pyalamode.tasks.task_map_with"])
        expected_keys = {"identity", "version", "runtime", "signature", "inputs", "output", "effects", "failures", "ordinary_invalid_inputs", "behavior", "ordering", "callback", "lifetime", "implicit_dispatch", "aliases", "initialization", "generic_arguments", "phase", "bounds", "complexity", "preconditions", "evidence", "foundations", "approval", "owner", "rationale", "cancellation", "failure", "cleanup", "scheduling"}
        for row in operations:
            self.assertEqual(set(row), expected_keys)
            self.assertEqual((row["ordering"], row["cancellation"], row["failure"], row["lifetime"]), (TASK_ORDERING, TASK_CANCELLATION, TASK_FAILURE, TASK_LIFETIME))
        for row in setups:
            self.assertEqual(set(row), {"aliases", "behavior", "effects", "evidence", "failures", "identity", "policy", "version"})
        before = json.loads(json.dumps(operations))
        operations[0]["callback"]["captures"] = "mutated"
        operations[0]["effects"].append("Future")
        operations[0]["initialization"]["effects"].append("Future")
        self.assertEqual(operation_catalog(), before)
        setups[0]["effects"].append("Future")
        self.assertEqual(setup_catalog()[0]["effects"], [])
        for name in ("task_map", "task_map_with"):
            for alias in (name, "tasks." + name, "pyalamode.tasks." + name):
                self.assertEqual(operation_contract(alias)["identity"], "pyalamode.tasks." + name)
        for name in ("live_tasks", "controlled_tasks"):
            for alias in (name, "tasks." + name, "pyalamode.tasks." + name):
                self.assertEqual(setup_contract(alias)["identity"], "pyalamode.tasks." + name)
        for value in (Hooks(), StrSubclass("task_map"), "other", None):
            self.assertIsNone(operation_contract(value))
            self.assertIsNone(setup_contract(value))
        self.assertEqual(Hooks.calls, [])
