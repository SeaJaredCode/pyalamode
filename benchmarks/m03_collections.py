"""Named tuple-backend construction/update/retained-history measurements.

Run with the published CPython 3.13.1 target. Imports, generated inputs, base
construction for update conditions, correctness checks, and JSON writing are
outside measured intervals. tracemalloc overhead is included; peaks are Python
allocations rather than process RSS. No universal latency claim is made.
"""

import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import sysconfig
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pyalamode.collections import Map, OrderedMap, Set, Vector
from pyalamode.model import foundation_identities

CLASSES = (Vector, OrderedMap, Map, Set)


def environment():
    cpu = platform.processor()
    hardware = {}
    if sys.platform == 'darwin':
        process = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], capture_output=True, text=True)
        if process.returncode == 0:
            cpu = process.stdout.strip()
        for name, key in [('hw.model', 'hardware_model'), ('hw.memsize', 'physical_memory_bytes')]:
            result = subprocess.run(['sysctl', '-n', name], capture_output=True, text=True)
            if result.returncode == 0:
                hardware[key] = int(result.stdout.strip()) if name == 'hw.memsize' else result.stdout.strip()
    elif Path('/proc/cpuinfo').exists():
        lines = Path('/proc/cpuinfo').read_text().splitlines()
        cpu = next((line.split(':', 1)[1].strip() for line in lines if line.startswith(('model name', 'Hardware'))), cpu)
        memory = Path('/proc/meminfo')
        if memory.exists():
            total = next((line.split()[1] for line in memory.read_text().splitlines() if line.startswith('MemTotal:')), None)
            hardware['visible_memory_bytes'] = int(total) * 1024 if total else None
        hardware['cgroup_limits'] = {path: Path(path).read_text().strip() for path in
                                    ('/sys/fs/cgroup/memory.max', '/sys/fs/cgroup/cpu.max') if Path(path).exists()}
    return {
        'implementation': platform.python_implementation(), 'python': platform.python_version(),
        'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(),
        'executable': sys.executable, 'platform': platform.platform(), 'machine': platform.machine(),
        'cpu': cpu, 'logical_cpus': os.cpu_count(), 'free_threaded': bool(sysconfig.get_config_var('Py_GIL_DISABLED')),
        **hardware,
    }


def source_snapshot():
    paths = ('pyalamode/collections.py', 'tests/m03_runtime.py', 'benchmarks/m03_collections.py')
    return {'owned_sources': {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
            'product_artifacts': foundation_identities()}


def target_gate():
    if platform.python_implementation() != 'CPython' or tuple(sys.version_info[:3]) != (3, 13, 1):
        raise SystemExit('benchmark requires CPython 3.13.1')
    if sys.platform not in {'darwin', 'linux'} or sysconfig.get_config_var('Py_GIL_DISABLED'):
        raise SystemExit('benchmark requires a standard GIL build on macOS/Linux')


def _construct(cls, values, pairs):
    return cls.of(*pairs) if cls in (Map, OrderedMap) else cls.of(*values)


def _revision(cls, value, size, step):
    index = (step * 379) % size
    if cls is Vector:
        return value.updated_at(index, size + step)
    if cls in (Map, OrderedMap):
        return value.updated(index, size + step)
    # Maintain size n while exercising two copying operations rather than reuse.
    return value.without(index).added(size + step)


def _revisions(cls, base, size, updates, retain):
    current = base
    versions = [base] if retain else None
    for step in range(updates):
        current = _revision(cls, current, size, step)
        if retain:
            versions.append(current)
    return versions if retain else [base, current]


def _verify_constructor(cls, value, size, values):
    assert type(value) is cls and len(value) == size
    if cls is Vector:
        assert value[0] == values[0] and value[-1] == values[-1]
    elif cls is Set:
        assert value.ordered_values() == Vector.of(*range(size))
    else:
        assert value[0] == 0 and value[size - 1] == size - 1
        if cls is Map:
            assert value.ordered_keys() == Vector.of(*range(size))
        else:
            assert value.keys() == Vector.of(*values)


def _verify_versions(cls, versions, size, updates, retain):
    assert len(versions) == updates + 1 if retain else len(versions) == 2
    assert all(type(value) is cls and len(value) == size for value in versions)
    # Probe every retained revision and every revised cell/member. Verification
    # is outside timing/allocation measurement and checks retained semantics.
    for revision, value in enumerate(versions):
        completed = revision if retain else (0 if revision == 0 else updates)
        for step in range(updates):
            index = (step * 379) % size
            if cls is Set:
                assert value.contains(size + step) is (step < completed)
                assert value.contains(index) is (step >= completed)
            else:
                expected = size + step if step < completed else index
                assert value[index] == expected


def _measure(function):
    gc.collect()
    tracemalloc.start()
    started = time.perf_counter()
    result = function()
    elapsed = time.perf_counter() - started
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, {'elapsed_seconds': elapsed, 'traced_current_bytes': current, 'traced_peak_bytes': peak}


def benchmark(sizes, trials, updates):
    before = source_snapshot()
    rows = []
    for size in sizes:
        if updates > size or len({(step * 379) % size for step in range(updates)}) != updates:
            raise ValueError('workload requires distinct revision indices; lower --updates or choose other sizes')
        values = list(range(size))
        random.Random(17).shuffle(values)
        values = tuple(values)
        pairs = tuple((value, value) for value in values)
        for cls in CLASSES:
            # Update fixtures have ascending Vector order and canonical/explicit
            # map scalar values; constructor condition uses shuffled seed-17 inputs.
            base_values = tuple(range(size))
            base_pairs = tuple((value, value) for value in base_values)
            for condition in ('construction', 'updates_latest', 'updates_retained'):
                observations = []
                for _ in range(trials):
                    if condition == 'construction':
                        result, observation = _measure(lambda: _construct(cls, values, pairs))
                        _verify_constructor(cls, result, size, values)
                    else:
                        base = _construct(cls, base_values, base_pairs)
                        retain = condition == 'updates_retained'
                        result, observation = _measure(lambda: _revisions(cls, base, size, updates, retain))
                        _verify_versions(cls, result, size, updates, retain)
                    observations.append(observation)
                rows.append({
                    'collection': cls.__name__, 'initial_size': size, 'condition': condition,
                    'revisions': 0 if condition == 'construction' else updates,
                    'runtime_update_calls': 0 if condition == 'construction' else updates * (2 if cls is Set else 1),
                    'retained_versions': 1 if condition == 'construction' else updates + 1 if condition == 'updates_retained' else 2,
                    'observations': observations,
                    'median_elapsed_seconds': statistics.median(row['elapsed_seconds'] for row in observations),
                    'maximum_traced_peak_bytes': max(row['traced_peak_bytes'] for row in observations),
                    'all_correctness_obligations_passed': True,
                })
    after = source_snapshot()
    if before != after:
        raise RuntimeError('benchmark source/product bytes changed during measurement; no new evidence written')
    return {
        'schema': 1, 'workload': 'm03 exact tuple-backed eager collections', 'target': 'cpython-3.13.1',
        'environment': environment(),
        'source_sha256': after['owned_sources'], 'product_artifacts_sha256': after['product_artifacts'],
        'source_snapshot_unchanged': True,
        'conditions': {
            'sizes': sizes, 'trials': trials, 'revisions_per_update_condition': updates,
            'construction_input_order': 'seed-17 shuffled homogeneous exact integer keys/items, no duplicates',
            'payload': 'exact integers; maps use exact integer key/value pairs',
            'update_indices': '(step * 379) % n, distinct under selected sizes/count',
            'Vector_update': 'updated_at(index, n + step); size remains n',
            'Map_OrderedMap_update': 'updated(index, n + step); existing keys, size remains n',
            'Set_update': 'without(index).added(n + step); two runtime calls per revision, size remains n',
            'latest_retention': 'base and latest retained; intermediate versions discarded',
            'history_retention': 'base plus every revision retained',
            'included': 'runtime validation, operation storage copying/scans, result allocation, loop overhead, perf_counter and tracemalloc overhead',
            'excluded': 'imports/startup, input generation, update-base construction, correctness checks, environment/source hashing and JSON writing',
            'memory': 'tracemalloc Python allocations only, not RSS; update bases/input fixtures allocated before tracing',
            'OS_page_cache': 'uncontrolled; no cold filesystem/cache claim',
            'source_gate': 'owned runtime/test/harness and complete model.foundation_identities maps match before/after measured trials',
        },
        'backend_contract': {
            'storage': 'exact builtin tuple; trusted CPython/product implementation, no external backend',
            'construction': 'Vector O(n+D); Map/OrderedMap/Set O(n log n+D) general upper bound, sorting may exploit input order',
            'single_updates': 'O(n+D_new) tuple storage scanning/copying; retained n-sized k histories can use O(kn) references',
            'lookup': 'Vector indexing O(1); map/set lookup O(n) scalar comparisons',
            'map_merge': 'O((n+m) log(n+m)+D) construction grouping/sorting and deep payload validation',
            'set_binary': 'O(n+m) homogeneous scalar traversal and output allocation',
            'D': 'reachable validation/comparison payload occurrences; arbitrary string/bytes key lengths and nested data costs are additional',
            'limitations': 'not a tree/trie structural-sharing backend; no universal speed or logarithmic update claim',
        },
        'measurements': rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sizes', type=int, nargs='+', default=[100, 1000, 10000])
    parser.add_argument('--trials', type=int, default=3)
    parser.add_argument('--updates', type=int, default=32)
    args = parser.parse_args()
    target_gate()
    if any(size < 1 for size in args.sizes) or args.trials < 1 or args.updates < 1:
        parser.error('sizes, trials and updates must be positive')
    result = benchmark(args.sizes, args.trials, args.updates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(f"Recorded {len(result['measurements'])} conditions; all retained-value assertions passed: {args.output}")


if __name__ == '__main__':
    main()
