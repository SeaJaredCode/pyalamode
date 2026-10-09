import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.checker import analyze_file, analyze_source, analyze_sources
from pyalamode.project import build_paths, check_paths

PREFIX = "from pyalamode import fun\nfrom collections.abc import Callable\n"
ROOT = Path(__file__).resolve().parents[1]


class ModuleContracts(unittest.TestCase):
    def good(self, source):
        result = analyze_source(source, "sample.py")
        self.assertTrue(result.verified, result.to_dict())
        return result

    def bad(self, source, rule=None):
        result = analyze_source(source, "sample.py")
        self.assertEqual(result.status, 1, result.to_dict())
        if rule:
            self.assertIn(rule, [d.rule for d in result.diagnostics], result.to_dict())
        return result

    def test_header_placement_and_non_directive_strings(self):
        result = self.good('#!/usr/bin/env python3\n# coding: utf-8\n"""module"""\n# mode: fun\nVALUE = 2\ndef f(x: int) -> int:\n    return VALUE + x\n')
        self.assertTrue(result.module_mode)
        self.assertEqual(result.initialization_evidence, "checked pure source initialization")
        for source in ['# mode: fun\n"""module"""\ndef f(x: int) -> int:return x\n',
                       'import types\n# mode: fun\ndef f(x: int) -> int:return x\n',
                       'def ordinary():\n    # mode: fun\n    pass\n',
                       '# mode: fun\n# mode: fun\ndef f(x: int) -> int:return x\n',
                       '# mode: fun\ndef f(x: int) -> int:return x\n# mode: off\n']:
            self.bad(source, "PAL121")
        for source in ['"""# mode: fun"""\ndef ordinary():print(1)\n', 'description = "# mode: fun"\n']:
            result = self.good(source)
            self.assertFalse(result.module_mode)
            self.assertEqual(result.selected_functions, 0)

    def test_recursive_exact_tuple_contracts(self):
        result = self.good('# mode: fun\nBASE = (1, ("a", b"b"))\ndef f(x: tuple[int, tuple[str, bytes]]) -> tuple[int, tuple[str, bytes]]:\n    return x\ndef g() -> tuple[int, tuple[str, bytes]]:\n    return f(BASE)\ndef empty() -> tuple[()]:return ()\ndef homogeneous(x: tuple[int, ...]) -> int:return len(x)\ndef use() -> int:return homogeneous((1, 2, 3))\n')
        self.assertEqual(result.contracts[0].parameters['x'], 'tuple[int, tuple[str, bytes]]')
        for expression in ['(1, [2])', '(1, (True,))', '(1, (2, 3))', '[1, (2,)]']:
            self.bad(PREFIX + '@fun\ndef f() -> tuple[int, tuple[int]]:\n    return ' + expression + '\n')
        self.bad(PREFIX + '@fun\ndef f(x: tuple[int, ...]) -> tuple[int, int]:return x\n', 'PAL211')
        self.bad(PREFIX + '@fun\ndef f(x: tuple[int, int]) -> tuple[int, ...]:return x\nf((1, True))\n', 'PAL221')
        self.good(PREFIX + '@fun\ndef f(x: tuple[int, int]) -> tuple[int, ...]:return x\nf((1, 2))\n')

    def test_tuple_whitelist_excludes_protocols_and_callable_data(self):
        for annotation in ['tuple', 'tuple[Any, ...]', 'tuple[int | list[int]]', 'tuple[int] | str', 'tuple[Callable[[int], int]]', 'list[int]', 'Sequence[int]', 'Callable[..., int]', 'Callable[[Any], int]']:
            self.bad(PREFIX + f'@fun\ndef f(x: {annotation}) -> int:return 1\n', 'PAL130')
        self.bad(PREFIX + '@fun\ndef identity(x: int) -> int:return x\n@fun\ndef f() -> tuple[int]:return (identity,)\n', 'PAL221')

    def test_A09_stable_constants_and_all_analyzed_writers(self):
        self.good(PREFIX + 'BASE = 1\nWORDS = ("a", "b")\n@fun\ndef f() -> int:return BASE + len(WORDS)\n')
        for writer in ['BASE = 2', 'def shell():\n    global BASE\n    BASE = 2', 'namespace = globals()\nnamespace["BASE"] = 2', 'globals()["BASE"] = 2']:
            self.bad(PREFIX + 'BASE = 1\n@fun\ndef f() -> int:return BASE\n' + writer + '\n', 'PAL240')
        self.bad(PREFIX + 'BASE = mutable_hook()\n@fun\ndef f() -> int:return BASE\n')
        self.bad(PREFIX + 'BASE = LATER\nLATER = 1\n@fun\ndef f() -> int:return BASE\n', 'PAL240')

    def test_checked_calls_signatures_aliases_and_recursion_failures(self):
        source = PREFIX + '@fun\ndef first(x: int) -> int:\n    if x == 0:return 1 // x\n    return second(x - 1)\n@fun\ndef second(x: int) -> int:return first(x)\n@fun\ndef entry(x: int) -> int:return second(x)\n'
        result = self.good(source)
        self.assertTrue(all(c.failures == ['RecursionError', 'ZeroDivisionError'] for c in result.contracts))
        self.good(PREFIX + '@fun\ndef f(x: int, /, y: str="a", *, flag: bool=True) -> int:return x if flag else len(y)\n@fun\ndef g() -> int:return f(1)\n')
        self.bad(PREFIX + '@fun\ndef f(x: int) -> int:return x\n@fun\ndef g() -> int:return f(True)\n', 'PAL221')
        self.good(PREFIX + '@fun\ndef f(x: int) -> int:return x\n@fun\ndef g(x: int) -> int:\n    alias = f\n    return alias(x)\n')

    def test_callable_obligations_actual_targets_and_failure_bound(self):
        source = PREFIX + '@fun\ndef divide(x: int) -> int:return 1 // x\n@fun\ndef apply(cb: Callable[[int], int], x: int) -> int:return cb(x)\n@fun\ndef caller(x: int) -> int:return apply(divide, x)\n@fun\ndef default(x: int, cb: Callable[[int], int]=divide) -> int:return cb(x)\n@fun\ndef factory() -> Callable[[int], int]:return divide\n@fun\ndef returned(x: int) -> int:return factory()(x)\napply(divide, 1)\n'
        result = self.good(source)
        contracts = {c.name: c for c in result.contracts}
        for name in ['apply', 'caller', 'default', 'returned']:
            self.assertIn('ZeroDivisionError', contracts[name].failures)
        self.assertEqual(contracts['factory'].return_callable_targets, ['sample.py::divide'])
        self.assertEqual(contracts['default'].callable_defaults, {'cb': ['sample.py::divide']})
        self.bad(PREFIX + 'def unknown(x: int) -> int:return x\n@fun\ndef apply(cb: Callable[[int], int]) -> int:return cb(1)\napply(unknown)\n', 'PAL221')
        self.bad(PREFIX + '@fun\ndef apply(cb: Callable[[int], int]) -> int:return cb(1)\ndef shell(cb: Callable[[int], int]):return apply(cb)\n', 'PAL221')

    def test_callable_shape_cannot_hide_keyword_only_or_variadic_inputs(self):
        apply = '@fun\ndef apply(cb: Callable[[int], int]) -> int:return cb(1)\n'
        for parameters in ['x: int, *, y: int', 'x: int, *, y: int=1', 'x: int, *args', 'x: int, **kwargs']:
            self.bad(PREFIX + f'@fun\ndef f({parameters}) -> int:return x\n' + apply + 'apply(f)\n')
        self.good(PREFIX + '@fun\ndef f(x: int=1, /) -> int:return x\n' + apply + 'apply(f)\n')

    def test_nested_functions_shadow_and_capture_metadata(self):
        result = self.good(PREFIX + '@fun\ndef make(offset: int) -> Callable[[int], int]:\n    def add(x: int) -> int:return offset + x\n    return add\n@fun\ndef use(x: int) -> int:return make(2)(x)\n')
        self.assertEqual(next(c for c in result.contracts if c.name == 'make.add').captures, {'offset': 'int'})
        self.good(PREFIX + '@fun\ndef outer(x: int) -> int:\n    def inner(x: str) -> int:return len(x)\n    return inner("a") + x\n')
        self.bad(PREFIX + '@fun\ndef outer(x: int) -> int:\n    def inner() -> int:return x\n    x = 2\n    return inner()\n')
        self.bad(PREFIX + '@fun\ndef outer() -> int:\n    offset = 1\n    def inner() -> int:return offset\n    def mutate() -> None:\n        nonlocal offset\n        offset = 2\n    return inner()\n')

    def test_ordinary_closed_captures_and_nonlocal_writes(self):
        self.good(PREFIX + 'def outer():\n    offset = 1\n    @fun\n    def inner(x: int) -> int:return offset + x\n    return inner\n')
        self.bad(PREFIX + 'def outer():\n    offset = 1\n    @fun\n    def inner(x: int) -> int:return offset + x\n    def mutate():\n        nonlocal offset\n        offset = 2\n    return inner\n', 'PAL240')
        self.bad(PREFIX + 'VALUE=1\ndef outer(VALUE):\n    @fun\n    def inner() -> int:return VALUE\n    return inner\n', 'PAL240')
        self.bad(PREFIX + 'VALUE=1\ndef outer(VALUE):\n    def middle():\n        @fun\n        def inner() -> int:return VALUE\n        return inner\n    return middle\n', 'PAL240')
        self.bad(PREFIX + 'def outer():\n    @fun\n    def inner(x: int) -> int:return x\n    return inner(True)\n', 'PAL221')

    def test_transitive_checked_captures_keep_lexical_identity(self):
        result=self.good(PREFIX + '@fun\ndef outer(offset: int) -> Callable[[], Callable[[int], int]]:\n    def middle() -> Callable[[int], int]:\n        def inner(x: int) -> int:return x + offset\n        return inner\n    return middle\n')
        self.assertEqual(next(c for c in result.contracts if c.name=='outer.middle.inner').captures, {'offset':'int'})
        self.assertEqual(next(c for c in result.contracts if c.name=='outer.middle').captures, {'offset':'int'})

    def test_closure_cells_ready_at_invocation_and_escape(self):
        for middle, tail in [('value = first(1)', 'return value'), ('return first', '')]:
            returns = 'int' if middle.startswith('value') else 'Callable[[int], int]'
            source = PREFIX + f'@fun\ndef outer() -> {returns}:\n    def first(x: int) -> int:return second(x)\n    {middle}\n    def second(x: int) -> int:return x\n' + ('    ' + tail + '\n' if tail else '')
            self.bad(source, 'PAL240')
        self.good(PREFIX + '@fun\ndef outer() -> int:\n    def first(x: int) -> int:return second(x)\n    def second(x: int) -> int:return x\n    return first(1)\n')

    def test_definition_site_bindings_and_lexical_annotations(self):
        for prefix, annotation in [('def outer(int):', 'int'), ('def outer():\n    int = str', 'int'), ('def outer(Callable):', 'Callable[[int], int]')]:
            self.bad(PREFIX + prefix + f'\n    @fun\n    def inner(x: {annotation}) -> int:return 1\n    return inner\n', 'PAL130')
        self.bad(PREFIX + '@fun\ndef f(x: int=LATER) -> int:return x\nLATER=1\n')
        self.bad(PREFIX + '@fun\ndef f(cb: Callable[[int], int]=f) -> int:return cb(1)\n')
        self.bad('@fun\ndef f(x: int) -> int:return x\nfrom pyalamode import fun\n', 'PAL120')
        self.bad('@fun\ndef f(x: Imported) -> int:return 1\nfrom types import NoneType as Imported\nfrom pyalamode import fun\n')

    def test_controlled_defaults_and_separate_failure_phases(self):
        result = self.good('# mode: fun\nVALUE=1 // 0\ndef f(x: int=2 // 0) -> int:return x\ndef outer() -> int:\n    def nested(x: int=3 // 0) -> int:return x\n    return nested()\n')
        contracts = {c.name: c for c in result.contracts}
        self.assertEqual(result.initialization_failures, ['ZeroDivisionError'])
        self.assertEqual(contracts['f'].definition_failures, ['ZeroDivisionError'])
        self.assertEqual(contracts['f'].failures, [])
        self.assertEqual(contracts['outer'].failures, ['ZeroDivisionError'])
        for default in ['[]', 'hook()', 'unknown', 'True']:
            self.bad(PREFIX + f'@fun\ndef f(x: int={default}) -> int:return x\n')
        self.bad(PREFIX + '@fun\ndef factory() -> int:return 1\n@fun\ndef f(x: int=factory()) -> int:return x\n', 'PAL230')

    def test_initialization_and_annotations_never_execute_hooks(self):
        with tempfile.TemporaryDirectory() as directory:
            flag = Path(directory)/'executed'
            for source in [f'# mode: fun\nopen({str(flag)!r}, "w").write("bad")\ndef f(x: int) -> int:return x\n',
                           PREFIX + f'@fun\ndef f(x: open({str(flag)!r}, "w")) -> int:return 1\n',
                           PREFIX + f'@open({str(flag)!r}, "w")\n@fun\ndef f(x: int) -> int:return x\n']:
                self.bad(source)
                self.assertFalse(flag.exists())

    def test_A10_callable_attribute_replacement_aliases(self):
        for mutation in ['f.__code__ = other', 'alias=f\nalias.__defaults__=(1,)', 'def shell():\n    alias=f\n    alias.__code__=other', 'setattr(f, "__code__", other)', 'f.__dict__["replacement"] = 1']:
            self.bad(PREFIX + '@fun\ndef f(x: int) -> int:return x\n' + mutation + '\n', 'PAL240')


class ModuleProjects(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, source):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        return path

    def check(self, name='app.py', cache=False):
        return check_paths([self.root/name], root=self.root, cache=cache)

    def test_project_policy_requires_module_without_marker(self):
        self.write('pyproject.toml', '[tool.pyalamode]\nschema=1\nrequire_modules=["core/**/*.py"]\n')
        path = self.write('core/app.py', 'BASE=2\ndef f(x: int) -> int:return x + BASE\n')
        result = check_paths([path], root=self.root, cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertTrue(result.results[0].module_mode)
        self.write('core/app.py', 'BASE=[]\ndef f(x: int) -> int:return x\n')
        self.assertEqual(check_paths([path], root=self.root).status, 1)
        for value in ['[1]', '["../app.py"]', '["/app.py"]', '"*.py"']:
            self.write('pyproject.toml', '[tool.pyalamode]\nrequire_modules=' + value + '\n')
            self.assertEqual(check_paths([path], root=self.root).status, 2)

    def test_cross_module_aliases_actual_bindings_and_build(self):
        self.write('core.py', '# mode: fun\nBASE=2\ndef add(x: int) -> int:return x+BASE\n')
        app = self.write('app.py', '# mode: fun\nimport core as calculations\nfrom core import add as plus\ndef f(x: int) -> int:return calculations.add(plus(x))\n')
        result = self.check()
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual(len(result.results), 2)
        output = self.root/'artifact'
        built = build_paths([app], root=self.root, output=output)
        self.assertEqual(built.status, 0, built.to_dict())
        self.assertEqual((output/'app.py').read_bytes(), app.read_bytes())
        process = subprocess.run([sys.executable, '-c', 'import app; print(app.f(1))'], cwd=output, capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout.strip(), '5')
        self.write('app.py', '# mode: fun\nfrom core import add\nadd=unknown\ndef f(x: int) -> int:return add(x)\n')
        self.assertEqual(self.check().status, 1)

    def test_ordinary_import_initialization_separate_and_direct_call_obligations(self):
        self.write('core.py', 'from pyalamode import fun\nprint("ordinary initialization")\n@fun\ndef identity(x: int) -> int:return x\n')
        self.write('app.py', 'from pyalamode import fun\nfrom core import identity\n@fun\ndef f(x: int) -> int:return identity(x)\nidentity(1)\n')
        result=self.check()
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertTrue(all(r.initialization_evidence == 'unchecked ordinary module initialization' for r in result.results))
        self.write('app.py', 'import core as c\nc.identity(True)\n')
        self.assertEqual(self.check().status, 1)
        self.write('app.py', '# mode: fun\nfrom core import identity\ndef f(x: int) -> int:return identity(x)\n')
        result=self.check()
        self.assertEqual(result.status, 1)
        self.assertIn('PAL241', [d.rule for r in result.results for d in r.diagnostics])

    def test_local_foundation_spelling_cannot_admit_custom_hooks(self):
        cases = [('pyalamode.py', 'def fun(f):print("hook");return f\n', 'from pyalamode import fun\n@fun\ndef f(x: int) -> int:return x\n'),
                 ('typing.py', 'class Callable:\n    def __class_getitem__(cls, x):print("hook");return object\n', 'from pyalamode import fun\nfrom typing import Callable\n@fun\ndef f(cb: Callable[[int], int]) -> int:return cb(1)\n'),
                 ('types.py', 'NoneType=list\n', 'from pyalamode import fun\nfrom types import NoneType\n@fun\ndef f(x: NoneType) -> NoneType:return x\n')]
        for name, dependency, app in cases:
            with self.subTest(name=name):
                dependency_path=self.write(name, dependency)
                self.write('app.py', app)
                self.assertEqual(self.check().status, 1)
                dependency_path.unlink()

    def test_package_initialization_relative_imports_and_missing_exports(self):
        self.write('pkg/__init__.py', '# mode: fun\n')
        self.write('pkg/leaf.py', '# mode: fun\ndef f(x: int) -> int:return x\n')
        self.write('pkg/core.py', '# mode: fun\nfrom .leaf import f\ndef g(x: int) -> int:return f(x)\n')
        self.write('app.py', '# mode: fun\nfrom pkg.core import g\ndef h(x: int) -> int:return g(x)\n')
        self.assertEqual(self.check().status, 0)
        self.write('pkg/__init__.py', 'print("ordinary init")\n')
        self.assertEqual(self.check().status, 1)
        self.write('pkg/__init__.py', '# mode: fun\n')
        self.write('app.py', '# mode: fun\nfrom pkg.core import missing\ndef h(x: int) -> int:return x\n')
        self.assertEqual(self.check().status, 1)

    def test_failed_dependency_marks_affected_files_and_exports_unverified(self):
        self.write('leaf.py', '# mode: fun\ndef f(x: int) -> int:return hash(x)\n')
        self.write('middle.py', '# mode: fun\nfrom leaf import f\ndef g(x: int) -> int:return f(x)\n')
        app=self.write('app.py', '# mode: fun\nfrom middle import g\ndef h(x: int) -> int:return g(x)\n')
        result=self.check()
        self.assertEqual(result.status, 1)
        self.assertTrue(all(not r.verified and r.status == 1 for r in result.results))
        self.assertTrue(all(r.initialization_evidence.startswith('unverified') for r in result.results))
        self.assertTrue(all(c.source_evidence.startswith('unverified') for r in result.results for c in r.contracts))
        self.assertEqual(analyze_file(app).status, 1)
        self.assertEqual(build_paths([app], root=self.root, output=self.root/'failed').status, 1)
        self.assertFalse((self.root/'failed').exists())

    def test_dependency_edit_invalidates_only_import_closure(self):
        self.write('leaf.py', '# mode: fun\ndef f(x: int) -> int:return x+1\n')
        self.write('middle.py', '# mode: fun\nfrom leaf import f\ndef g(x: int) -> int:return f(x)\n')
        self.write('app.py', '# mode: fun\nfrom middle import g\ndef h(x: int) -> int:return g(x)\n')
        independent=self.write('independent.py', '# mode: fun\ndef one() -> int:return 1\n')
        cold=check_paths([self.root/'app.py', independent], root=self.root)
        warm=check_paths([self.root/'app.py', independent], root=self.root)
        self.assertEqual(cold.status, 0, cold.to_dict())
        self.assertTrue(all(r.cache_hit for r in warm.results))
        self.write('leaf.py', '# mode: fun\ndef f(x: int) -> int:return x+2\n')
        changed=check_paths([self.root/'app.py', independent], root=self.root)
        self.assertEqual({Path(r.path).name:r.cache_hit for r in changed.results}, {'app.py':False, 'independent.py':True, 'leaf.py':False, 'middle.py':False})
        self.write('leaf.py', '# mode: fun\ndef f(x: int) -> int:return print(x)\n')
        self.assertEqual(check_paths([self.root/'app.py', independent], root=self.root).status, 1)

    def test_mutation_in_other_analyzed_module_blocks_callable(self):
        self.write('core.py', '# mode: fun\ndef f(x: int) -> int:return x\n')
        self.write('app.py', 'import core as c\nc.f.__code__=other\n')
        result=self.check()
        self.assertEqual(result.status, 1, result.to_dict())
        self.assertIn('PAL240', [d.rule for r in result.results for d in r.diagnostics])

    def test_new_ordinary_writer_invalidates_relevant_warm_evidence(self):
        cases = [('from pyalamode import fun\n@fun\ndef f(x: int) -> int:return abs(x)\n', 'import builtins\nbuiltins.abs=print\n'),
                 ('from pyalamode import fun\n@fun\ndef f(x: int) -> int:return x\n', 'import pyalamode\npyalamode.fun=print\n'),
                 ('from pyalamode import fun\nfrom typing import Callable\n@fun\ndef f(cb: Callable[[int], int]) -> int:return cb(1)\n', 'import typing\ntyping.Callable=print\n')]
        for source, mutation in cases:
            with self.subTest(mutation=mutation):
                self.write('core.py', source)
                check_paths([self.root], root=self.root)
                self.assertTrue(all(r.cache_hit for r in check_paths([self.root], root=self.root).results))
                writer=self.write('writer.py', mutation)
                cached=check_paths([self.root], root=self.root)
                fresh=check_paths([self.root], root=self.root, cache=False)
                self.assertEqual(cached.status, 1, cached.to_dict())
                self.assertEqual(cached.status, fresh.status)
                self.assertFalse(next(r for r in cached.results if Path(r.path).name=='core.py').cache_hit)
                writer.unlink()
        self.write('leaf.py', '# mode: fun\ndef identity(x: int) -> int:return x\n')
        self.write('core.py', '# mode: fun\nfrom leaf import identity\ndef f(x: int) -> int:return identity(x)\n')
        self.assertEqual(check_paths([self.root], root=self.root).status, 0)
        check_paths([self.root], root=self.root)
        self.write('writer.py', 'import leaf\nleaf.identity=print\n')
        self.assertEqual(check_paths([self.root], root=self.root).status, 1)
        self.assertEqual(check_paths([self.root], root=self.root, cache=False).status, 1)

    def test_package_precedence_matches_python_source_resolution(self):
        self.write('dep.py', '# mode: fun\ndef identity(x: int) -> int:return x\n')
        self.write('dep/__init__.py', 'from pyalamode import fun\nprint("ordinary initialization")\n@fun\ndef identity(x: int) -> int:return x\n')
        self.write('app.py', '# mode: fun\nfrom dep import identity\ndef f(x: int) -> int:return identity(x)\n')
        result=self.check()
        self.assertEqual(result.status, 1, result.to_dict())
        self.assertTrue(any(Path(r.path).name=='__init__.py' for r in result.results))
        self.assertFalse(any(Path(r.path).name=='dep.py' for r in result.results))

    def test_source_change_during_build_and_audit(self):
        app=self.write('app.py', '# mode: fun\nVALUE=1\ndef f() -> int:return VALUE\n')
        original=app.read_bytes()
        read=Path.read_bytes
        count=0
        def changing(path):
            nonlocal count
            if path.resolve()==app.resolve():
                count+=1
                if count==2:return original+b'# changed\n'
            return read(path)
        with patch.object(Path, 'read_bytes', changing):
            result=build_paths([app], root=self.root, output=self.root/'changed')
        self.assertEqual(result.status, 2, result.to_dict())
        self.assertFalse((self.root/'changed').exists())
        self.write('app.py', '# mode: fun\nVALUE=[]\ndef f() -> int:return 1\n')
        audit=check_paths([app], root=self.root, audit=True)
        self.assertEqual(audit.status, 0)
        self.assertFalse(audit.verified)
        self.assertTrue(all(not r.verified for r in audit.results))


if __name__ == '__main__':
    unittest.main()
