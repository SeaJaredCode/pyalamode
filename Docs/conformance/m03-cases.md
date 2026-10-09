# Milestone 3 independent conformance corpus

Status: final frozen-code independent review complete; no remaining blocker observed in this bounded corpus. Authority: the full `SPEC-sol6.1-composite.md`, especially sections 8–9 and 16–18, inherited `Docs/milestones/02-modules.md`, and `Docs/conformance/acceptance-matrix.md` A11–A13/A32. This reviewer owns only this document; product implementation, tests, other documentation, suite acceptance and commits belong to other workers/orchestrator.

## Contract and scope

The approved increment uses an eager tuple-copy façade on the stock CPython foundation, with O(n) tuple-copy updates, O(n log n) sorted map/set construction, O(kn) retained-history storage, and separately accounted recursive validation costs. No external backend is used. Runtime type subscripting is erased annotation metadata. Ordinary constructors validate recursively immutable data and homogeneous scalar map-key/set-element domains; complete parameterized schemas are static caller/constructor obligations. Scalars are exact None/bool/int/str/bytes; bool and int are distinct domains. Callable data members, foreign protocols, generators, mutable exports, evolvers and builders remain excluded.

Unordered Map/Set use canonical order for explicit ordered results, runtime representation, and supported validation/error selection. Arbitrary unordered iteration, reducers and formatting hooks are excluded from strict source. OrderedMap insertion order participates in equivalence. Vector callbacks need actual checked evidence or a conditional pure Callable input obligation; annotation alone cannot promote an ordinary target. Conditional callback failures include the current characterized finite failure universe, with precise concrete-target failures retained where known.

The source corpus below has fixed expected admission statuses. Constructor/default/module analysis must never import or execute application source. Conservative exclusions are acceptable when explicitly published; false admission or erased failure/evidence is blocking. Published operation syntax will be reconciled before the final frozen run; discovered implementation bugs receive focused regression cases instead of open-ended corpus expansion.

## Fixed single-source corpus

The `source` values are literal text passed to the actual `checker.analyze_source` API, one independent file per case. Status 0 means admitted; status 1 means refused by strict verification. V19 specifically requires ValueError in invocation failures. C08 specifically requires ZeroDivisionError in `probe` failures. C07 requires the published conditional callable bound. No example source is evaluated.

```json
[
  {
    "id": "V01",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(1, 2)\n",
    "note": ""
  },
  {
    "id": "V02",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[int]:\n    return Vector[int].of()\n",
    "note": ""
  },
  {
    "id": "V03",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int], value: int) -> Vector[int]:\n    return values.appended(value)\n",
    "note": ""
  },
  {
    "id": "V04",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int], index: int, value: int) -> Vector[int]:\n    return values.updated_at(index, value)\n",
    "note": ""
  },
  {
    "id": "V05",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int], index: int) -> int:\n    return values[index]\n",
    "note": ""
  },
  {
    "id": "V06",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values[1:3]\n",
    "note": ""
  },
  {
    "id": "V07",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Vector[int], right: Vector[int]) -> Vector[int]:\n    return left.concat(right)\n",
    "note": ""
  },
  {
    "id": "V08",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Vector[int], right: Vector[int]) -> bool:\n    return left == right\n",
    "note": ""
  },
  {
    "id": "V09",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int]) -> int:\n    return len(values)\n",
    "note": ""
  },
  {
    "id": "V10",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[tuple[int, str]]:\n    return Vector.of((1, 'a'), (2, 'b'))\n",
    "note": ""
  },
  {
    "id": "V11",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[Vector[int]]:\n    return Vector.of(Vector.of(1), Vector.of(2))\n",
    "note": ""
  },
  {
    "id": "V12",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of([1])\n",
    "note": "Nested mutable member refused; source is not executed."
  },
  {
    "id": "V13",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[int]:\n    return Vector[int].of(True)\n",
    "note": ""
  },
  {
    "id": "V14",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(True)\n",
    "note": ""
  },
  {
    "id": "V15",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Vector[int], right: Vector[str]) -> Vector[int]:\n    return left.concat(right)\n",
    "note": ""
  },
  {
    "id": "V16",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(1, True)\n",
    "note": ""
  },
  {
    "id": "V17",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Vector[int], right: Vector[bool]) -> bool:\n    return left == right\n",
    "note": ""
  },
  {
    "id": "V18",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int]) -> int:\n    return values[True]\n",
    "note": ""
  },
  {
    "id": "V19",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values[::0]\n",
    "note": "Admitted characterized ValueError, rather than successful traversal."
  },
  {
    "id": "V20",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    values.appended(2)\n    return values\n",
    "note": "Discarded return-only update must diagnose."
  },
  {
    "id": "O01",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> OrderedMap[str, int]:\n    return OrderedMap.of(('b', 2), ('a', 1))\n",
    "note": ""
  },
  {
    "id": "O02",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> OrderedMap[str, int]:\n    return OrderedMap[str, int].of()\n",
    "note": ""
  },
  {
    "id": "O03",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int], key: str, value: int) -> OrderedMap[str, int]:\n    return values.updated(key, value)\n",
    "note": ""
  },
  {
    "id": "O04",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int], key: str) -> OrderedMap[str, int]:\n    return values.without(key)\n",
    "note": ""
  },
  {
    "id": "O05",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int], key: str) -> int:\n    return values[key]\n",
    "note": ""
  },
  {
    "id": "O06",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int], key: str, default: int) -> int:\n    return values.get(key, default)\n",
    "note": ""
  },
  {
    "id": "O07",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int], key: str) -> bool:\n    return values.contains(key)\n",
    "note": ""
  },
  {
    "id": "O08",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: OrderedMap[str, int], right: OrderedMap[str, int]) -> OrderedMap[str, int]:\n    return left.merge(right)\n",
    "note": ""
  },
  {
    "id": "O09",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> OrderedMap[int, int]:\n    return OrderedMap.of((1, 1), (True, 2))\n",
    "note": ""
  },
  {
    "id": "O10",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> OrderedMap[str, int]:\n    return OrderedMap.of(('a', [1]))\n",
    "note": ""
  },
  {
    "id": "O11",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[int, int]) -> int:\n    return values[True]\n",
    "note": ""
  },
  {
    "id": "O12",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int]) -> int:\n    return values.get('absent')\n",
    "note": ""
  },
  {
    "id": "O13",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: OrderedMap[str, int]) -> OrderedMap[str, int]:\n    return values.updated('a', [1])\n",
    "note": ""
  },
  {
    "id": "M01",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Map[str, int]:\n    return Map.of(('b', 2), ('a', 1))\n",
    "note": ""
  },
  {
    "id": "M02",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Map[str, int]:\n    return Map[str, int].of()\n",
    "note": ""
  },
  {
    "id": "M03",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int], key: str, value: int) -> Map[str, int]:\n    return values.updated(key, value)\n",
    "note": ""
  },
  {
    "id": "M04",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int], key: str) -> Map[str, int]:\n    return values.without(key)\n",
    "note": ""
  },
  {
    "id": "M05",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int], key: str) -> int:\n    return values[key]\n",
    "note": ""
  },
  {
    "id": "M06",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int], key: str, default: int) -> int:\n    return values.get(key, default)\n",
    "note": ""
  },
  {
    "id": "M07",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int], key: str) -> bool:\n    return values.contains(key)\n",
    "note": ""
  },
  {
    "id": "M08",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Map[str, int], right: Map[str, int]) -> Map[str, int]:\n    return left.merge(right)\n",
    "note": ""
  },
  {
    "id": "M09",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Map[int, int]:\n    return Map.of((1, 1), (True, 2))\n",
    "note": ""
  },
  {
    "id": "M10",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Map[str, int]:\n    return Map.of(('a', [1]))\n",
    "note": ""
  },
  {
    "id": "M11",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[int, int]) -> int:\n    return values[True]\n",
    "note": ""
  },
  {
    "id": "M12",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> int:\n    return values.get('absent')\n",
    "note": ""
  },
  {
    "id": "M13",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> Map[str, int]:\n    return values.updated('a', [1])\n",
    "note": ""
  },
  {
    "id": "M14",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> Vector[tuple[str, int]]:\n    return values.ordered_entries()\n",
    "note": ""
  },
  {
    "id": "M15",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> Vector[str]:\n    return values.ordered_keys()\n",
    "note": ""
  },
  {
    "id": "M16",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> Vector[int]:\n    return values.ordered_values()\n",
    "note": ""
  },
  {
    "id": "M17",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> Vector[int]:\n    return values.values()\n",
    "note": ""
  },
  {
    "id": "S01",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Set[int]:\n    return Set.of(2, 1, 2)\n",
    "note": ""
  },
  {
    "id": "S02",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Set[int]:\n    return Set[int].of()\n",
    "note": ""
  },
  {
    "id": "S03",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int], item: int) -> Set[int]:\n    return values.added(item)\n",
    "note": ""
  },
  {
    "id": "S04",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int], item: int) -> Set[int]:\n    return values.without(item)\n",
    "note": ""
  },
  {
    "id": "S05",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int], item: int) -> bool:\n    return values.contains(item)\n",
    "note": ""
  },
  {
    "id": "S06",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Set[int], right: Set[int]) -> Set[int]:\n    return left.union(right)\n",
    "note": ""
  },
  {
    "id": "S07",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Set[int], right: Set[int]) -> Set[int]:\n    return left.intersection(right)\n",
    "note": ""
  },
  {
    "id": "S08",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(left: Set[int], right: Set[int]) -> Set[int]:\n    return left.difference(right)\n",
    "note": ""
  },
  {
    "id": "S09",
    "expected": 0,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int]) -> Vector[int]:\n    return values.ordered_values()\n",
    "note": ""
  },
  {
    "id": "S10",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Set[int]:\n    return Set.of(1, True)\n",
    "note": ""
  },
  {
    "id": "S11",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe() -> Set[tuple[int, int]]:\n    return Set.of((1, 2))\n",
    "note": ""
  },
  {
    "id": "S12",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int]) -> Set[int]:\n    return values.added(True)\n",
    "note": ""
  },
  {
    "id": "S13",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int], other: Set[bool]) -> Set[int]:\n    return values.union(other)\n",
    "note": ""
  },
  {
    "id": "C01",
    "expected": 0,
    "source": "from pyalamode import fun, Vector\n@fun\ndef increment(value: int) -> int:\n    return value + 1\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.map(increment)\n",
    "note": ""
  },
  {
    "id": "C02",
    "expected": 0,
    "source": "from pyalamode import fun, Vector\n@fun\ndef positive(value: int) -> bool:\n    return value > 0\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.filter(positive)\n",
    "note": ""
  },
  {
    "id": "C03",
    "expected": 0,
    "source": "from pyalamode import fun, Vector\n@fun\ndef add(total: int, value: int) -> int:\n    return total + value\n@fun\ndef probe(values: Vector[int]) -> int:\n    return values.fold(add, 0)\n",
    "note": ""
  },
  {
    "id": "C04",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\ndef ordinary(value: int) -> int:\n    print(value)\n    return value\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.map(ordinary)\n",
    "note": ""
  },
  {
    "id": "C05",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef effectful(value: int) -> int:\n    print(value)\n    return value\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.map(effectful)\n",
    "note": ""
  },
  {
    "id": "C06",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef wrong(value: int) -> int:\n    return value\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.filter(wrong)\n",
    "note": ""
  },
  {
    "id": "C07",
    "expected": 0,
    "source": "from pyalamode import fun, Vector\nfrom typing import Callable\n@fun\ndef probe(values: Vector[int], cb: Callable[[int], int]) -> Vector[int]:\n    return values.map(cb)\n",
    "note": "Conditional pure invocation obligation with published finite failure bound."
  },
  {
    "id": "C08",
    "expected": 0,
    "source": "from pyalamode import fun, Vector\n@fun\ndef divide(value: int) -> int:\n    return 1 // value\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.map(divide)\n",
    "note": "Known callback ZeroDivisionError must propagate."
  },
  {
    "id": "C09",
    "expected": 0,
    "source": "from pyalamode import fun, Vector\n@fun\ndef factory(offset: int, values: Vector[int]) -> Vector[int]:\n    def adjusted(value: int) -> int:\n        return value + offset\n    return values.map(adjusted)\n",
    "note": ""
  },
  {
    "id": "C10",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef factory(offset: int, values: Vector[int]) -> Vector[int]:\n    def adjusted(value: int) -> int:\n        return value + offset\n    result = values.map(adjusted)\n    offset = 4\n    return result\n",
    "note": ""
  },
  {
    "id": "C11",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef divide(value: int) -> int:\n    return value\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(divide)\n",
    "note": ""
  },
  {
    "id": "D01",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> str:\n    return repr(values)\n",
    "note": ""
  },
  {
    "id": "D02",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> str:\n    return f'{values}'\n",
    "note": ""
  },
  {
    "id": "D03",
    "expected": 1,
    "source": "from pyalamode import fun, Set\n@fun\ndef probe(values: Set[int]) -> int:\n    if values:\n        return 1\n    return 0\n",
    "note": ""
  },
  {
    "id": "D04",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int]) -> int:\n    return hash(values)\n",
    "note": ""
  },
  {
    "id": "D05",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Set[int]) -> int:\n    return next(iter(values))\n",
    "note": ""
  },
  {
    "id": "D06",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Map[str, int]) -> Vector[int]:\n    return values.map(abs)\n",
    "note": ""
  },
  {
    "id": "D07",
    "expected": 1,
    "source": "from pyalamode import fun, Vector, OrderedMap, Map, Set\n@fun\ndef probe(values: Vector[int]) -> object:\n    return values.evolver()\n",
    "note": ""
  },
  {
    "id": "A01",
    "expected": 0,
    "source": "import pyalamode as p\nfrom pyalamode import Vector as V\n@p.fun\ndef probe(values: V[int]) -> V[int]:\n    return values.appended(2)\n",
    "note": ""
  },
  {
    "id": "A02",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\nVector = list\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(1)\n",
    "note": ""
  },
  {
    "id": "A03",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\nimport pyalamode\npyalamode.Vector = list\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(1)\n",
    "note": ""
  },
  {
    "id": "A04",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\nimport pyalamode\npyalamode.Vector.of = print\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(1)\n",
    "note": ""
  },
  {
    "id": "A05",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(2)\nVector.appended = print\n",
    "note": ""
  },
  {
    "id": "I01",
    "expected": 0,
    "source": "# mode: fun\nfrom pyalamode import Vector\nVALUES = Vector.of(1, 2)\ndef probe() -> Vector[int]:\n    return VALUES.appended(3)\n",
    "note": ""
  },
  {
    "id": "I02",
    "expected": 1,
    "source": "# mode: fun\nfrom pyalamode import Vector\nVALUES = Vector.of([1])\ndef probe() -> int:\n    return 1\n",
    "note": ""
  },
  {
    "id": "I03",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef probe(value: Vector[int] = Vector.of([1])) -> Vector[int]:\n    return value\n",
    "note": ""
  },
  {
    "id": "O14",
    "expected": 0,
    "source": "from pyalamode import fun, OrderedMap, Vector\n@fun\ndef probe(values: OrderedMap[str, int]) -> Vector[tuple[str, int]]:\n    return values.entries()\n",
    "note": ""
  },
  {
    "id": "O15",
    "expected": 0,
    "source": "from pyalamode import fun, OrderedMap, Vector\n@fun\ndef probe(values: OrderedMap[str, int]) -> Vector[str]:\n    return values.keys()\n",
    "note": ""
  },
  {
    "id": "O16",
    "expected": 0,
    "source": "from pyalamode import fun, OrderedMap, Vector\n@fun\ndef probe(values: OrderedMap[str, int]) -> Vector[int]:\n    return values.values()\n",
    "note": ""
  },
  {
    "id": "T01",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, str]) -> str:\n    return values[1]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T02",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, str]) -> int:\n    return values[-2]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T03",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, str]) -> tuple[str]:\n    return values[1:]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T04",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, ...], index: int) -> int:\n    return values[index]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T05",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, ...], step: int) -> tuple[int, ...]:\n    return values[::step]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T06",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(left: tuple[int, str], right: tuple[int, str]) -> bool:\n    return left == right\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T07",
    "expected": 1,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, str], index: int) -> int:\n    return values[index]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T08",
    "expected": 1,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, str]) -> int:\n    return values[True]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T09",
    "expected": 1,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(left: tuple[int], right: tuple[bool]) -> bool:\n    return left == right\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T10",
    "expected": 1,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(left: tuple[int], right: tuple[int]) -> bool:\n    return left < right\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T11",
    "expected": 1,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: tuple[int, str], stop: int) -> tuple[int]:\n    return values[:stop]\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T12",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: Map[str, int], key: str) -> bool:\n    return key in values\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T13",
    "expected": 0,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: Set[int], item: int) -> bool:\n    return item not in values\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "T14",
    "expected": 1,
    "source": "from pyalamode import fun, Map, Set\n@fun\ndef probe(values: Set[int]) -> bool:\n    return True in values\n",
    "note": "Bounded tuple/membership expansion confirmed by builder; exact dispatch and characterized failures."
  },
  {
    "id": "C12",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\ndef target(value: int) -> bool:\n    print(value)\n    return value > 0\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.filter(target)\n",
    "note": "A13 requires unknown/effectful target refusal for every admitted higher-order operation."
  },
  {
    "id": "C13",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef target(value: int) -> bool:\n    print(value)\n    return value > 0\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.filter(target)\n",
    "note": "A13 requires unknown/effectful target refusal for every admitted higher-order operation."
  },
  {
    "id": "C14",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\ndef target(total: int, value: int) -> int:\n    print(value)\n    return total + value\n@fun\ndef probe(values: Vector[int]) -> int:\n    return values.fold(target, 0)\n",
    "note": "A13 requires unknown/effectful target refusal for every admitted higher-order operation."
  },
  {
    "id": "C15",
    "expected": 1,
    "source": "from pyalamode import fun, Vector\n@fun\ndef target(total: int, value: int) -> int:\n    print(value)\n    return total + value\n@fun\ndef probe(values: Vector[int]) -> int:\n    return values.fold(target, 0)\n",
    "note": "A13 requires unknown/effectful target refusal for every admitted higher-order operation."
  }
]
```

## Runtime and project verification to execute

Retain old Vector, Map, OrderedMap and Set versions through append/replace/remove/merge/set algebra and compare all versions with independently expected contents. Exercise negative index, missing key, zero slice step, empty typed values, recursively nested values, and exact scalar domains. Unsupported members and user subclasses/hooks must fail before invoking hooks. Runtime callbacks execute as ordinary Python; their purity evidence is a static obligation, and no runtime purity claim is inferred from raw callback execution.

For unordered histories, compare independent insertion/replacement/removal histories, canonical result vectors and representation across at least three fixed process hash seeds; compare errors for ambiguous/unsupported homogeneous key domains. Verify OrderedMap history order remains distinguishable.

Project layouts will cover the actual installed façade, local product shadow, analyzed class/method/namespace replacements, writer additions after warm cache, source/policy/product freshness and backend identity inclusion. Actual check_paths/build_paths must preserve source bytes and reject invalid builds without publishing output. The no-execution sentinel must remain absent. Runtime tests directly invoke only the installed library, never import application fixture files.

## Observations

The following chronological records distinguish interim observations from final frozen results. Human usability remains unmeasured. Platform suite verification and update/retention measurements are orchestrator-owned.

## Fixed project corpus

Each JSON layout is written in a temporary directory and checked with `project.check_paths(root=root, cache=False)`. P01 additionally builds; every refusal additionally attempts a fresh output and verifies no output exists. P03–P05 are repeated as cold/warm positive baselines, then writer additions without caller edits, comparing cached and fresh gates. P08 has an application-file sentinel; the path remains absent after check/build. Each loaded source participates in the actual root resolution model.

```json
[
  {
    "id": "P01-installed-alias",
    "expected": 0,
    "files": {
      "leaf.py": "# mode: fun\nfrom pyalamode import Vector as V\ndef identity(values: V[int]) -> V[int]:\n    return values.appended(3)\n",
      "core.py": "# mode: fun\nfrom pyalamode import Vector\nfrom leaf import identity\ndef probe(values: Vector[int]) -> Vector[int]:\n    return identity(values)\n"
    }
  },
  {
    "id": "P02-product-shadow",
    "expected": 1,
    "files": {
      "pyalamode.py": "def fun(cb):\n    print(\"marker hook\")\n    return cb\nclass Vector:\n    def __class_getitem__(cls, value):\n        print(\"type hook\")\n        return cls\n",
      "core.py": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(1)\n"
    }
  },
  {
    "id": "P03-method-writer",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(1)\n",
      "writer.py": "from pyalamode import Vector\nVector.appended = print\n"
    }
  },
  {
    "id": "P04-nested-module-writer",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Map\n@fun\ndef probe(values: Map[str, int]) -> int:\n    return values[\"a\"]\n",
      "writer.py": "import pyalamode as p\np.Map.__getitem__ = print\n"
    }
  },
  {
    "id": "P05-constructor-writer",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Vector\n@fun\ndef probe() -> Vector[int]:\n    return Vector.of(1)\n",
      "writer.py": "from pyalamode import Vector as V\nV.of = print\n"
    }
  },
  {
    "id": "P06-key-subclass",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Map\nclass Key(str):\n    def __hash__(self):\n        print(\"hash hook\")\n        return 1\n@fun\ndef probe(values: Map[str, int]) -> int:\n    return values[\"a\"]\nprobe(Map.of((Key(\"a\"), 1)))\n"
    }
  },
  {
    "id": "P07-input-subclass",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Vector\nclass V(Vector):\n    def __getitem__(self, value):\n        print(\"getter hook\")\n        return 7\n@fun\ndef probe(values: Vector[int]) -> int:\n    return values[0]\nprobe(V.of(1))\n"
    }
  },
  {
    "id": "P08-nonexecution",
    "expected": 1,
    "files": {
      "core.py": "from pathlib import Path\nfrom pyalamode import fun, Vector\nPath(\"executed-sentinel\").write_text(\"executed\")\n@fun\ndef probe(values: Vector[int] = Vector.of([1])) -> Vector[int]:\n    return values\n"
    }
  },
  {
    "id": "P09-backend-validator",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(1)\n",
      "writer.py": "import pyalamode.collections as backend\nbackend._validate = print\n"
    }
  },
  {
    "id": "P10-backend-equality",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(1)\n",
      "writer.py": "import pyalamode.collections as backend\nbackend._Frozen.__eq__ = print\n"
    }
  },
  {
    "id": "P11-backend-constructor",
    "expected": 1,
    "files": {
      "core.py": "from pyalamode import fun, Vector\n@fun\ndef probe(values: Vector[int]) -> Vector[int]:\n    return values.appended(1)\n",
      "writer.py": "import pyalamode.collections as backend\nbackend._MapBase.of = print\n"
    }
  }
]
```

## Interim actual observations

On CPython 3.13.1 macOS arm64, the first syntactically stable static run matched all 110 fixed single-source expected statuses with no exceptions. Index/update lookup failures include IndexError, map lookup includes KeyError, slice includes ValueError, C07 conditional callback includes IndexError/KeyError/RecursionError/ValueError/ZeroDivisionError, and C08 concrete division callback propagates precise ZeroDivisionError. These are interim results, before a frozen implementation.

An actual runtime/static mismatch was reported promptly: T12/T13 map/set membership passed `analyze_source` with no failure but ordinary `"a" in Map.of(("a", 1))` and `1 in Set.of(1)` raised TypeError because the runtime supplied `contains` and rejected `__iter__` while omitting `__contains__`. The runtime helper is correcting membership; final retest remains required.

## Interim actual project/cache/build observations

The 11 fixed layouts were written only in temporary directories. Actual `check_paths(cache=False)` and fresh `build_paths` produced the recorded statuses; P01 copies unchanged source and includes `collections.py` in product identity. No application source was imported by this reviewer. The six writer layouts were also repeated with cold/warm positive baselines then writer-only additions, comparing cached/fresh refusal.

```json
{
  "layouts": [
    {
      "id": "P01-installed-alias",
      "expected": 0,
      "check": 0,
      "build": 0,
      "verified": true,
      "artifact_exists": true,
      "diagnostics": [],
      "sentinel_exists": false,
      "unchanged_sources": true,
      "backend_identity_included": true
    },
    {
      "id": "P02-product-shadow",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL120:only one unchanged pyalamode.fun identity declaration is supported",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires None; found unknown/unsupported value",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P03-method-writer",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires None; found unknown/unsupported value",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P04-nested-module-writer",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires int; found unknown/unsupported value",
        "core.py:PAL201:indexing requires an admitted exact Vector/map/tuple contract"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P05-constructor-writer",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires None; found unknown/unsupported value",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin",
        "core.py:PAL240:binding `Vector` is not a statically established stable dependency",
        "core.py:PAL240:binding `Vector` is not a statically established stable dependency"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P06-key-subclass",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL221:map of inputs must be exact fixed two-element key/value tuples",
        "core.py:PAL221:argument `values` of `probe` requires Map[str, int]; found unknown/unsupported value",
        "core.py:PAL221:tuple contents must be recursively admitted immutable data; callable/module objects are not tuple data",
        "core.py:PAL102:local `Key` is not initialized or shadows an approved operation",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P07-input-subclass",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL102:local `V` is not initialized or shadows an approved operation",
        "core.py:PAL102:local `V` is not initialized or shadows an approved operation",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL221:argument `values` of `probe` requires Vector[int]; found unknown/unsupported value",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P08-nonexecution",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL221:collection elements must establish one recursively admitted exact data schema; empty of requires explicit type arguments",
        "core.py:PAL221:default `values` does not establish Vector[int]",
        "core.py:PAL201:List is outside the scalar expression vocabulary"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P09-backend-validator",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL120:only one unchanged pyalamode.fun identity declaration is supported",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires None; found unknown/unsupported value",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P10-backend-equality",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL120:only one unchanged pyalamode.fun identity declaration is supported",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires None; found unknown/unsupported value",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    },
    {
      "id": "P11-backend-constructor",
      "expected": 1,
      "check": 1,
      "build": 1,
      "verified": false,
      "artifact_exists": false,
      "diagnostics": [
        "core.py:PAL120:only one unchanged pyalamode.fun identity declaration is supported",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL130:annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
        "core.py:PAL211:return requires None; found unknown/unsupported value",
        "core.py:PAL201:attribute access is admitted only for statically resolved module dependencies",
        "core.py:PAL230:call target is not a resolved checked callable or characterized builtin"
      ],
      "sentinel_exists": false
    }
  ],
  "warm_transitions": [
    {
      "id": "P03-method-writer",
      "cold": 0,
      "warm": 0,
      "baseline_hit": true,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P04-nested-module-writer",
      "cold": 0,
      "warm": 0,
      "baseline_hit": true,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P05-constructor-writer",
      "cold": 0,
      "warm": 0,
      "baseline_hit": true,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P09-backend-validator",
      "cold": 0,
      "warm": 0,
      "baseline_hit": true,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P10-backend-equality",
      "cold": 0,
      "warm": 0,
      "baseline_hit": true,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P11-backend-constructor",
      "cold": 0,
      "warm": 0,
      "baseline_hit": true,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    }
  ]
}
```

## Fixed ordinary-library runtime harness

This harness directly imports the installed product library. It does not import, evaluate or execute any application source fixture from the static/project corpus. Run it separately under fixed hash seeds 1, 2 and 8675309 with the supported interpreter. Python lists/dicts inside this ordinary harness are expected-value instrumentation, not admitted strict values. Runtime type arguments are erased, so the erasure assertions establish only deep-data/key-domain invariants.

```python
from itertools import permutations
import json
from pyalamode import Vector, Map, OrderedMap, Set

checks = 0
def require(value):
    global checks
    assert value
    checks += 1

def fails(kind, operation):
    global checks
    try:
        operation()
    except kind as error:
        checks += 1
        return str(error)
    raise AssertionError("expected " + kind.__name__)

v0 = Vector.of(1, 2)
v1 = v0.appended(3)
v2 = v1.updated_at(-2, 9)
v3 = v2.concat(Vector.of(4))
v4 = v3[1:3]
for actual, expected in [(v0, Vector.of(1, 2)), (v1, Vector.of(1, 2, 3)),
                         (v2, Vector.of(1, 9, 3)), (v3, Vector.of(1, 9, 3, 4)),
                         (v4, Vector.of(9, 3))]:
    require(actual == expected)
require(v0[-1] == 2)
require(v0.map(lambda x: x + 1) == Vector.of(2, 3))
require(v0.filter(lambda x: x > 1) == Vector.of(2))
require(v0.fold(lambda total, x: total + x, 0) == 3)
fails(IndexError, lambda: v0[2])
fails(IndexError, lambda: v0.updated_at(2, 9))
fails(ValueError, lambda: v0[::0])
require(v0 == Vector.of(1, 2))

canonical = []
for keys in [(None,), (True, False), (2, -1, 0), ("z", "a", "é"), (b"z", b"a", b"c")]:
    base = tuple((key, index + 1) for index, key in enumerate(keys))
    expected = Map.of(*base)
    expected_set = Set.of(*keys)
    for order in permutations(base):
        made = Map.of(*order)
        incremental = Map.of()
        for key, value in order:
            incremental = incremental.updated(key, value)
        rewritten = made.updated(base[0][0], 999).updated(*base[0]).without(base[-1][0]).updated(*base[-1])
        require(made == expected and incremental == expected and rewritten == expected)
        require(made.ordered_entries() == expected.ordered_entries())
        require(made.ordered_keys() == expected.ordered_keys())
        require(made.ordered_values() == expected.ordered_values())
        require(repr(made) == repr(expected))
        made_set = Set.of(*(key for key, _ in order))
        incremental_set = Set.of()
        for key, _ in order:
            incremental_set = incremental_set.added(key)
        rewritten_set = made_set.without(base[-1][0]).added(base[-1][0])
        require(made_set == expected_set and incremental_set == expected_set and rewritten_set == expected_set)
        require(made_set.ordered_values() == expected_set.ordered_values())
        require(repr(made_set) == repr(expected_set))
    canonical.append([repr(expected), repr(expected.ordered_entries()), repr(expected_set), repr(expected_set.ordered_values())])

m0 = Map.of(("b", 2), ("a", 1))
m1 = m0.updated("a", 9)
m2 = m1.updated("c", 3)
m3 = m2.without("b")
m4 = m3.merge(Map.of(("d", 4), ("a", 10)))
for actual, expected in [(m0, Map.of(("a", 1), ("b", 2))), (m1, Map.of(("a", 9), ("b", 2))),
                         (m2, Map.of(("a", 9), ("b", 2), ("c", 3))), (m3, Map.of(("a", 9), ("c", 3))),
                         (m4, Map.of(("a", 10), ("c", 3), ("d", 4)))]:
    require(actual == expected)
require(m0.get("absent", 7) == 7 and m0["a"] == 1 and m0.contains("a"))
require("a" in m0 and "absent" not in m0)
fails(KeyError, lambda: m0["absent"])

o0 = OrderedMap.of(("b", 2), ("a", 1))
o1 = o0.updated("b", 9)
o2 = o1.updated("c", 3)
o3 = o2.without("a")
o4 = o3.merge(OrderedMap.of(("d", 4), ("b", 10)))
for actual, expected in [(o0, OrderedMap.of(("b", 2), ("a", 1))), (o1, OrderedMap.of(("b", 9), ("a", 1))),
                         (o2, OrderedMap.of(("b", 9), ("a", 1), ("c", 3))), (o3, OrderedMap.of(("b", 9), ("c", 3))),
                         (o4, OrderedMap.of(("b", 10), ("c", 3), ("d", 4)))]:
    require(actual == expected)
require(o0 != OrderedMap.of(("a", 1), ("b", 2)))
require(o0.entries() == Vector.of(("b", 2), ("a", 1)))
require(o0.keys() == Vector.of("b", "a") and o0.values() == Vector.of(2, 1))
require("b" in o0 and "absent" not in o0)
require(OrderedMap.of(("b", 2), ("a", 1), ("b", 9)) == o1)

s0 = Set.of(2, 1)
s1 = s0.added(3)
s2 = s1.without(1)
s3 = s2.union(Set.of(4, 2))
s4 = s3.intersection(Set.of(2, 4, 5))
s5 = s4.difference(Set.of(2))
for actual, expected in [(s0, Set.of(1, 2)), (s1, Set.of(1, 2, 3)), (s2, Set.of(2, 3)),
                         (s3, Set.of(2, 3, 4)), (s4, Set.of(2, 4)), (s5, Set.of(4))]:
    require(actual == expected)
require(1 in s0 and 3 not in s0)

require(Vector.of((1,)) != Vector.of((True,)))
require(Map.of(("a", (1,))) != Map.of(("a", (True,))))
require(Set.of(1) != Set.of(True))
require(Map.of((1, "a")) != Map.of((True, "a")))
require(Vector[int].of(True) == Vector.of(True))
require(Map[int, int].of((True, "a")) == Map.of((True, "a")))
require(Set[int].of(True) == Set.of(True))

hits = []
class Hidden:
    def __iter__(self): hits.append("iter"); return iter(())
    def __eq__(self, other): hits.append("eq"); return False
    def __hash__(self): hits.append("hash"); return 1
    def __repr__(self): hits.append("repr"); return "hidden"
    def __bool__(self): hits.append("bool"); return True
    def __index__(self): hits.append("index"); return 0
    def __call__(self, *args): hits.append("call"); return 1
class ScalarSubclass(int):
    def __hash__(self): hits.append("subclass hash"); return 1
class TupleSubclass(tuple):
    def __iter__(self): hits.append("subclass iter"); return iter(())
hidden = Hidden()
for constructor in [lambda: Vector.of(hidden), lambda: Vector.of(([1],)),
                    lambda: Vector.of(ScalarSubclass(1)), lambda: Vector.of(TupleSubclass((1,))),
                    lambda: Map.of((hidden, 1)), lambda: Map.of((ScalarSubclass(1), 1)),
                    lambda: Map.of(("a", [1])), lambda: Set.of(hidden),
                    lambda: Set.of(1, True), lambda: Map.of((1, 1), (True, 2)),
                    lambda: v0.appended(hidden), lambda: v0.updated_at(0, hidden),
                    lambda: m0.updated("a", hidden), lambda: m0.get("a", hidden),
                    lambda: m0[hidden], lambda: s0.added(hidden), lambda: v0[hidden],
                    lambda: v0[slice(hidden, None)], lambda: v0.map(hidden),
                    lambda: v0.filter(lambda x: hidden), lambda: v0.map(lambda x: []),
                    lambda: v0.fold(lambda total, x: [], 0), lambda: Vector(hidden),
                    lambda: iter(m0), lambda: iter(s0)]:
    fails(TypeError, constructor)
require(hits == [])
for value in [v0, m0, o0, s0]:
    fails(AttributeError, lambda value=value: setattr(value, "new", 1))
    fails(AttributeError, lambda value=value: delattr(value, "new"))
    fails(AttributeError, lambda value=value: value.evolver())
    fails(AttributeError, lambda value=value: value.__init__())
    fails(TypeError, lambda value=value: hash(value))
errors = [fails(TypeError, lambda: Map.of(("b", []), ("a", {}))),
          fails(TypeError, lambda: Map.of(("a", {}), ("b", [])))]
require(errors[0] == errors[1] and 'a' in errors[0])
print(json.dumps({"checks": checks, "canonical": canonical, "errors": errors, "hook_hits": hits}, sort_keys=True, ensure_ascii=True))
```

## Interim actual runtime observations

The fixed harness was run as `[sys.executable, "-c", harness]` in three independent subprocesses with `PYTHONHASHSEED=1`, `2`, and `8675309`, using the installed product library only. Exact output identity and observation follow; runtime helper has announced code-only freeze but overall static/build freeze is still pending.

```json
{
  "seeds": [
    {
      "seed": "1",
      "status": 0,
      "stderr": "",
      "stdout_sha256": "65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942"
    },
    {
      "seed": "2",
      "status": 0,
      "stderr": "",
      "stdout_sha256": "65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942"
    },
    {
      "seed": "8675309",
      "status": 0,
      "stderr": "",
      "stdout_sha256": "65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942"
    }
  ],
  "identical_outputs": true,
  "sample": {
    "canonical": [
      [
        "Map.of((None, 1))",
        "Vector.of((None, 1))",
        "Set.of(None)",
        "Vector.of(None)"
      ],
      [
        "Map.of((False, 2), (True, 1))",
        "Vector.of((False, 2), (True, 1))",
        "Set.of(False, True)",
        "Vector.of(False, True)"
      ],
      [
        "Map.of((-1, 2), (0, 3), (2, 1))",
        "Vector.of((-1, 2), (0, 3), (2, 1))",
        "Set.of(-1, 0, 2)",
        "Vector.of(-1, 0, 2)"
      ],
      [
        "Map.of(('a', 2), ('z', 1), ('\u00e9', 3))",
        "Vector.of(('a', 2), ('z', 1), ('\u00e9', 3))",
        "Set.of('a', 'z', '\u00e9')",
        "Vector.of('a', 'z', '\u00e9')"
      ],
      [
        "Map.of((b'a', 2), (b'c', 3), (b'z', 1))",
        "Vector.of((b'a', 2), (b'c', 3), (b'z', 1))",
        "Set.of(b'a', b'c', b'z')",
        "Vector.of(b'a', b'c', b'z')"
      ]
    ],
    "checks": 262,
    "errors": [
      "entries['a'].value: expected exact recursively immutable data",
      "entries['a'].value: expected exact recursively immutable data"
    ],
    "hook_hits": []
  }
}
```

## Actual isolated backend-byte freshness probe

The installed product package was copied to a temporary runtime directory, excluding bytecode, without changing the workspace. Subprocesses used `[sys.executable, "-c", harness, app_root, mode]`, that runtime as cwd and its path as PYTHONPATH. The copied product path in every record confirms actual dependency selection. A harmless newline was appended only to the copied `collections.py`; actual product digests/fingerprints changed and warm body evidence was discarded. An explicit admitted policy edit also invalidated cache. Successful build records the copied backend digest and unchanged app bytes. Corrupt/deleted caches preserve invalid-source refusal and a later failed build preserves the prior artifact. Application fixture source was never imported.

```json
[
  {
    "backend_digest": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
    "fingerprints": [
      "3cb8b897fd99d9869a3f45d9efabb0b6b433289fe297064aedb1cb511d045621"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "cold"
  },
  {
    "backend_digest": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
    "fingerprints": [
      "3cb8b897fd99d9869a3f45d9efabb0b6b433289fe297064aedb1cb511d045621"
    ],
    "hit": [
      true
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "unchanged warm"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "36471902599fe92c936f1e2b4fd3b8012b10e0165c99291ee85ae04524bb17a1"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "copied backend byte edit"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "36471902599fe92c936f1e2b4fd3b8012b10e0165c99291ee85ae04524bb17a1"
    ],
    "hit": [
      true
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "edited backend unchanged warm"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "bceaf90c61af98153ef609b98444a8bef9cc4aaa6d0efbcdebc40522cf909b0e"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "policy edit"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "bceaf90c61af98153ef609b98444a8bef9cc4aaa6d0efbcdebc40522cf909b0e"
    ],
    "hit": [
      false
    ],
    "output": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/app/artifact",
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "fresh build"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "f861887120f6843a31cc00831d8e78e8caf168076118368a1598420ead7e4fcd",
      "79fe76c29dab17861ca0686ed8bfa3e8fabdafa539805441072588219a8e9e26"
    ],
    "hit": [
      false,
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "invalid source"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "f861887120f6843a31cc00831d8e78e8caf168076118368a1598420ead7e4fcd",
      "79fe76c29dab17861ca0686ed8bfa3e8fabdafa539805441072588219a8e9e26"
    ],
    "hit": [
      false,
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "corrupted cache invalid source"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "f861887120f6843a31cc00831d8e78e8caf168076118368a1598420ead7e4fcd",
      "79fe76c29dab17861ca0686ed8bfa3e8fabdafa539805441072588219a8e9e26"
    ],
    "hit": [
      false,
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "deleted cache invalid source"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "f861887120f6843a31cc00831d8e78e8caf168076118368a1598420ead7e4fcd",
      "79fe76c29dab17861ca0686ed8bfa3e8fabdafa539805441072588219a8e9e26"
    ],
    "hit": [
      false,
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-review-backend-_u44ucb6/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "invalid fresh build"
  }
]
```

## Final frozen-code verification

**No remaining false admission, checker exception, runtime invariant failure or cache-dependent admission was observed in this bounded corpus.** The membership mismatch above was corrected and retested. The complete 110 fixed source cases, 11 actual project check/build layouts, six warm writer additions, and three focused nested-library failure regressions were run after the combined product freeze. Source snapshots stayed unchanged throughout. Runtime bytes match the earlier code-frozen three-seed harness, so its 262 assertions per process and identical output remain current. The library validation/equivalence recursion bound is conditional and separate from application call-graph recursion; scalar-only known callbacks retain precise failures.

This review covers A11–A13 and the finite A32 expansion, with source/build freshness inherited from A10. Unsupported general traversal, protocols, arbitrary callback objects, mutable data, evolvers and uncharacterized formatting remain excluded. Ordinary erased generic constructors claim closed deep values and scalar key/element invariants, while complete generic/callback/capture schemas remain statically established caller obligations. The review never imported application fixtures. Platform full-suite acceptance, benchmarks and commit remain orchestrator-owned; human usability is unmeasured.

```json
{
  "runtime": "3.13.1",
  "platform": "macOS-26.6.2-arm64-arm-64bit-Mach-O",
  "product_artifacts": {
    "__init__.py": "fd407d17688f88f3f1db79588d995e1432ab0955745dc70edf6480413860cc93",
    "collections.py": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
    "model.py": "9d7e92eeb524981766561cfa61e462b7c7e8dd72fe5a0b6e0345056179076b34",
    "checker.py": "bbfab32f08ec51de36902d5651cbf374bc26d6d1e2456c3b6178e5e333f88bff",
    "project.py": "b983e1ce25bd99ddb97fce4ddffe20f571c2eb70af01aa17ea41709fd0ac8d41",
    "cli.py": "f7992e4c7ab15eb86f72d24239df9ee6b5e7419c051ddeefa68827d2494b2297"
  },
  "snapshot_unchanged": true,
  "source_cases": 110,
  "source_statuses": {
    "V01": 0,
    "V02": 0,
    "V03": 0,
    "V04": 0,
    "V05": 0,
    "V06": 0,
    "V07": 0,
    "V08": 0,
    "V09": 0,
    "V10": 0,
    "V11": 0,
    "V12": 1,
    "V13": 1,
    "V14": 1,
    "V15": 1,
    "V16": 1,
    "V17": 1,
    "V18": 1,
    "V19": 0,
    "V20": 1,
    "O01": 0,
    "O02": 0,
    "O03": 0,
    "O04": 0,
    "O05": 0,
    "O06": 0,
    "O07": 0,
    "O08": 0,
    "O09": 1,
    "O10": 1,
    "O11": 1,
    "O12": 1,
    "O13": 1,
    "M01": 0,
    "M02": 0,
    "M03": 0,
    "M04": 0,
    "M05": 0,
    "M06": 0,
    "M07": 0,
    "M08": 0,
    "M09": 1,
    "M10": 1,
    "M11": 1,
    "M12": 1,
    "M13": 1,
    "M14": 0,
    "M15": 0,
    "M16": 0,
    "M17": 1,
    "S01": 0,
    "S02": 0,
    "S03": 0,
    "S04": 0,
    "S05": 0,
    "S06": 0,
    "S07": 0,
    "S08": 0,
    "S09": 0,
    "S10": 1,
    "S11": 1,
    "S12": 1,
    "S13": 1,
    "C01": 0,
    "C02": 0,
    "C03": 0,
    "C04": 1,
    "C05": 1,
    "C06": 1,
    "C07": 0,
    "C08": 0,
    "C09": 0,
    "C10": 1,
    "C11": 1,
    "D01": 1,
    "D02": 1,
    "D03": 1,
    "D04": 1,
    "D05": 1,
    "D06": 1,
    "D07": 1,
    "A01": 0,
    "A02": 1,
    "A03": 1,
    "A04": 1,
    "A05": 1,
    "I01": 0,
    "I02": 1,
    "I03": 1,
    "O14": 0,
    "O15": 0,
    "O16": 0,
    "T01": 0,
    "T02": 0,
    "T03": 0,
    "T04": 0,
    "T05": 0,
    "T06": 0,
    "T07": 1,
    "T08": 1,
    "T09": 1,
    "T10": 1,
    "T11": 1,
    "T12": 0,
    "T13": 0,
    "T14": 1,
    "C12": 1,
    "C13": 1,
    "C14": 1,
    "C15": 1
  },
  "source_mismatches": 0,
  "source_exceptions": 0,
  "required_failures": {
    "V04": [
      "IndexError"
    ],
    "V05": [
      "IndexError"
    ],
    "V10": [
      "RecursionError"
    ],
    "V11": [
      "RecursionError"
    ],
    "V19": [
      "ValueError"
    ],
    "M05": [
      "KeyError"
    ],
    "C07": [
      "IndexError",
      "KeyError",
      "RecursionError",
      "ValueError",
      "ZeroDivisionError"
    ],
    "C08": [
      "ZeroDivisionError"
    ],
    "T04": [
      "IndexError"
    ],
    "T05": [
      "ValueError"
    ]
  },
  "focused_regressions": [
    {
      "id": "R01-nested-equality",
      "source": "from pyalamode import fun, Vector\n@fun\ndef probe(left: Vector[tuple[int]], right: Vector[tuple[int]]) -> bool:\n    return left == right\n",
      "required": [
        "RecursionError"
      ],
      "status": 0,
      "failures": {
        "probe": [
          "RecursionError"
        ]
      }
    },
    {
      "id": "R02-nested-map-result",
      "source": "from pyalamode import fun, Vector\n@fun\ndef wrap(value: int) -> tuple[int]:\n    return (value,)\n@fun\ndef probe(values: Vector[int]) -> Vector[tuple[int]]:\n    return values.map(wrap)\n",
      "required": [
        "RecursionError"
      ],
      "status": 0,
      "failures": {
        "wrap": [],
        "probe": [
          "RecursionError"
        ]
      }
    },
    {
      "id": "R03-nested-fold-accumulator",
      "source": "from pyalamode import fun, Vector\n@fun\ndef add(total: tuple[int], value: int) -> tuple[int]:\n    return (total[0] + value,)\n@fun\ndef probe(values: Vector[int]) -> tuple[int]:\n    return values.fold(add, (0,))\n",
      "required": [
        "IndexError",
        "RecursionError"
      ],
      "status": 0,
      "failures": {
        "add": [
          "IndexError"
        ],
        "probe": [
          "IndexError",
          "RecursionError"
        ]
      }
    }
  ],
  "project_layouts": [
    {
      "id": "P01-installed-alias",
      "check": 0,
      "build": 0,
      "artifact_exists": true,
      "unchanged_sources": true,
      "backend_identity_included": true
    },
    {
      "id": "P02-product-shadow",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P03-method-writer",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P04-nested-module-writer",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P05-constructor-writer",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P06-key-subclass",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P07-input-subclass",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P08-nonexecution",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P09-backend-validator",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P10-backend-equality",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    },
    {
      "id": "P11-backend-constructor",
      "check": 1,
      "build": 1,
      "artifact_exists": false
    }
  ],
  "warm_transitions": [
    {
      "id": "P03-method-writer",
      "cold": 0,
      "warm": 0,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P04-nested-module-writer",
      "cold": 0,
      "warm": 0,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P05-constructor-writer",
      "cold": 0,
      "warm": 0,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P09-backend-validator",
      "cold": 0,
      "warm": 0,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P10-backend-equality",
      "cold": 0,
      "warm": 0,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    },
    {
      "id": "P11-backend-constructor",
      "cold": 0,
      "warm": 0,
      "changed_cached": 1,
      "changed_fresh": 1,
      "affected_core_hit": false
    }
  ],
  "runtime_unchanged_since_seeded_harness": true
}
```

## Final backend freshness rerun and artifact handoff

The isolated backend-byte probe was rerun after the combined product freeze, selecting only `core.py` and keeping build outputs outside the app root. The copied runtime backend byte edit and explicit admitted policy edit each changed fingerprints and discarded warm evidence. Build recorded actual copied backend bytes, retained unchanged app source, and invalid/corrupt/deleted-cache checks all refused. The failed fresh build published no new output and preserved the prior artifact. Original workspace product digests stayed unchanged. The exact command remains the subprocess harness described above; results follow.

```json
[
  {
    "backend_digest": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
    "fingerprints": [
      "33b70bbccf62574b714f454366a4d7b93b62a7eb6d2aafd0a578cdea7042c8bc"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "cold"
  },
  {
    "backend_digest": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
    "fingerprints": [
      "33b70bbccf62574b714f454366a4d7b93b62a7eb6d2aafd0a578cdea7042c8bc"
    ],
    "hit": [
      true
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "warm"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "af4810db7a4f8625885e77d6b4533dede99c33da285c4c3dc35e700ef6ba6dc1"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "backend byte edit"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "8d6d6fa58ad66eabab319a363fd0562f2563571b4877e43971a0426b727f6638"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "policy edit"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "8d6d6fa58ad66eabab319a363fd0562f2563571b4877e43971a0426b727f6638"
    ],
    "hit": [
      false
    ],
    "output": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/artifact",
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 0,
    "label": "fresh build"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "2bf1a0b6ad64b8f7f5a58d579f02ba7a61f0031e3e138710643645c5cc75d113"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "invalid source"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "2bf1a0b6ad64b8f7f5a58d579f02ba7a61f0031e3e138710643645c5cc75d113"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "corrupt cache"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "2bf1a0b6ad64b8f7f5a58d579f02ba7a61f0031e3e138710643645c5cc75d113"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "deleted cache"
  },
  {
    "backend_digest": "918dd50be312174456b7159af59c1be9d2c1d7b931192ecb262e0acb1879ca6f",
    "fingerprints": [
      "2bf1a0b6ad64b8f7f5a58d579f02ba7a61f0031e3e138710643645c5cc75d113"
    ],
    "hit": [
      false
    ],
    "output": null,
    "product_path": "/private/var/folders/lg/b9_9bvlj6294bgy95w857xlr0000gp/T/m03-final-backend-qfzsts9z/runtime/pyalamode/__init__.py",
    "status": 1,
    "label": "invalid fresh build"
  }
]
```

Final handoff: this reviewer changed only `Docs/conformance/m03-cases.md`. Product implementation/tests/examples/other documentation remained read-only. No commits, schedules, external project writes or thread operations were performed. No additional review work remains against the frozen bounded corpus.

## Renewed final artifact after diagnostic-text correction

After the preceding frozen runs, the builder corrected exactly four `model.py` remediation strings (PAL130/PAL201/PAL211/PAL221) to describe recursive admitted data, product collections and checked callable/capture contracts. Independent comparison against the staged prior M3 model, whose SHA-256 matches the prior frozen record, confirms these exact string replacements account for the entire change. Checker, runtime, schema, test and example behavior stayed unchanged; all other product artifact digests are identical. The earlier corpus results and digests above are retained as historical observations rather than relabeled as runs on the new bytes.

On the renewed freeze, the reviewer independently reran representative collection input (V13), annotation (S11), expression (D02) and return (V15) diagnostics. All retain strict refusal status 1 and now display the corrected actionable remediation below. The full 113-case corpus and runtime harness were not repeated because the verified diff changes only text. The orchestrator separately reports the renewed 90-test suite passing on both supported targets; those suite results remain orchestrator-owned. No new blocker was observed. The following digests supersede the previous product artifact table for the final delivered snapshot.

```json
{
  "previous_model_sha256": "9d7e92eeb524981766561cfa61e462b7c7e8dd72fe5a0b6e0345056179076b34",
  "renewed_model_sha256": "6f0cbbc5837c3054f65bb1c3b8d4f6b0c5ce85a39506037790fdcc3af65fa184",
  "only_model_changes": "four exact PAL130/PAL201/PAL211/PAL221 remediation strings",
  "other_product_bytes_unchanged": true,
  "product_artifacts": {
    "__init__.py": "fd407d17688f88f3f1db79588d995e1432ab0955745dc70edf6480413860cc93",
    "collections.py": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
    "model.py": "6f0cbbc5837c3054f65bb1c3b8d4f6b0c5ce85a39506037790fdcc3af65fa184",
    "checker.py": "bbfab32f08ec51de36902d5651cbf374bc26d6d1e2456c3b6178e5e333f88bff",
    "project.py": "b983e1ce25bd99ddb97fce4ddffe20f571c2eb70af01aa17ea41709fd0ac8d41",
    "cli.py": "f7992e4c7ab15eb86f72d24239df9ee6b5e7419c051ddeefa68827d2494b2297"
  },
  "representative_diagnostics": [
    {
      "id": "V13",
      "status": 1,
      "rule": "PAL221",
      "diagnostics": [
        {
          "reason": "collection elements must establish one recursively admitted exact data schema; empty of requires explicit type arguments",
          "remediation": "Supply values with established recursively exact data schemas and actual checked callable/capture evidence; ordinary unknown inputs remain caller obligations.",
          "line": 4,
          "boundary": "probe"
        }
      ]
    },
    {
      "id": "S11",
      "status": 1,
      "rule": "PAL130",
      "diagnostics": [
        {
          "reason": "annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars",
          "remediation": "Use explicit exact scalars, recursive tuple/product collection types, or fixed Callable contracts; Map keys and Set elements require exact scalar domains. Annotation expressions are never evaluated.",
          "line": 3,
          "boundary": "probe"
        }
      ]
    },
    {
      "id": "D02",
      "status": 1,
      "rule": "PAL201",
      "diagnostics": [
        {
          "reason": "JoinedStr is outside the scalar expression vocabulary",
          "remediation": "Use the published exact scalar, tuple, collection and checked callable expression contracts; move uncharacterized integration to ordinary Python.",
          "line": 4,
          "boundary": "probe"
        }
      ]
    },
    {
      "id": "V15",
      "status": 1,
      "rule": "PAL211",
      "diagnostics": [
        {
          "reason": "return requires Vector[int]; found unknown/unsupported value",
          "remediation": "Return the declared recursively exact admitted data or checked callable contract on every completing path.",
          "line": 4,
          "boundary": "probe"
        }
      ]
    }
  ]
}
```

## Large integer diagnostic-path correction

A subsequent concrete runtime defect reopened only the two internal diagnostic key-path sites. An exact integer key `10**5000` is in the unrestricted admitted integer domain, but eagerly formatting it in decimal previously added ValueError to otherwise admitted map construction and nested map validation at the default CPython 4,300 digit limit. This reviewer reproduced all three known failures using a temporary copy of the current product package with only `collections.py` replaced by the staged prior backend bytes. The actual static `make(key: int)` constructor remained admitted with no invocation failures, confirming the mismatch. No application fixture was executed.

The runtime correction adds `_path_key` with deterministic exact-int hex fallback on decimal representation ValueError and uses it only at both diagnostic value-path sites. Public `_data_repr` and public representation behavior remain unchanged and excluded from strict source. Source diff inspection confirmed this exact scope. Focused direct-library probes cover positive/negative huge-key construction, nested Vector validation/transforms/fold, retained map versions, merge/get, canonical deterministic invalid paths, ordinary small-key paths, subclass/unknown hooks and unchanged public representation failure. The records below precede any separately approved subsequent checker correction.

```json
{
  "historical_backend_sha256": "a5dbc2850e67165c22fdb1f4a7cfcad11987eee6323ad3b46078a7866df67c73",
  "historical_reproduction": {
    "int_max_str_digits": 4300,
    "runtime": [
      {
        "exception": "ValueError",
        "message": "Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit",
        "operation": "Map.of"
      },
      {
        "exception": "ValueError",
        "message": "Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit",
        "operation": "OrderedMap.of"
      },
      {
        "exception": "ValueError",
        "message": "Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit",
        "operation": "nested Vector.of"
      }
    ],
    "static_failures": {
      "make": []
    },
    "static_status": 0
  },
  "corrected_backend_sha256": "c0a4738ae85c1048b44c160a19f2d425c2872a5b601dcd352989903ad4102ab6",
  "focused_assertions": 43,
  "int_max_str_digits": 4300,
  "invalid_paths": [
    {
      "class": "Map",
      "sign": 1,
      "path_hex_matches": true,
      "message_sha256": "7f709f36cdecbe4ba71d7b447400bbe326576f13ba0a0e26fe0a23260a9a91cb",
      "message_length": 4216
    },
    {
      "class": "Map",
      "sign": -1,
      "path_hex_matches": true,
      "message_sha256": "24607d9a1ba240d713acbffc38ff74b359c9a61b40aa4ba881f9aebb6c822f92",
      "message_length": 4217
    },
    {
      "class": "OrderedMap",
      "sign": 1,
      "path_hex_matches": true,
      "message_sha256": "7f709f36cdecbe4ba71d7b447400bbe326576f13ba0a0e26fe0a23260a9a91cb",
      "message_length": 4216
    },
    {
      "class": "OrderedMap",
      "sign": -1,
      "path_hex_matches": true,
      "message_sha256": "24607d9a1ba240d713acbffc38ff74b359c9a61b40aa4ba881f9aebb6c822f92",
      "message_length": 4217
    }
  ],
  "hook_hits": [],
  "static_status": 0,
  "static_failures": [],
  "other_product_bytes_unchanged": true
}
```

## Final backend-foundation dependency correction

The final narrow checker correction inventories the actual explicit/implicit builtin and `types` dependencies read by the collection backend, including its initialization. Analyzed writes to these identities now invalidate collection contracts and their warm keys. This does not admit application calls to those builtins or add a live runtime namespace monitor. Unrelated scalar source keeps its own gate and cache evidence. Independent diff inspection verified that replacement/setter collection stays within the per-AST-node traversal, then dependency inventory expansion precedes signatures and participates in collection cache context.

After the renewed combined freeze, eight fixed actual writer layouts below exercised direct repr, an aliased hex route, type namespace writes, exception and constructor identities, and FunctionType replacement. Each cold/warm baseline passed; each writer-only addition made both cached/fresh collection gates and build refuse, removed the affected hit and retained the unrelated scalar identity hit/fingerprint. A focused inherited callable-setter layout also still refused. Because checker gating changed, all 110 fixed source cases and the three existing nested-failure regressions were repeated at expected results. Because runtime bytes changed, the fixed 262-assertion harness was repeated in all three seeds with identical output. No application source fixture was executed.

**No remaining blocker was observed in this final bounded review.** The prior final tables are historical snapshots. The following product digests identify the renewed delivered snapshot, superseding earlier tables; the large-int focused results above remain current because runtime bytes match. Full platform suites and final measurements remain orchestrator-owned.

```json
{
  "product_artifacts": {
    "__init__.py": "fd407d17688f88f3f1db79588d995e1432ab0955745dc70edf6480413860cc93",
    "collections.py": "c0a4738ae85c1048b44c160a19f2d425c2872a5b601dcd352989903ad4102ab6",
    "model.py": "6f0cbbc5837c3054f65bb1c3b8d4f6b0c5ce85a39506037790fdcc3af65fa184",
    "checker.py": "7791b1ae028218413af16d02f956bb434f6cb8e7b073d4369ad6ba1b83683539",
    "project.py": "b983e1ce25bd99ddb97fce4ddffe20f571c2eb70af01aa17ea41709fd0ac8d41",
    "cli.py": "f7992e4c7ab15eb86f72d24239df9ee6b5e7419c051ddeefa68827d2494b2297"
  },
  "snapshot_unchanged": true,
  "core_source": "from pyalamode import fun, Map\n@fun\ndef make(key: int) -> Map[int,int]:\n    return Map.of((key,1))\n",
  "unrelated_scalar_source": "from pyalamode import fun\n@fun\ndef identity(value: str) -> str:\n    return value\n",
  "foundation_writer_cases": [
    {
      "id": "F01-repr",
      "writer_source": "import builtins\nbuiltins.repr = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.repr.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F02-hex-alias",
      "writer_source": "import builtins as b\nalias = b\nalias.hex = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.hex.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F03-type-namespace",
      "writer_source": "import builtins\nbuiltins.__dict__[\"type\"] = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.type.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F04-ValueError",
      "writer_source": "import builtins\nbuiltins.ValueError = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.ValueError.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F05-TypeError",
      "writer_source": "import builtins\nbuiltins.TypeError = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.TypeError.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F06-tuple",
      "writer_source": "import builtins\nbuiltins.tuple = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.tuple.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F07-object",
      "writer_source": "import builtins\nbuiltins.object = print\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "builtins.object.<collection dependency>",
        "pyalamode.Map.<behavior>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    },
    {
      "id": "F08-FunctionType",
      "writer_source": "import types as t\nt.FunctionType = object\n",
      "cold_status": 0,
      "warm_status": 0,
      "changed_cached_status": 1,
      "changed_fresh_status": 1,
      "build_status": 1,
      "affected_core_hit": false,
      "scalar_status": 0,
      "scalar_hit": true,
      "scalar_fingerprint_unchanged": true,
      "binding_context": [
        "pyalamode.Map.<behavior>",
        "types.FunctionType.<collection dependency>"
      ],
      "rules": [
        "PAL130",
        "PAL201",
        "PAL211",
        "PAL230",
        "PAL240"
      ]
    }
  ],
  "inherited_setter_regression": {
    "status": 1,
    "leaf_status": 1
  },
  "fixed_source_cases_repeated": 113,
  "source_mismatches": 0,
  "source_exceptions": 0,
  "seeded_runtime_harness_repeated": [
    {
      "seed": "1",
      "status": 0,
      "assertions": 262,
      "stdout_sha256": "65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942"
    },
    {
      "seed": "2",
      "status": 0,
      "assertions": 262,
      "stdout_sha256": "65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942"
    },
    {
      "seed": "8675309",
      "status": 0,
      "assertions": 262,
      "stdout_sha256": "65c9e10d933f9bcd7274d2b17119fd0f98dfc08faffc26014fac27ce09dcc942"
    }
  ]
}
```
