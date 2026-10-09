"""Meaningful runtime invariants for closed alternatives and actual failure copies."""

import unittest

from pyalamode import (oneof, case, Option, Some, Nothing, Result, Ok, Err,
                      accumulate, Failure, failure_value, record, replace,
                      Vector, Map, OrderedMap, Set, freeze, thaw, recorded_clock)
from pyalamode.boundaries import validate_data
from pyalamode import records as _records
from pyalamode import sums as _sums
from pyalamode import failures as _failures


@record
class Point:
    number: int


@oneof
class Lookup:
    @case
    class Found:
        point: Point
        label: str = "default"

    @case
    class Missing:
        pass


@oneof
class Batch:
    @case
    class Ready:
        entries: Vector[Lookup]
        selected: Lookup.Found
        answer: Result[Option[int], Failure]

    @case
    class Empty:
        pass


@record
class Saved:
    case_value: Lookup
    exact: Lookup.Found
    optional: Option[Lookup]
    result: Result[int, Failure]


class M6RuntimeTests(unittest.TestCase):
    def test_fixed_fields_defaults_and_native_patterns(self):
        value = Lookup.Found(Point(4))
        self.assertEqual(value.label, "default")
        self.assertEqual(Lookup.Found.__match_args__, ("point", "label"))
        match value:
            case Lookup.Found(Point(number), label):
                observed = number, label
            case _:
                self.fail("ordinary class pattern did not match")
        self.assertEqual(observed, (4, "default"))
        match Lookup.Missing():
            case Lookup.Missing():
                absent = True
            case _:
                absent = False
        self.assertTrue(absent)

    def test_fixed_constructor_failures(self):
        for invoke in (lambda: Lookup.Found(), lambda: Lookup.Found(1),
                       lambda: Lookup.Found(Point(True)), lambda: Lookup.Found(Point(1), 7),
                       lambda: Lookup.Found(Point(1), point=Point(2)),
                       lambda: Lookup.Found(Point(1), unknown="x"),
                       lambda: Lookup.Found(Point(1), "x", "extra"),
                       lambda: Lookup.Missing(1), lambda: Nothing(value=1),
                       lambda: Some(), lambda: Err(value="bad")):
            with self.subTest(invoke=invoke), self.assertRaises(TypeError):
                invoke()

    def test_immutability_reinitialization_and_subclasses(self):
        value = Lookup.Found(Point(1))
        for invoke in (lambda: setattr(value, "label", "new"), lambda: delattr(value, "point"),
                       lambda: value.__init__(Point(2)), lambda: setattr(Lookup, "New", object),
                       lambda: delattr(Lookup, "Found")):
            with self.assertRaises(AttributeError):
                invoke()
        for base in (Lookup.Found, Some, Nothing, Ok, Err, Option, Result, Lookup):
            with self.subTest(base=base), self.assertRaises(TypeError):
                type("Child", (base,), {})
        for value in (Some(1), Nothing(), Ok(1), Err("x"), Lookup.Missing()):
            with self.assertRaises(TypeError):
                hash(value)
        with self.assertRaises(TypeError):
            Lookup()
        with self.assertRaises(TypeError):
            Option()
        with self.assertRaises(TypeError):
            Result()
        with self.assertRaises(AttributeError):
            object.__getattribute__(value, "__dict__")

    def test_constructor_keyword_binding_adds_no_foreign_calls(self):
        hooks = []
        class Key(str):
            def __hash__(self):
                hooks.append("hash")
                return str.__hash__(self)
            def __eq__(self, other):
                hooks.append("equal")
                return str.__eq__(self, other)
        arguments = {Key("value"): 1}
        class Plain:
            def __init__(self, /, *args, **kwargs):
                pass
        hooks.clear()
        Plain(**arguments)
        binding_calls = list(hooks)
        hooks.clear()
        with self.assertRaises(TypeError):
            Some(**arguments)
        self.assertEqual(hooks, binding_calls)

    def test_public_payload_names_do_not_collide_with_constructor(self):
        @oneof
        class PublicNames:
            @case
            class Data:
                self: int
                value: str
                args: bool
        value = PublicNames.Data(self=1, value="x", args=True)
        self.assertEqual((value.self, value.value, value.args), (1, "x", True))
        self.assertEqual(PublicNames.Data.__match_args__, ("self", "value", "args"))

    def test_exact_tag_and_type_sensitive_equivalence(self):
        self.assertNotEqual(Some(True), Some(1))
        self.assertNotEqual(Ok(1), Some(1))
        self.assertNotEqual(Nothing(), Lookup.Missing())
        self.assertEqual(Lookup.Found(Point(1)), Lookup.Found(point=Point(1), label="default"))
        self.assertNotEqual(Lookup.Found(Point(1), "a"), Lookup.Found(Point(1), "b"))
        self.assertEqual(Vector.of(Some(1), Nothing()), Vector.of(Some(1), Nothing()))
        self.assertNotEqual(Vector.of(Some(True)), Vector.of(Some(1)))
        self.assertEqual(repr(Lookup.Found(Point(1))), "Found(point=Point(number=1), label='default')")
        self.assertEqual(repr(Some(Vector.of(1))), "Some(value=Vector.of(1))")

    def test_nested_exact_values_and_retained_versions(self):
        before = Vector.of(Lookup.Found(Point(1)))
        after = before.appended(Lookup.Missing())
        status = Ok(Some(7))
        value = Batch.Ready(after, before[0], status)
        self.assertEqual(len(before), 1)
        self.assertEqual(len(value.entries), 2)
        self.assertEqual(value.selected.point.number, 1)
        self.assertIs(value.answer, status)
        saved = Saved(value.selected, value.selected, Some(Lookup.Missing()), Ok(3))
        self.assertIs(freeze(saved), saved)
        with self.assertRaises(TypeError):
            replace(value.selected, label="changed")

    def test_collections_accept_cases_but_scalar_keys_stay_closed(self):
        item = Some(Lookup.Missing())
        self.assertIs(Map.of(("a", item))["a"], item)
        self.assertIs(OrderedMap.of(("a", item)).values()[0], item)
        self.assertEqual(Vector.of(item).map(lambda x: x)[0], item)
        with self.assertRaises(TypeError):
            Map.of((Some(1), "value"))
        with self.assertRaises(TypeError):
            Set.of(Some(1))

    def test_option_result_stock_patterns(self):
        observations = []
        for value in (Some(3), Nothing(), Ok("done"), Err(Failure("x", "y"))):
            match value:
                case Some(value=number):
                    observations.append(("some", number))
                case Nothing():
                    observations.append(("nothing",))
                case Ok(value=text):
                    observations.append(("ok", text))
                case Err(error=Failure(category=kind, message=message)):
                    observations.append(("err", kind, message))
                case _:
                    self.fail("known case did not match")
        self.assertEqual(observations, [("some", 3), ("nothing",), ("ok", "done"), ("err", "x", "y")])

    def test_option_result_deep_schema_guards(self):
        schemas = ((Some(1), ("Option", ("int",))), (Nothing(), ("Option", ("int",))),
                   (Ok(1), ("Result", ("int", "str"))), (Err("x"), ("Result", ("int", "str"))),
                   (Some(1), ("Some", ("int",))), (Nothing(), ("Nothing", ())),
                   (Ok(1), ("Ok", ("int",))), (Err("x"), ("Err", ("str",))))
        for value, schema in schemas:
            self.assertIs(validate_data(value, schema), value)
        for value, schema in ((Some(True), ("Option", ("int",))), (Ok("bad"), ("Result", ("int", "str"))),
                              (Err(4), ("Result", ("int", "str"))), (Nothing(), ("Some", ("int",))),
                              (Ok(1), ("Option", ("int",))), (Some(1), ("Result", ("int", "str")))):
            with self.assertRaises(TypeError):
                validate_data(value, schema)

    def test_domain_and_exact_case_schema_guards(self):
        domain = _records._annotation_schema(Lookup)
        exact = _records._annotation_schema(Lookup.Found)
        self.assertIs(validate_data(Lookup.Missing(), domain).__class__, Lookup.Missing)
        self.assertEqual(validate_data(Lookup.Found(Point(2)), exact).point.number, 2)
        for value, schema in ((Lookup.Missing(), exact), (Some(1), domain),
                              (Batch.Empty(), domain)):
            with self.assertRaises(TypeError):
                validate_data(value, schema)
        with self.assertRaises(TypeError):
            validate_data(Lookup.Missing(), ("oneof", Lookup, domain[2][:-1]))
        with self.assertRaises(TypeError):
            validate_data(Lookup.Missing(), ("case", Lookup.Missing, (("wrong", "int"),)))

    def test_generic_alias_annotations_are_finite(self):
        self.assertEqual(_records._annotation_schema(Option[int]), ("Option", ("int",)))
        self.assertEqual(_records._annotation_schema(Result[int, str]), ("Result", ("int", "str")))
        self.assertEqual(_records._annotation_schema(Some[int]), ("Some", ("int",)))
        self.assertEqual(_records._annotation_schema(Nothing), ("Nothing", ()))
        for invoke in (lambda: Option[int, str], lambda: Result[int], lambda: Some[int, str],
                       lambda: Nothing[int], lambda: Lookup.Found[int], lambda: Option[list],
                       lambda: Result[int, object], lambda: _records._annotation_schema(Option),
                       lambda: _records._annotation_schema(Some)):
            with self.assertRaises(TypeError):
                invoke()
        self.assertIs(freeze(Some(2), schema=Option[int]).__class__, Some)
        with self.assertRaises(TypeError):
            freeze(Some(True), schema=Option[int])

    def test_future_annotation_domain_and_generic_schema(self):
        namespace = {"Lookup": Lookup, "Option": Option, "Result": Result, "Failure": Failure,
                     "Some": Some, "Nothing": Nothing, "Vector": Vector}
        self.assertEqual(_records._annotation_schema("Lookup.Found", namespace), _records._annotation_schema(Lookup.Found))
        self.assertEqual(_records._annotation_schema("Option[Lookup]", namespace), ("Option", (_records._annotation_schema(Lookup),)))
        self.assertEqual(_records._annotation_schema("Result[Vector[int], Failure]", namespace)[0], "Result")
        self.assertEqual(_records._annotation_schema("Some[int]", namespace), ("Some", ("int",)))
        for annotation in ("Lookup.missing", "Lookup.Found[int]", "Result[int]", "Option[print('boom')]",
                           "__import__('os').system('boom')", "Option[object]"):
            with self.assertRaises(TypeError):
                _records._annotation_schema(annotation, namespace)

    def test_mutable_raw_exception_callable_and_capability_payloads_refused(self):
        for value in ([], {}, {1}, bytearray(b"x"), object(), ValueError("x"),
                      lambda: 1, recorded_clock((1,)), (1, []), Vector.of(1).__iter__()):
            for constructor in (Some, Ok, Err):
                with self.subTest(kind=type(value), constructor=constructor), self.assertRaises(TypeError):
                    constructor(value)
            with self.assertRaises(TypeError):
                freeze(value)

    def test_no_foreign_value_or_metaclass_hooks(self):
        hooks = []
        class Meta(type):
            def __hash__(self):
                hooks.append("meta hash")
                return 0
            def __eq__(self, other):
                hooks.append("meta equal")
                return False
            def __getattribute__(self, name):
                hooks.append("meta getattr")
                return super().__getattribute__(name)
        class Hostile(metaclass=Meta):
            def __getattribute__(self, name):
                hooks.append("getattr")
                raise AssertionError(name)
            def __iter__(self):
                hooks.append("iter")
                raise AssertionError
            def __hash__(self):
                hooks.append("hash")
                raise AssertionError
            def __repr__(self):
                hooks.append("repr")
                raise AssertionError
            def __str__(self):
                hooks.append("str")
                raise AssertionError
            def __eq__(self, other):
                hooks.append("equal")
                raise AssertionError
        value = Hostile()
        for invoke in (lambda: Some(value), lambda: Ok((value,)), lambda: Err(value),
                       lambda: freeze(value), lambda: thaw(value), lambda: failure_value(value),
                       lambda: Option[Hostile], lambda: validate_data(Nothing(), ("oneof", Hostile, ())),
                       lambda: validate_data(Nothing(), ("case", Hostile, ()))):
            with self.assertRaises(TypeError):
                invoke()
        self.assertEqual(hooks, [])

    def test_forged_storage_and_cycle_refused_deeply(self):
        uninitialized = object.__new__(Some)
        with self.assertRaises(TypeError):
            freeze(uninitialized)
        malformed = object.__new__(Some)
        object.__setattr__(malformed, "_pal_initialized", True)
        object.__setattr__(malformed, "value", [])
        for invoke in (lambda: Vector.of(malformed), lambda: freeze(malformed),
                       lambda: thaw(malformed), lambda: validate_data(malformed, ("Option", ("int",))),
                       lambda: Some(malformed)):
            with self.assertRaises(TypeError):
                invoke()
        cycle = object.__new__(Some)
        object.__setattr__(cycle, "_pal_initialized", True)
        object.__setattr__(cycle, "value", cycle)
        with self.assertRaises(TypeError):
            freeze(cycle)
        forged = object.__new__(Lookup.Found)
        object.__setattr__(forged, "_pal_initialized", 1)
        object.__setattr__(forged, "point", Point(1))
        object.__setattr__(forged, "label", "a")
        with self.assertRaises(TypeError):
            freeze(forged)

    def test_no_partial_initialization_from_failed_validation(self):
        value = object.__new__(Lookup.Found)
        with self.assertRaises(TypeError):
            value.__init__(Point(1), 7)
        with self.assertRaises(AttributeError):
            object.__getattribute__(value, "point")
        value.__init__(Point(2), "ready")
        self.assertEqual(value.point.number, 2)
        prefilled = object.__new__(Lookup.Found)
        object.__setattr__(prefilled, "point", Point(3))
        with self.assertRaises(AttributeError):
            prefilled.__init__(Point(4))
        self.assertEqual(prefilled.point.number, 3)

    def test_freeze_reuses_deeply_valid_cases(self):
        value = Some(Batch.Ready(Vector.of(Lookup.Missing()), Lookup.Found(Point(1)), Err(Failure("a", "b"))))
        self.assertIs(freeze(value), value)
        copied = freeze([value, value], exclusive=True)
        self.assertIs(copied[0], value)
        self.assertIs(copied[1], value)
        with self.assertRaises(TypeError):
            freeze([value])

    def test_thaw_exact_envelopes_are_recursively_fresh(self):
        shared = Some(Vector.of(Point(1)))
        exported = thaw((shared, shared))
        self.assertEqual(tuple(exported[0]), ("oneof", "case", "fields"))
        self.assertEqual(exported[0]["oneof"], "pyalamode:Option")
        self.assertEqual(exported[0]["case"], "Some")
        exported[0]["fields"]["value"][0]["number"] = 99
        self.assertEqual(exported[1]["fields"]["value"][0]["number"], 1)
        self.assertEqual(shared.value[0].number, 1)
        self.assertEqual(thaw(Nothing()), {"oneof": "pyalamode:Option", "case": "Nothing", "fields": {}})
        self.assertEqual(thaw(Lookup.Missing())["oneof"], __name__ + ":Lookup")
        self.assertEqual(thaw(Err("bad")), {"oneof": "pyalamode:Result", "case": "Err", "fields": {"error": "bad"}})

    def test_accumulate_success_and_ordered_independent_errors(self):
        left, right = Ok(1), Ok("x")
        self.assertEqual(accumulate(left, right), Ok((1, "x")))
        self.assertEqual(accumulate(Err("first"), right), Err(Vector.of("first")))
        self.assertEqual(accumulate(left, Err("second")), Err(Vector.of("second")))
        self.assertEqual(accumulate(Err("first"), Err("second")), Err(Vector.of("first", "second")))
        trace = []
        def input_value(name):
            trace.append(name)
            return Err(name)
        self.assertEqual(accumulate(input_value("left"), input_value("right")), Err(Vector.of("left", "right")))
        self.assertEqual(trace, ["left", "right"])
        self.assertEqual(left, Ok(1))
        self.assertEqual(right, Ok("x"))

    def test_accumulate_retains_structured_errors_without_flattening(self):
        first, second = Failure("a", "first"), Failure("b", "second")
        result = accumulate(Err(first), Err(second))
        self.assertIs(result.error[0], first)
        self.assertIs(result.error[1], second)
        again = accumulate(result, Err(Vector.of(first)))
        self.assertEqual(again, Err(Vector.of(Vector.of(first, second), Vector.of(first))))
        for left, right in ((Some(1), Ok(2)), (Ok(1), Nothing()), (1, Err("x"))):
            with self.assertRaises(TypeError):
                accumulate(left, right)
        forged = object.__new__(Err)
        object.__setattr__(forged, "_pal_initialized", True)
        object.__setattr__(forged, "error", [])
        with self.assertRaises(TypeError):
            accumulate(Ok(1), forged)

    def test_declaration_refusals_and_unattached_cases(self):
        @case
        class Alone:
            value: int
        with self.assertRaises(TypeError):
            Alone(1)
        with self.assertRaises(TypeError):
            case(Alone)
        class EmptyDomain:
            pass
        with self.assertRaises(TypeError):
            oneof(EmptyDomain)
        class WrongDomain:
            Alias = Alone
        with self.assertRaises(TypeError):
            oneof(WrongDomain)
        class FieldDomain:
            value: int
        with self.assertRaises(TypeError):
            oneof(FieldDomain)
        class MethodCase:
            def run(self):
                return 1
        with self.assertRaises(TypeError):
            case(MethodCase)
        class Base:
            pass
        class Derived(Base):
            value: int
        with self.assertRaises(TypeError):
            case(Derived)
        class MutableDefault:
            value: tuple[int, ...] = []
        with self.assertRaises(TypeError):
            case(MutableDefault)
        class WrongDefaultOrder:
            first: int = 1
            second: int
        with self.assertRaises(TypeError):
            case(WrongDefaultOrder)

    def test_malformed_schema_metadata_has_no_foreign_comparison(self):
        hooks = []
        class Evil:
            def __eq__(self, other):
                hooks.append("equal")
                raise AssertionError
        bad = Evil()
        for schema in (("case", Lookup.Found, (("point", bad),)),
                       ("oneof", Lookup, ((Lookup.Found, (("point", bad),)),)),
                       ("Result", ("int", bad)), ("Option", (bad,)),
                       ("Nothing", ("int",))):
            with self.assertRaises(TypeError):
                validate_data(Nothing(), schema)
        self.assertEqual(hooks, [])

    def test_future_annotation_module_metadata_rejects_foreign_keys(self):
        from types import ModuleType
        hooks = []
        class Key:
            def __hash__(self):
                return hash("Some")
            def __eq__(self, other):
                hooks.append("equal")
                raise AssertionError
        module = ModuleType("m06_hostile_annotations")
        module.__dict__[Key()] = Some
        hooks.clear()
        with self.assertRaises(TypeError):
            _records._annotation_schema("foreign.Some[int]", {"foreign": module})
        self.assertEqual(hooks, [])

    def test_every_exact_native_failure_identity_and_fixed_messages(self):
        self.assertEqual(len(_failures._NATIVE_FAILURES), 26)
        for kind, category, message in _failures._NATIVE_FAILURES:
            value = kind.__new__(kind)
            result = failure_value(value)
            self.assertEqual(result, Failure(category, message))
            self.assertIs(type(result), Failure)
        self.assertIs(IOError, OSError)
        self.assertIs(EnvironmentError, OSError)
        self.assertEqual(failure_value(RecursionError()).category, "RecursionError")
        self.assertEqual(failure_value(UnicodeError()).category, "UnicodeError")

    def test_genuine_builtin_operation_failures(self):
        observed = []
        for invoke in (lambda: 1 // 0, lambda: (1,)[4], lambda: Map.of(("a", 1))["b"],
                       lambda: Vector.of(1)[::0], lambda: b"\xff".decode("utf8"),
                       lambda: "\ud800".encode("utf8"), lambda: open("/pyalamode-m06-guaranteed-missing/no-file")):
            try:
                invoke()
            except (ZeroDivisionError, IndexError, KeyError, ValueError, OSError) as exception:
                observed.append(failure_value(exception).category)
        self.assertEqual(observed, ["ZeroDivisionError", "IndexError", "KeyError", "ValueError", "UnicodeError", "UnicodeError", "OSError"])

    def test_failure_copy_does_not_read_payload_formatting_or_dictionary(self):
        hooks = []
        class Payload:
            def __str__(self):
                hooks.append("str")
                raise AssertionError
            def __repr__(self):
                hooks.append("repr")
                raise AssertionError
            def __getattribute__(self, name):
                hooks.append("getattr")
                raise AssertionError
        mutable = [Payload()]
        exception = ValueError(mutable)
        exception.detail = mutable
        first = failure_value(exception)
        second = failure_value(exception)
        mutable.append("changed")
        exception.args = ("changed",)
        self.assertEqual(first, Failure("ValueError", "invalid value"))
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(thaw(first), {"category": "ValueError", "message": "invalid value"})
        self.assertEqual(hooks, [])

    def test_unknown_exception_subclasses_and_hooks_are_not_observed(self):
        hooks = []
        class Custom(ValueError):
            def __getattribute__(self, name):
                hooks.append("getattr")
                raise AssertionError
            def __str__(self):
                hooks.append("str")
                raise AssertionError
            def __repr__(self):
                hooks.append("repr")
                raise AssertionError
        for value in (Custom(), Exception(), BaseException(), TypeError(), StopIteration(), 1, "bad"):
            with self.assertRaises(TypeError):
                failure_value(value)
        self.assertEqual(hooks, [])

    def test_actual_except_cleanup_and_category_inheritance(self):
        try:
            raise RecursionError()
        except RuntimeError as caught:
            recursion = failure_value(caught)
        self.assertEqual(recursion.category, "RecursionError")
        with self.assertRaises(UnboundLocalError):
            _ = caught
        try:
            b"\xff".decode("utf8")
        except ValueError as unicode_caught:
            unicode_failure = failure_value(unicode_caught)
        self.assertEqual(unicode_failure.category, "UnicodeError")
        with self.assertRaises(UnboundLocalError):
            _ = unicode_caught

    def test_failure_is_deep_data_but_raw_exception_is_not(self):
        failure = failure_value(KeyError("hidden"))
        self.assertEqual(Some(Err(failure)).value.error, failure)
        self.assertIs(freeze(failure), failure)
        self.assertIs(validate_data(failure, _records._annotation_schema(Failure)), failure)
        with self.assertRaises(TypeError):
            Failure(True, "message")
        with self.assertRaises(AttributeError):
            failure.category = "changed"
        with self.assertRaises(TypeError):
            Some(KeyError("hidden"))
        self.assertEqual(replace(failure, message="new"), Failure("KeyError", "new"))


if __name__ == "__main__":
    unittest.main()
