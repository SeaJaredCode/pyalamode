"""Approved finite frontend controls. No authored code or product constructor runs.

The fixed literal oracle inventory was reviewed before helper authorship.
Caller context is not an inherited annotation/effect/capture certificate.
"""
import ast
import builtins
import copy
import io
import json
import tokenize
import unittest
from dataclasses import FrozenInstanceError, replace
from unittest.mock import patch

from pyalamode import source_maps as sm
from pyalamode import syntax as sx

_FIXED = json.loads("{\"schema\":1,\"kind\":\"m14-frontend-fixed-unit-plan\",\"status\":\"source-only-unexecuted\",\"api\":\"API.md\",\"owned_test_file\":\"tests/m14_syntax.py\",\"method_count\":47,\"case_count\":170,\"oracle_policy\":\"All source/expected ranges/output strings are fixed proposal data. No candidate/helper/Python parser has been executed to obtain them. Stock parser errors explicitly depend on actual reported coordinates, not invented messages; fixed malformed header and Unicode/map oracles are independently literal. Compile-only helper status0 never grants inherited strict semantic admission. Parser-error rows also pin a literal expected range plus an independent same-version stock reporter check. Any real disagreement is a retained focused failure requiring root review, never an automatic expected-value rewrite.\",\"methods\":[{\"method\":\"test_prepare_val_scaffold\",\"purpose\":\"Exact raw/scaffold/val relations, no source execution\",\"cases\":[{\"source\":\"val x = 1\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"x = 1\\n\",\"keyword\":[0,3],\"target\":[4,5],\"statement\":[0,9],\"copied_segment\":[0,6,4,10]}},{\"source\":\"def f() -> int:\\n    val café: int = 1\\n    return café\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"def f() -> int:\\n    café: int = 1\\n    return café\\n\",\"keyword\":[20,23],\"target\":[24,29],\"statement\":[20,38]}}]},{\"method\":\"test_prepare_val_forms\",\"purpose\":\"Physical statement grammar and delimiter continuation\",\"cases\":[{\"source\":\"# mode: fun\\nval x = (\\n    1 + 2\\n) # keep\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"# mode: fun\\nx = (\\n    1 + 2\\n) # keep\\n\"}},{\"source\":\"def f() -> int:\\n\\tval\\t x: int = 1\\n\\treturn x\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"def f() -> int:\\n\\tx: int = 1\\n\\treturn x\\n\"}}]},{\"method\":\"test_valid_reserved_names\",\"purpose\":\"Parseable ordinary uses of reserved val remain source1\",\"cases\":[{\"source\":\"val = 1\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[0,3],\"no_lowered_output\":true}},{\"source\":\"val: int = 1\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[0,3],\"no_lowered_output\":true}},{\"source\":\"def val(x: int) -> int:\\n    return x\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[4,7],\"no_lowered_output\":true}},{\"source\":\"x = obj.val\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[8,11],\"no_lowered_output\":true}},{\"source\":\"from other import val\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[18,21],\"no_lowered_output\":true}},{\"source\":\"def f(val: int) -> int:\\n    return val\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[6,9],\"no_lowered_output\":true,\"all_collision_spans\":[[6,9],[35,38]]}},{\"source\":\"match x:\\n    case val:\\n        pass\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[18,21],\"no_lowered_output\":true}},{\"source\":\"try:\\n    pass\\nexcept ValueError as val:\\n    pass\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[35,38],\"no_lowered_output\":true}},{\"source\":\"global val\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[7,10],\"no_lowered_output\":true}},{\"source\":\"nonlocal val\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[9,12],\"no_lowered_output\":true}}]},{\"method\":\"test_nfkc_collisions\",\"purpose\":\"Full authored NAME token, normalized identity never redirects aliases\",\"cases\":[{\"source\":\"ｖａｌ = 1\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[0,9],\"no_lowered_output\":true}},{\"source\":\"val ｖａｌ = 1\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[4,13],\"no_lowered_output\":true}},{\"source\":\"val _pyalamode_syntax_Vector = 1\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[4,28],\"no_lowered_output\":true}},{\"source\":\"val _ｐyalamode_syntax_Vector = 1\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL392\",\"span\":[4,30],\"no_lowered_output\":true}},{\"source\":\"val café = 1\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"café = 1\\n\",\"ast_identifier\":\"café\",\"raw_target_preserved\":true}}]},{\"method\":\"test_malformed_val_headers\",\"purpose\":\"Fixed first offending header token or missing-initializer point\",\"cases\":[{\"source\":\"val (x, y) = (1, 2)\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[4,5],\"no_lowered_output\":true}},{\"source\":\"val x.y = 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[5,6],\"no_lowered_output\":true}},{\"source\":\"val x[0] = 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[5,6],\"no_lowered_output\":true}},{\"source\":\"val x = y = 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[10,11],\"no_lowered_output\":true}},{\"source\":\"val x += 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[6,8],\"no_lowered_output\":true}},{\"source\":\"val x\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[5,5],\"no_lowered_output\":true}},{\"source\":\"val x: int\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[10,10],\"no_lowered_output\":true}},{\"source\":\"val x =\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[7,7],\"no_lowered_output\":true}},{\"source\":\"val x \\\\\\n= 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[6,7],\"no_lowered_output\":true}}]},{\"method\":\"test_malformed_val_contexts\",\"purpose\":\"One-line suite, semicolon and direct class field are malformed dialect declarations\",\"cases\":[{\"source\":\"if True: val x = 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[9,12],\"no_lowered_output\":true}},{\"source\":\"x = 1; val y = 2\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[7,10],\"no_lowered_output\":true}},{\"source\":\"val x = 1; y = 2\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[0,3],\"no_lowered_output\":true,\"first_offending_token\":\"val keyword in semicolon chain\"}},{\"source\":\"class C:\\n    val x: int = 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[13,16],\"no_lowered_output\":true}},{\"source\":\"class C:\\n    def f() -> int:\\n        val x = 1\\n        return x\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"class C:\\n    def f() -> int:\\n        x = 1\\n        return x\\n\",\"no_class_semantic_admission_claim\":true}}]},{\"method\":\"test_encoding_profile\",\"purpose\":\"Strict UTF8/BOM/cookie detection without application imports\",\"cases\":[{\"raw_hex\":\"76616c2078203d20ff0a\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[8,9],\"line\":1,\"column\":9,\"end_line\":1,\"end_column\":10,\"no_prepared_map\":true}},{\"source\":\"# coding: latin-1\\nval x = 1\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[10,17],\"no_lowered_output\":true}},{\"source\":\"# coding: UTF_8\\nval x = 1\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"# coding: UTF_8\\nx = 1\\n\"}},{\"source\":\"﻿# coding: utf-8\\nval x = 1\\n\",\"expected\":{\"source_status\":0,\"scaffold\":\"# coding: utf-8\\nx = 1\\n\",\"authored_bom_hashed\":true}}]},{\"method\":\"test_token_parser_precedence\",\"purpose\":\"Malformed first, with exact stock-reported locations and no guessed end\",\"cases\":[{\"source\":\"val x = (\\n\",\"edition\":\"python-v1\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"not_rule\":\"PAL390\",\"no_prepared_map\":true,\"span\":[10,10],\"line\":2,\"column\":1,\"end_line\":2,\"end_column\":1,\"stock_baseline\":\"tokenize TokenError EOF point; test independently obtains actual stock reporter and checks this fixed range\"}},{\"source\":\"val x = 1\\n_py alamode = 2\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"span\":[14,21],\"line\":2,\"column\":5,\"end_line\":2,\"end_column\":12,\"stock_baseline\":\"stock SyntaxError alamode token; exact range fixed before candidate execution\"}},{\"source\":\"val _pyalamode_syntax_x = (\\n\",\"expected\":{\"source_status\":2,\"rule\":\"PAL001\",\"not_rule\":\"PAL392\",\"no_prepared_map\":true,\"span\":[28,28],\"line\":2,\"column\":1,\"end_line\":2,\"end_column\":1,\"stock_baseline\":\"tokenize EOF point\"}}]},{\"method\":\"test_disabled_edition\",\"purpose\":\"Actual authored identity remains experimental; known disabled selection is semantic\",\"cases\":[{\"source\":\"# mode: fun\\nval x = 1\\n\",\"edition\":\"python-v1\",\"expected\":{\"source_status\":1,\"rule\":\"PAL390\",\"span\":[0,0],\"line\":1,\"column\":1,\"prepared_edition\":\"pyalamode-v1-experimental\",\"selected_edition\":\"python-v1\",\"no_lowered_output\":true}},{\"source\":\"﻿# mode: fun\\nval x = 1\\n\",\"edition\":\"python-v1\",\"expected\":{\"source_status\":1,\"rule\":\"PAL390\",\"span\":[3,3],\"line\":1,\"column\":1,\"no_lowered_output\":true}},{\"source\":\"val x = 1\\n\",\"edition\":\"unknown\",\"expected\":{\"exception\":\"SourceMapError\",\"projection\":\"PAL001/tooling2\"}},{\"source\":\"x = [1]\\n\",\"owner_authored\":\"unit.py\",\"owner_runtime\":\"unit.py\",\"expected\":{\"exception\":\"SourceMapError\",\"no_dialect_lowering\":true}}]},{\"method\":\"test_protected_text_bytes\",\"purpose\":\"Comment/string/bytes/JoinedStr extents copied without lexical rewrite\",\"cases\":[{\"source\":\"# val [1] {2} _pyalamode_syntax_x\\nval s = \\\"val [1] {2} _pyalamode_syntax_x\\\"\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"# val [1] {2} _pyalamode_syntax_x\\ns = \\\"val [1] {2} _pyalamode_syntax_x\\\"\\n\",\"used_collections\":[]}},{\"source\":\"val s = '''val [\\n{1}  \\n]'''\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"s = '''val [\\n{1}  \\n]'''\\n\",\"used_collections\":[]}},{\"source\":\"val s = f\\\"val {x!r} [1]\\\"\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"s = f\\\"val {x!r} [1]\\\"\\n\",\"inherited_semantic_refusal\":\"PAL201\",\"used_collections\":[]}}]},{\"method\":\"test_literal_constructors\",\"purpose\":\"Exact smallest Vector/Map/Set transformations\",\"cases\":[{\"source\":\"val xs = [1, 2]\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nxs = _pyalamode_syntax_Vector.of(1, 2)\\n\",\"used_collections\":[\"Vector\"]}},{\"source\":\"val kv = {\\\"b\\\": 2, \\\"a\\\": 1}\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Map as _pyalamode_syntax_Map\\nkv = _pyalamode_syntax_Map.of((\\\"b\\\", 2), (\\\"a\\\", 1))\\n\",\"used_collections\":[\"Map\"]}},{\"source\":\"val ids = {3, 1, 3}\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Set as _pyalamode_syntax_Set\\nids = _pyalamode_syntax_Set.of(3, 1, 3)\\n\",\"used_collections\":[\"Set\"]}},{\"source\":\"val t = (1, 2)\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"t = (1, 2)\\n\",\"used_collections\":[]}}]},{\"method\":\"test_nested_display_order\",\"purpose\":\"Recursive structure preserves child once/order without runtime execution\",\"cases\":[{\"source\":\"val x = [{\\\"b\\\": f(1), \\\"a\\\": g(2)}, {3, 1}]\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nfrom pyalamode import Map as _pyalamode_syntax_Map\\nfrom pyalamode import Set as _pyalamode_syntax_Set\\nx = _pyalamode_syntax_Vector.of(_pyalamode_syntax_Map.of((\\\"b\\\", f(1)), (\\\"a\\\", g(2))), _pyalamode_syntax_Set.of(3, 1))\\n\",\"ast_call_order\":[\"f(1)\",\"g(2)\"],\"used_collections\":[\"Vector\",\"Map\",\"Set\"],\"no_callback_execution\":true}},{\"source\":\"val x = [first(), fail(), later()]\\n\",\"expected\":{\"source_status\":0,\"compatible_expression\":\"Vector.of(first(), fail(), later())\",\"ast_child_order\":[\"first()\",\"fail()\",\"later()\"],\"runtime_failure_order_owned_by_main\":true}}]},{\"method\":\"test_runtime_value_contexts\",\"purpose\":\"Defaults, decorators, returns, call arguments and match guards transform value children\",\"cases\":[{\"source\":\"def f(x = [1]):\\n    return [x]\\n\",\"expected\":{\"source_status\":0,\"expected_call_families\":[\"Vector\",\"Vector\"]}},{\"source\":\"@decorate([1])\\ndef f():\\n    return call({1})\\n\",\"expected\":{\"source_status\":0,\"expected_call_families\":[\"Vector\",\"Set\"],\"import_before_decorator\":true}},{\"source\":\"match x:\\n    case True if [1].length() == 1:\\n        pass\\n\",\"expected\":{\"source_status\":0,\"pattern_unchanged\":true,\"guard_vector_lowered\":true}}]},{\"method\":\"test_annotation_subscript_pattern_exclusions\",\"purpose\":\"Context traversal preserves annotation/type/store/match syntax\",\"cases\":[{\"source\":\"from typing import Callable\\nfrom pyalamode import Effectful, IO, Vector\\nval f: Callable[[int], int] = inc\\nval g: Effectful[[int], int, IO] = inc\\nval xs: Vector[int] = [1]\\nval x = xs[0]\\n\",\"expected\":{\"source_status\":0,\"annotation_lists_preserved\":true,\"subscript_preserved\":true,\"used_collections\":[\"Vector\"]}},{\"source\":\"[a, b] = pair\\nmatch x:\\n    case [a, b]:\\n        pass\\n\",\"expected\":{\"source_status\":0,\"lowered\":\"[a, b] = pair\\nmatch x:\\n    case [a, b]:\\n        pass\\n\",\"used_collections\":[],\"inherited_semantics_not_admitted\":true}},{\"source\":\"def f[T: tuple[int, str]](x: T) -> T:\\n    return x\\n\",\"expected\":{\"source_status\":0,\"type_parameters_preserved\":true,\"inherited_semantics_not_admitted\":true}}]},{\"method\":\"test_unsupported_display_forms\",\"purpose\":\"Full outer display/generator anchors and nested duplicate suppression\",\"cases\":[{\"source\":\"val x = [i for i in xs]\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,23],\"no_lowered_output\":true}},{\"source\":\"val x = {i for i in xs}\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,23],\"no_lowered_output\":true}},{\"source\":\"val x = {i: i for i in xs}\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,26],\"no_lowered_output\":true}},{\"source\":\"val x = (i for i in xs)\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,23],\"no_lowered_output\":true}},{\"source\":\"val x = [1, *xs]\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,16],\"no_lowered_output\":true}},{\"source\":\"val x = {**xs}\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,14],\"no_lowered_output\":true}},{\"source\":\"val x = [[i for i in xs], *ys]\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,30],\"no_lowered_output\":true,\"issue_count\":1}}]},{\"method\":\"test_empty_display_feedback\",\"purpose\":\"No general expected-type inference or empty Set punctuation\",\"cases\":[{\"source\":\"val x = []\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,10],\"no_lowered_output\":true}},{\"source\":\"val x = {}\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[8,10],\"no_lowered_output\":true}},{\"source\":\"def f():\\n    return []\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[20,22],\"no_lowered_output\":true}},{\"source\":\"val x: Vector[int] = [] if yes else [1]\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[21,23],\"no_lowered_output\":true}},{\"source\":\"val x = [[]]\\n\",\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[9,11],\"no_lowered_output\":true}},{\"source\":\"val x = Set[int].of()\\nval y = OrderedMap[str, int].of()\\n\",\"expected\":{\"source_status\":0,\"used_collections\":[],\"explicit_compatible_unchanged\":true}}]},{\"method\":\"test_empty_direct_contexts\",\"purpose\":\"Exact direct simple-name annotated initializer supplied by main\",\"cases\":[{\"source\":\"val xs: Vector[int] = []\\n\",\"context\":{\"span\":[22,24],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nxs: Vector[int] = _pyalamode_syntax_Vector[int].of()\\n\",\"compatible\":\"xs: Vector[int] = Vector[int].of()\"}},{\"source\":\"val kv: Map[str, int] = {}\\n\",\"context\":{\"span\":[24,26],\"family\":\"Map\",\"schema\":\"Map[str, int]\"},\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Map as _pyalamode_syntax_Map\\nkv: Map[str, int] = _pyalamode_syntax_Map[str, int].of()\\n\",\"compatible\":\"kv: Map[str, int] = Map[str, int].of()\"}},{\"source\":\"xs: Vector[int] = []\\n\",\"context\":{\"span\":[18,20],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nxs: Vector[int] = _pyalamode_syntax_Vector[int].of()\\n\"}}]},{\"method\":\"test_empty_alias_qualified_nested\",\"purpose\":\"Argument spelling preserved; caller resolves actual inherited identity\",\"cases\":[{\"source\":\"val xs: V[int] = []\\n\",\"context\":{\"span\":[17,19],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nxs: V[int] = _pyalamode_syntax_Vector[int].of()\\n\",\"compatible\":\"xs: V[int] = V[int].of()\"}},{\"source\":\"val xs: p.Vector[int] = []\\n\",\"context\":{\"span\":[24,26],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nxs: p.Vector[int] = _pyalamode_syntax_Vector[int].of()\\n\",\"compatible\":\"xs: p.Vector[int] = p.Vector[int].of()\"}},{\"source\":\"val xs: Vector[tuple[int, str]] = []\\n\",\"context\":{\"span\":[34,36],\"family\":\"Vector\",\"schema\":\"Vector[tuple[int, str]]\"},\"expected\":{\"source_status\":0,\"lowered\":\"from pyalamode import Vector as _pyalamode_syntax_Vector\\nxs: Vector[tuple[int, str]] = _pyalamode_syntax_Vector[tuple[int, str]].of()\\n\",\"compatible\":\"xs: Vector[tuple[int, str]] = Vector[tuple[int, str]].of()\"}}]},{\"method\":\"test_empty_whole_quoted_annotations\",\"purpose\":\"Whole quoted arguments compile-only render, original token retained and fully anchored\",\"cases\":[{\"source\":\"val xs: \\\"Vector[int]\\\" = []\\n\",\"context\":{\"span\":[24,26],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"source_status\":0,\"compatible_initializer\":\"_pyalamode_syntax_Vector[int].of()\",\"annotation_token_preserved\":true,\"generated_argument_anchor\":[8,21],\"generated_argument_exact\":false,\"actual_schema_availability_owned_by_main\":true}},{\"source\":\"val kv: \\\"Map[str, Vector[int]]\\\" = {}\\n\",\"context\":{\"span\":[34,36],\"family\":\"Map\",\"schema\":\"Map[str, Vector[int]]\"},\"expected\":{\"source_status\":0,\"compatible_initializer\":\"_pyalamode_syntax_Map[str, Vector[int]].of()\",\"annotation_token_preserved\":true,\"generated_argument_anchor\":[8,31],\"generated_argument_exact\":false,\"actual_schema_availability_owned_by_main\":true}},{\"source\":\"val xs: \\\"V[Row]\\\" = []\\n\",\"context\":{\"span\":[19,21],\"family\":\"Vector\",\"schema\":\"Vector[Record['unit:Row']]\"},\"expected\":{\"source_status\":0,\"compatible_initializer\":\"_pyalamode_syntax_Vector[Row].of()\",\"annotation_token_preserved\":true,\"generated_argument_anchor\":[8,16],\"generated_argument_exact\":false,\"actual_schema_availability_owned_by_main\":true}}]},{\"method\":\"test_empty_inner_quoted_and_unrenderable\",\"purpose\":\"Quoted inner schema/forward failures distinct from whole quoted annotations\",\"cases\":[{\"source\":\"val xs: Vector[\\\"int\\\"] = []\\n\",\"context\":[],\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[24,26],\"inherited_annotation_rule\":\"PAL130\",\"compatible\":\"xs: Vector[\\\"int\\\"] = Vector[\\\"int\\\"].of()\",\"no_lowered_output\":true}},{\"source\":\"val xs: \\\"Vector[Missing]\\\" = []\\n\",\"context\":[],\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[28,30],\"inherited_annotation_rule\":\"PAL130\",\"compatible\":\"xs: \\\"Vector[Missing]\\\" = Vector[Missing].of()\",\"no_lowered_output\":true}},{\"source\":\"val xs: \\\"Vector[make_type()]\\\" = []\\n\",\"context\":[],\"expected\":{\"source_status\":1,\"rule\":\"PAL391\",\"span\":[32,34],\"inherited_annotation_rule\":\"PAL130\",\"no_annotation_call\":true,\"no_lowered_output\":true}}]},{\"method\":\"test_invalid_empty_context_rows\",\"purpose\":\"Wrong/duplicate/stale/extra row is tooling API misuse, not annotation authority\",\"cases\":[{\"source\":\"val xs: Vector[int] = []\\n\",\"contexts\":[{\"span\":[0,3],\"family\":\"Vector\",\"schema\":\"Vector[int]\"}],\"expected\":{\"exception\":\"SourceMapError\"}},{\"source\":\"val xs: Vector[int] = []\\n\",\"contexts\":[{\"span\":[22,24],\"family\":\"Map\",\"schema\":\"Map[str, int]\"}],\"expected\":{\"exception\":\"SourceMapError\"}},{\"source\":\"val xs: Vector[int] = []\\n\",\"contexts\":[{\"span\":[22,24],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"duplicate_same_row\"],\"expected\":{\"exception\":\"SourceMapError\"}},{\"source\":\"val xs = [1]\\n\",\"contexts\":[{\"span\":[9,12],\"family\":\"Vector\",\"schema\":\"Vector[int]\"}],\"expected\":{\"exception\":\"SourceMapError\"}},{\"source\":\"val xs: Vector[int] = []\\n\",\"contexts\":[{\"span\":[22,24],\"family\":\"Vector\",\"schema\":\"\"}],\"expected\":{\"exception\":\"SourceMapError\"}},{\"source\":\"val xs: V[Unknown] = []\\n\",\"claimed_context\":{\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"frontend_is_not_semantic_proof\":true,\"main_must_compare_actual_resolver_and_refuse\":\"PAL130/240; no checked claim\"}}]},{\"method\":\"test_forged_prepared_records\",\"purpose\":\"Fresh authored re-preparation prevents substituted scaffold/maps/val/issues\",\"cases\":[{\"mutation\":\"authored_text differs from actual authored bytes\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"mutation\":\"scaffold bytes changed and digest/map forged consistently\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"mutation\":\"val keyword/target/statement span changed while scaffold retained\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"mutation\":\"reserved NAME issue deleted from prepared issues\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"mutation\":\"selected_edition changed without regenerated PAL390\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"mutation\":\"foreign dataclass subclass/bool span/list instead of tuple\",\"expected\":{\"exception\":\"SourceMapError\"}}]},{\"method\":\"test_scaffold_mapping_unicode\",\"purpose\":\"Fixed independent raw bytes including deleted interior declaration\",\"cases\":[{\"source\":\"﻿# mode: fun\\r\\nval café = [\\\"😀\\\", 2]\\r\\n\",\"expected\":{\"authored_bytes\":41,\"scaffold_bytes\":34,\"scaffold\":\"# mode: fun\\r\\ncafé = [\\\"😀\\\", 2]\\r\\n\",\"keyword\":[16,19],\"target\":[20,25],\"display\":[28,39],\"scaffold_target\":[13,18],\"scaffold_display\":[21,32],\"whole_scaffold_query\":{\"generated_span\":[0,34],\"source_span\":[3,41],\"exact\":false},\"target_query\":{\"generated_span\":[13,18],\"source_span\":[20,25],\"exact\":true}}}]},{\"method\":\"test_constructor_import_header\",\"purpose\":\"Mode/cookie/docstring/futures/decorator placement, used-only fixed order\",\"cases\":[{\"source\":\"# mode: fun\\n\\\"\\\"\\\"doc\\\"\\\"\\\"\\nfrom __future__ import annotations\\n# header\\n@fun\\ndef f():\\n    return [1]\\n\",\"expected\":{\"source_status\":0,\"insert_before\":\"@fun\",\"insert_after\":\"# header\\n\",\"import_anchor\":[0,66],\"used_collections\":[\"Vector\"],\"mode_line_unchanged\":true}},{\"source\":\"# coding: utf-8\\r\\n# mode: fun\\r\\nval x = {1}\\r\\n\",\"expected\":{\"source_status\":0,\"generated_import_newline\":\"\\r\\n\",\"used_collections\":[\"Set\"],\"cookie_first_line_preserved\":true}},{\"source\":\"val x = [1]\\nval y = {1: 2}\\nval z = {1}\\n\",\"expected\":{\"source_status\":0,\"import_order\":[\"Vector\",\"Map\",\"Set\"],\"each_import_count\":1}}]},{\"method\":\"test_positions_utf8_utf16\",\"purpose\":\"Independent Unicode byte/UTF16 endpoints and inverse\",\"cases\":[{\"raw\":\"﻿# mode: fun\\r\\nval café = [\\\"😀\\\", 2]\\r\\n\",\"positions\":[{\"offset\":0,\"line\":1,\"column\":1,\"utf16_column\":0},{\"offset\":3,\"line\":1,\"column\":1,\"utf16_column\":0},{\"offset\":14,\"line\":1,\"column\":12,\"utf16_column\":11},{\"offset\":20,\"line\":2,\"column\":5,\"utf16_column\":4},{\"offset\":25,\"line\":2,\"column\":10,\"utf16_column\":8},{\"offset\":30,\"line\":2,\"column\":15,\"utf16_column\":13},{\"offset\":34,\"line\":2,\"column\":19,\"utf16_column\":15},{\"offset\":39,\"line\":2,\"column\":24,\"utf16_column\":20},{\"offset\":41,\"line\":3,\"column\":1,\"utf16_column\":0}],\"inverse_bom_offset\":3}]},{\"method\":\"test_physical_line_endings\",\"purpose\":\"CRLF/loneCR/LF only; U2028/U2029 not lines; tabs one unit\",\"cases\":[{\"raw\":\"a\\r\\nb\\rc\\n\",\"positions\":[{\"offset\":1,\"line\":1,\"column\":2},{\"offset\":3,\"line\":2,\"column\":1},{\"offset\":4,\"line\":2,\"column\":2},{\"offset\":5,\"line\":3,\"column\":1},{\"offset\":7,\"line\":4,\"column\":1}]},{\"raw\":\"a b c\\n\",\"positions\":[{\"offset\":4,\"line\":1,\"column\":5,\"utf16_column\":2},{\"offset\":9,\"line\":1,\"column\":10,\"utf16_column\":5},{\"offset\":10,\"line\":2,\"column\":1,\"utf16_column\":0}]},{\"raw\":\"\\tx\",\"positions\":[{\"offset\":1,\"line\":1,\"column\":2,\"utf16_column\":1},{\"offset\":2,\"line\":1,\"column\":3,\"utf16_column\":2}]}]},{\"method\":\"test_bom_cookie_eof\",\"purpose\":\"BOM stripped only from compiler text; absent final newline and empty EOF\",\"cases\":[{\"raw\":\"\",\"positions\":[{\"offset\":0,\"line\":1,\"column\":1,\"utf16_column\":0}]},{\"raw\":\"﻿\",\"positions\":[{\"offset\":0,\"line\":1,\"column\":1,\"utf16_column\":0},{\"offset\":3,\"line\":1,\"column\":1,\"utf16_column\":0}],\"inverse_bom_offset\":3},{\"source\":\"# coding: utf-8\\nval x = 1\",\"expected\":{\"source_status\":0,\"scaffold\":\"# coding: utf-8\\nx = 1\",\"eof_offset\":25}}]},{\"method\":\"test_invalid_coordinates\",\"purpose\":\"No scalar/surrogate/CRLF/BOM interior or clamp\",\"cases\":[{\"raw\":\"﻿é😀\\r\\n\",\"invalid_offsets\":[1,2,4,6,7,8,10,-1,12],\"expected\":{\"exception\":\"SourceMapError\"}},{\"raw\":\"😀\",\"invalid_utf16_columns\":[1,3,-1],\"invalid_utf8_columns\":[2,3,4,6],\"expected\":{\"exception\":\"SourceMapError\"}},{\"raw\":\"a\\n\",\"invalid_lines\":[0,3],\"invalid_encoding\":\"characters\",\"expected\":{\"exception\":\"SourceMapError\"}}]},{\"method\":\"test_closed_wire_types\",\"purpose\":\"Exact map wire keys/types/digests/translator filename identities\",\"cases\":[{\"mutations\":[\"extra top key\",\"missing coordinate_encoding\",\"schema=true\",\"kind unknown\",\"extra owner key\",\"files key pyalamode/syntax.py instead of syntax.py\",\"uppercase digest\",\"byte_count=true\",\"segments tuple instead of list\",\"foreign dict subclass\"],\"expected\":{\"exception\":\"SourceMapError\"}},{\"expected_top_keys\":[\"schema\",\"kind\",\"owner\",\"translator\",\"source\",\"generated\",\"coordinate_encoding\",\"segments\"],\"expected_translator_file_keys\":[\"source_maps.py\",\"syntax.py\"],\"detached\":true}]},{\"method\":\"test_map_ownership_coverage_validation\",\"purpose\":\"Independent actual bytes and owner/role/digest coverage, not metadata claims\",\"cases\":[{\"mutations\":[\"absolute/../backslash/colon/control/empty-component path\",\"owner module keyword/noncanonical NFKC\",\"runtime stem differs\",\"source digest differs actual bytes\",\"generated digest differs actual bytes\",\"forged caller translator\",\"wrong role pair\",\"gap/overlap/nonmonotonic generated coverage\",\"zero generated segment\",\"copy same size unequal bytes\",\"copy unequal size\",\"out-of-bounds source anchor\",\"UTF8 scalar interior\"],\"expected\":{\"exception\":\"SourceMapError\"}}]},{\"method\":\"test_range_exactness\",\"purpose\":\"Contiguous slope1 source coverage required across segments\",\"cases\":[{\"source\":\"abcd\",\"generated\":\"abcd\",\"segments\":[[0,2,0,2,\"copy\"],[2,4,2,4,\"copy\"]],\"query\":[0,4],\"expected\":{\"source_span\":[0,4],\"exact\":true,\"segments\":[0,1]}},{\"source\":\"abXXcd\",\"generated\":\"abcd\",\"segments\":[[0,2,0,2,\"copy\"],[2,4,4,6,\"copy\"]],\"query\":[0,4],\"expected\":{\"source_span\":[0,6],\"exact\":false,\"segments\":[0,1]}},{\"source\":\"abcd\",\"generated\":\"cdab\",\"segments\":[[0,2,2,4,\"copy\"],[2,4,0,2,\"copy\"]],\"query\":[0,4],\"expected\":{\"source_span\":[0,4],\"exact\":false}},{\"source\":\"ab\",\"generated\":\"abab\",\"segments\":[[0,2,0,2,\"copy\"],[2,4,0,2,\"copy\"]],\"query\":[0,4],\"expected\":{\"source_span\":[0,2],\"exact\":false}},{\"source\":\"abcd\",\"generated\":\"XYcd\",\"segments\":[[0,2,0,2,\"anchor\"],[2,4,2,4,\"copy\"]],\"query\":[1,3],\"expected\":{\"source_span\":[0,3],\"exact\":false}}]},{\"method\":\"test_zero_range_reverse_occurrences\",\"purpose\":\"Half-open right-segment/EOF behavior and no deleted val guesses\",\"cases\":[{\"source\":\"abXXcd\",\"generated\":\"abcd\",\"segments\":[[0,2,0,2,\"copy\"],[2,4,4,6,\"copy\"]],\"query\":[2,2],\"expected\":{\"source_span\":[4,4],\"exact\":true,\"segments\":[1]}},{\"source\":\"abcd\",\"generated\":\"XYcd\",\"segments\":[[0,2,0,2,\"anchor\"],[2,4,2,4,\"copy\"]],\"query\":[1,1],\"expected\":{\"source_span\":[0,2],\"exact\":false}},{\"source\":\"abc\",\"generated\":\"\",\"segments\":[],\"query\":[0,0],\"expected\":{\"source_span\":[3,3],\"exact\":false}},{\"source\":\"\",\"generated\":\"\",\"segments\":[],\"query\":[0,0],\"expected\":{\"source_span\":[0,0],\"exact\":true}},{\"source\":\"abXXcd\",\"generated\":\"abcd\",\"segments\":[[0,2,0,2,\"copy\"],[2,4,4,6,\"copy\"]],\"reverse_query\":[2,4],\"expected\":{\"generated_ranges\":[]}},{\"source\":\"abcd\",\"generated\":\"cdab\",\"segments\":[[0,2,2,4,\"copy\"],[2,4,0,2,\"copy\"]],\"query\":[4,4],\"expected\":{\"source_span\":[4,4],\"exact\":false}},{\"source\":\"ab\",\"generated\":\"abab\",\"segments\":[[0,2,0,2,\"copy\"],[2,4,0,2,\"copy\"]],\"reverse_query\":[0,2],\"expected\":{\"generated_ranges\":[[0,4]]}}]},{\"method\":\"test_composition_copy_splits\",\"purpose\":\"Exact source/intermediate/output descriptor join and deleted gap preservation\",\"cases\":[{\"source\":\"abXXcd\",\"intermediate\":\"abcd\",\"generated\":\"(abcd)\",\"inner\":[[0,2,0,2,\"copy\"],[2,4,4,6,\"copy\"]],\"outer\":[[0,1,0,0,\"anchor\"],[1,5,0,4,\"copy\"],[5,6,4,4,\"anchor\"]],\"expected\":{\"segments\":[[0,1,0,0,\"anchor\"],[1,3,0,2,\"copy\"],[3,5,4,6,\"copy\"],[5,6,6,6,\"anchor\"]],\"whole_exact\":false}}]},{\"method\":\"test_composition_anchor_hulls\",\"purpose\":\"Anchors propagate their complete disclosed originals and zero EOF\",\"cases\":[{\"source\":\"ab\",\"intermediate\":\"XYZb\",\"generated\":\"YZ\",\"inner\":[[0,3,0,1,\"anchor\"],[3,4,1,2,\"copy\"]],\"outer\":[[0,2,1,3,\"copy\"]],\"expected\":{\"segments\":[[0,2,0,1,\"anchor\"]]}},{\"source\":\"ab\",\"intermediate\":\"XYZb\",\"generated\":\"()\",\"inner\":[[0,3,0,1,\"anchor\"],[3,4,1,2,\"copy\"]],\"outer\":[[0,2,0,4,\"anchor\"]],\"expected\":{\"segments\":[[0,2,0,2,\"anchor\"]]}},{\"source\":\"abc\",\"intermediate\":\"\",\"generated\":\"()\",\"inner\":[],\"outer\":[[0,2,0,0,\"anchor\"]],\"expected\":{\"segments\":[[0,2,3,3,\"anchor\"]]}}]},{\"method\":\"test_composition_refusals\",\"purpose\":\"No relabeling/ownership/translator or stale byte joins\",\"cases\":[{\"mutations\":[\"inner generated SHA differs outer source SHA\",\"intermediate actual bytes changed\",\"owner differs\",\"translator differs\",\"formatted role relabeled authored\",\"bounds exceeded by split output\"],\"expected\":{\"exception\":\"SourceMapError\"}}]},{\"method\":\"test_derive_preserved_children\",\"purpose\":\"Stock structural paths and byte-equal child copies, no substring search\",\"cases\":[{\"source\":\"def f(x: int) -> int:\\n    return x + 1\\n\",\"expected_generated\":\"def f(x: int) -> int:\\n    return x + 1\\n\",\"expected\":{\"exact_child_identifiers\":[\"x\"],\"same_ast_fields\":true,\"coverage_complete\":true}},{\"source\":\"def f(x):\\n    return (x)\\n\",\"expected_generated\":\"def f(x):\\n    return x\\n\",\"expected\":{\"exact_return_name\":true,\"changed_parentheses_anchor\":true}},{\"source\":\"val_string = 'é😀'\\n\",\"expected_generated\":\"val_string = 'é😀'\\n\",\"expected\":{\"byte_equal_string_copy\":true,\"coverage_complete\":true}},{\"source\":\"x = -1\\n\",\"expected_generated\":\"x = -1\\n\",\"expected\":{\"parsed_unary_topology_passes\":true}}]},{\"method\":\"test_derive_debug_return_argument\",\"purpose\":\"Literal compiler instrumentation preserves actual returned child, anchors synthetic assertions\",\"cases\":[{\"source\":\"def f(x: int) -> int:\\n    return x + 1\\n\",\"instrumentation\":\"insert assert x is not None anchored to authored arg x; replace Return with result Assign of SAME original BinOp, assert result is not None anchored to complete original Return, Return result anchor\",\"expected\":{\"exact_original_return_Name_and_Constant_children\":true,\"synthetic_assert_argument_anchor\":\"authored arg x\",\"synthetic_return_anchor\":\"complete authored Return\",\"same_reparsed_ast_fields\":true,\"coverage_complete\":true}}]},{\"method\":\"test_derive_facade_fields\",\"purpose\":\"Synthetic facade header/args/defaults/keyword/attribute nodes have explicit boundary origins\",\"cases\":[{\"source\":\"def f(x: int = 1, *, y: int = 2) -> int:\\n    return x + y\\n\",\"instrumentation\":\"Module imports alias, Assign original reference, FunctionDef f with annotation-free copied arg/default nodes, validation Call keyword path, result Assign original(x,y=y), Return result; all inserted nodes anchored explicitly\",\"expected\":{\"same_reparsed_ast_fields\":true,\"coverage_complete\":true,\"missing_any_required_origin_refuses\":true}}]},{\"method\":\"test_derive_finite_allowed_shapes\",\"purpose\":\"Literal syntax fixtures cover finite class and operator vocabulary\",\"cases\":[{\"source\":\"from p import a as b\\nimport p as q\\nclass C:\\n    x: int = 1\\n\\ndef f(x, /, y=1, *, z=2):\\n    with q.borrow(x) as loan:\\n        if x:\\n            a = y if z else 1\\n        else:\\n            a = 2\\n    try:\\n        q.call(a, key=z)\\n    except ValueError as error:\\n        pass\\n    finally:\\n        q.close()\\n    assert a is not None\\n    return q.table[a:2:1]\\n\",\"expected\":{\"same_reparsed_ast_fields\":true,\"mechanical_derivation_only\":true}},{\"source\":\"x = (a+b, a-b, a*b, a@b, a/b, a//b, a%b, a**b, a<<b, a>>b, a|b, a^b, a&b, +a, -a, ~a, not a, a and b, a or b, a==b, a!=b, a<b, a<=b, a>b, a>=b, a is b, a is not b, a in b, a not in b)\\n\",\"expected\":{\"same_reparsed_ast_fields\":true,\"all_declared_operator_classes_covered\":true,\"no_semantic_admission\":true}},{\"source\":\"match x:\\n    case 1 | 2:\\n        pass\\n    case None:\\n        pass\\n    case [a, *rest]:\\n        pass\\n    case {'a': a, **rest}:\\n        pass\\n    case C(a, key=b) as whole:\\n        pass\\n    case _:\\n        pass\\n\",\"expected\":{\"same_reparsed_ast_fields\":true,\"all_declared_pattern_classes_covered\":true,\"no_semantic_admission\":true}},{\"source\":\"x: tuple[int, ...] = (None, True, b'x')\\n\",\"expected\":{\"same_reparsed_ast_fields\":true,\"List_annotation_covered_by_other_fixture\":true,\"Constant_plain_payloads\":true}}]},{\"method\":\"test_derive_topology_fail_closed\",\"purpose\":\"Known unparse normalizations must never receive guessed mapping\",\"cases\":[{\"synthetic_ast\":\"Constant(value=-1)\",\"expected\":{\"exception\":\"SourceMapError\",\"why\":\"reparse UnaryOp != Constant\"}},{\"synthetic_ast\":\"Constant(value=(1,2))\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"synthetic_ast\":\"Set(elts=[])\",\"expected\":{\"exception\":\"SourceMapError\",\"why\":\"unparse call/set topology differs or outside finite class profile\"}},{\"synthetic_ast\":\"Constant(value=float('nan')) / Constant(value=float('inf'))\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"synthetic_ast\":\"Lambda/For/AsyncFunctionDef/NamedExpr/Yield/JoinedStr\",\"expected\":{\"exception\":\"SourceMapError\",\"why\":\"outside finite allowed derivation vocabulary\"}},{\"synthetic_ast\":\"foreign AST subclass or Constant sentinel object whose repr increments flag\",\"expected\":{\"exception\":\"SourceMapError\",\"repr_calls\":0}}]},{\"method\":\"test_derive_origin_validation\",\"purpose\":\"Exact final AST paths, source bytes and boundaries; no installed trust\",\"cases\":[{\"mutations\":[\"missing root\",\"missing positioned child\",\"unknown structural path\",\"index true/-1\",\"wrong copy byte extent\",\"span inside astral scalar\",\"origin foreign subclass\",\"foreign AST field value\",\"extra unsupported AST field\"],\"expected\":{\"exception\":\"SourceMapError\"}},{\"assertion\":\"original tree/origins/source unchanged after derive success/refusal\",\"expected\":true}]},{\"method\":\"test_formatter_safe_edits\",\"purpose\":\"Literal val separator/trailing outside strings/comments/final newline\",\"cases\":[{\"source\":\"val\\t  x = 1  \",\"expected\":{\"format_status\":1,\"source_status\":0,\"after\":\"val x = 1\\n\",\"edits\":[{\"span\":[3,6],\"replacement\":\" \"},{\"span\":[11,13],\"replacement\":\"\"},{\"span\":[13,13],\"replacement\":\"\\n\"}],\"second_status\":0}},{\"source\":\"def f():\\n\\tval\\t x = 1 \\t\\n\\treturn x\\n\",\"expected\":{\"format_status\":1,\"source_status\":0,\"after\":\"def f():\\n\\tval x = 1\\n\\treturn x\\n\",\"indentation_preserved\":true}},{\"source\":\"val x = 1\\r\\n \\t\\r\\n\",\"expected\":{\"format_status\":1,\"source_status\":0,\"after\":\"val x = 1\\r\\n\\r\\n\",\"newline_kind\":\"\\r\\n\"}}]},{\"method\":\"test_formatter_protected_bytes\",\"purpose\":\"No string/comment/JoinedStr token byte edits\",\"cases\":[{\"source\":\"val s = '''a  \\n b\\t\\n'''  # keep  \\n\",\"expected\":{\"format_status\":0,\"source_status\":0,\"after\":\"val s = '''a  \\n b\\t\\n'''  # keep  \\n\",\"string_comment_bytes_identical\":true}},{\"source\":\"val s = \\\"x  \\\" \\t\\n# comment \\t\",\"expected\":{\"format_status\":1,\"source_status\":0,\"after\":\"val s = \\\"x  \\\"\\n# comment \\t\\n\",\"string_comment_bytes_identical\":true}},{\"source\":\"﻿# coding: utf-8\\r\\nval\\t x = 1\",\"expected\":{\"format_status\":1,\"source_status\":0,\"after\":\"﻿# coding: utf-8\\r\\nval x = 1\\r\\n\",\"bom_cookie_identical\":true}}]},{\"method\":\"test_formatter_rebases_empty_rows\",\"purpose\":\"Approved contexts move through exact formatter edit map, no lexical type re-resolution\",\"cases\":[{\"source\":\"val\\t  xs: Vector[int] = []  \\n\",\"context\":{\"span\":[24,26],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"format_status\":1,\"source_status\":0,\"after\":\"val xs: Vector[int] = []\\n\",\"rebased_context\":{\"span\":[22,24],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"same_scaffold_ast\":true,\"same_lowered_ast\":true,\"second_status\":0}},{\"source\":\"val\\t xs: \\\"Vector[int]\\\" = []  \\n\",\"context\":{\"span\":[25,27],\"family\":\"Vector\",\"schema\":\"Vector[int]\"},\"expected\":{\"format_status\":1,\"source_status\":0,\"annotation_token_preserved\":true,\"generated_argument_anchor_full_string\":true,\"same_lowered_ast\":true}}]},{\"method\":\"test_formatter_status_axes\",\"purpose\":\"Formatting refusal status2 preserves semantic source1; no after/edits/map\",\"cases\":[{\"source\":\"val x = []\\n\",\"expected\":{\"format_status\":2,\"source_status\":1,\"rule\":\"PAL391\",\"after\":null,\"edits\":[],\"source_map\":null}},{\"source\":\"val = 1\\n\",\"expected\":{\"format_status\":2,\"source_status\":1,\"rule\":\"PAL392\",\"after\":null,\"edits\":[],\"source_map\":null}},{\"source\":\"val x = 1\\n\",\"edition\":\"python-v1\",\"expected\":{\"format_status\":2,\"source_status\":1,\"rule\":\"PAL390\",\"after\":null,\"edits\":[],\"source_map\":null}},{\"source\":\"val x\\n\",\"expected\":{\"format_status\":2,\"source_status\":2,\"rule\":\"PAL001\",\"after\":null,\"edits\":[],\"source_map\":null}},{\"source\":\"val x = 1\\n\",\"expected\":{\"format_status\":0,\"source_status\":0,\"after\":\"val x = 1\\n\",\"edits\":[],\"idempotent\":true}}]},{\"method\":\"test_bounds_and_exact_argument_types\",\"purpose\":\"Published finite input/output/AST/map caps, with no pre-parser AST allocation claim\",\"cases\":[{\"input\":\"1048577 authored bytes\",\"expected\":{\"exception\":\"SourceMapError\",\"before_tokenization\":true}},{\"input\":\"100001 tokens within byte bound\",\"expected\":{\"exception\":\"SourceMapError\",\"before_stock_parse\":true}},{\"input\":\"parsed AST >100000 nodes/depth>256\",\"expected\":{\"exception\":\"SourceMapError\",\"immediately_after_stock_parse\":true,\"before_unparse\":true}},{\"input\":\"map >200000 segments/output >8388608/serialized map >33554432\",\"expected\":{\"exception\":\"SourceMapError\",\"output_incremental\":true}},{\"input\":\"bytearray/str raw; bool offsets; list contexts; dataclass subclass\",\"expected\":{\"exception\":\"SourceMapError\"}},{\"input\":\"AST cumulative field text8388609 bytes / field items400001 / integer magnitude bits8388609 / origins100002 / path513 elements\",\"expected\":{\"exception\":\"SourceMapError\",\"before_stock_unparse\":true}}]},{\"method\":\"test_detached_records_and_no_dispatch\",\"purpose\":\"Source helpers never call supplied source and returned wire edits do not mutate records\",\"cases\":[{\"source\":\"import os\\nos.write(1, b'SENTINEL')\\nval x = [foreign()]\\n\",\"expected\":{\"source_status\":0,\"source_execution_count\":0,\"no_application_import\":true,\"no_semantic_admission\":true}},{\"action\":\"mutate map_to_dict nested dict/list values after detachment\",\"expected\":{\"original_record_unchanged\":true}},{\"action\":\"modify input context/wire dictionary after successful validation\",\"expected\":{\"validated_frozen_record_unchanged\":true}}]}]}")
CASES = {row["method"]: row["cases"] for row in _FIXED["methods"]}
OWNER = sm.SourceOwner("unit.pya", "unit.py", "unit")
TRANSLATOR = sm.TranslatorIdentity(sm.TRANSLATOR_VERSION,
    (("source_maps.py", "1" * 64), ("syntax.py", "2" * 64)))


class Foreign:
    calls = []
    def __eq__(self, other):
        self.calls.append("eq")
        raise AssertionError("foreign equality")
    def __repr__(self):
        self.calls.append("repr")
        raise AssertionError("foreign representation")
    def __iter__(self):
        self.calls.append("iter")
        raise AssertionError("foreign iterator")


class ForeignOwner(sm.SourceOwner):
    pass


class ForeignMap(dict):
    pass


def _raw(case):
    return bytes.fromhex(case["raw_hex"]) if "raw_hex" in case else case.get("source", case.get("raw", "")).encode("utf-8")


def _rows(case):
    data = case.get("contexts", case.get("context", []))
    if type(data) is dict:
        data = [data]
    rows = []
    for row in data:
        rows.append(rows[-1] if row == "duplicate_same_row" else
                    sx.EmptyDisplayType(sm.ByteSpan(*row["span"]), row["family"], row["schema"]))
    return tuple(rows)


def _owner(case):
    return sm.SourceOwner(case.get("owner_authored", "unit.pya"), case.get("owner_runtime", "unit.py"), "unit")


def _identity(raw, role, path=None):
    path = path or ("unit.pya" if role in {"authored", "formatted"} else "unit.py")
    return sm.source_identity(raw, path=path, edition=sm.EDITION if path.endswith(".pya") else "python-v1", role=role)


def _map(source, generated, segments, source_role="authored", generated_role="lowered"):
    source = source.encode("utf-8") if type(source) is str else source
    generated = generated.encode("utf-8") if type(generated) is str else generated
    return sm.SourceMap(OWNER, TRANSLATOR, _identity(source, source_role), _identity(generated, generated_role),
                        tuple(sm.MapSegment(*row) for row in segments))


def _wire_check(value, source, generated, wire=None, **changes):
    arguments = dict(source=source, generated=generated, owner=value.owner, translator=value.translator,
                     source_identity=value.source, generated_identity=value.generated)
    arguments.update(changes)
    return sm.validate_map(sm.map_to_dict(value) if wire is None else wire, **arguments)


def _span(node, raw):
    # Derivation fixtures use LF. Stock AST columns are byte offsets; no search.
    lines = raw.split(b"\n")
    starts, total = [], 0
    for line in lines:
        starts.append(total)
        total += len(line) + 1
    if type(node) is ast.Module:
        return sm.ByteSpan(0, len(raw))
    return sm.ByteSpan(starts[node.lineno - 1] + node.col_offset,
                       starts[node.end_lineno - 1] + node.end_col_offset)


def _positioned(node):
    return isinstance(node, (ast.stmt, ast.expr, ast.arg, ast.alias, ast.keyword, ast.ExceptHandler, ast.pattern)) or type(node) is ast.Module


def _paths(tree):
    pending = [((), tree)]
    while pending:
        path, node = pending.pop()
        yield path, node
        for name, value in ast.iter_fields(node):
            if type(value) is list:
                pending.extend((path + (name, index), child) for index, child in enumerate(value) if isinstance(child, ast.AST))
            elif isinstance(value, ast.AST):
                pending.append((path + (name,), value))


def _origins(tree, raw, tags=None):
    return {path: (tags[id(node)] if tags is not None and id(node) in tags else sm.NodeOrigin(_span(node, raw), "copy"))
            for path, node in _paths(tree) if _positioned(node)}


def _anchor(node, span, tags):
    for child in ast.walk(node):
        if _positioned(child):
            tags[id(child)] = sm.NodeOrigin(span, "anchor")
    return node


def _derive(raw, tree=None, origins=None):
    tree = ast.parse(raw, feature_version=(3, 13)) if tree is None else tree
    origins = _origins(tree, raw) if origins is None else origins
    return sm.derive_ast(raw, tree, origins, owner=OWNER, translator=TRANSLATOR,
                         source_identity=_identity(raw, "authored"), generated_path="debug/unit.py", generated_role="debug")


def _fields(tree):
    return ast.dump(tree, annotate_fields=True, include_attributes=False)


class FrontendSyntax(unittest.TestCase):
    def setUp(self):
        Foreign.calls.clear()

    def _expected(self, result, expected):
        self.assertEqual(result.status, expected["source_status"])
        if "rule" in expected:
            self.assertTrue(result.issues)
            issue = result.issues[0]
            self.assertEqual(issue.rule, expected["rule"])
            self.assertEqual(issue.category, "tooling" if issue.rule == "PAL001" else "semantic")
            if "span" in expected:
                self.assertEqual(issue.span, sm.ByteSpan(*expected["span"]))
            for key in ("line", "column", "end_line", "end_column"):
                if key in expected:
                    self.assertEqual(getattr(issue, key), expected[key])
            if "not_rule" in expected:
                self.assertNotIn(expected["not_rule"], [row.rule for row in result.issues])
            if "all_collision_spans" in expected:
                self.assertEqual([[row.span.start, row.span.end] for row in result.issues], expected["all_collision_spans"])
            if "issue_count" in expected:
                self.assertEqual(len(result.issues), expected["issue_count"])

    def _prepare(self, case):
        expected = case["expected"]
        arguments = dict(edition=case.get("edition", sm.EDITION), translator=TRANSLATOR)
        if "exception" in expected:
            with self.assertRaises(sm.SourceMapError):
                sx.prepare_source(_raw(case), _owner(case), **arguments)
            return None
        result = sx.prepare_source(_raw(case), _owner(case), **arguments)
        self._expected(result, expected)
        if expected.get("no_prepared_map"):
            self.assertIsNone(result.prepared)
        if "scaffold" in expected:
            self.assertEqual(result.prepared.scaffold_bytes, expected["scaffold"].encode("utf-8"))
        if "keyword" in expected:
            row = result.prepared.vals[0]
            for field in ("keyword", "target", "statement"):
                if field in expected:
                    self.assertEqual(getattr(row, field), sm.ByteSpan(*expected[field]))
        if "copied_segment" in expected:
            self.assertEqual(result.prepared.scaffold_map.segments,
                             (sm.MapSegment(*expected["copied_segment"], "copy"),))
        if "prepared_edition" in expected:
            self.assertEqual(result.prepared.edition, expected["prepared_edition"])
            self.assertEqual(result.prepared.selected_edition, expected["selected_edition"])
        if expected.get("no_lowered_output") and result.prepared is not None:
            lowered = sx.lower_source(result.prepared)
            self.assertEqual(lowered.status, 1)
            self.assertIsNone(lowered.translation)
        return result

    def _translate(self, case):
        result = sx.translate_source(_raw(case), _owner(case), edition=case.get("edition", sm.EDITION),
                                     translator=TRANSLATOR, empty_types=_rows(case))
        expected = case["expected"]
        self._expected(result, expected)
        if result.status:
            self.assertIsNone(result.translation)
            return result
        translation = result.translation
        self.assertIsNotNone(translation)
        if "lowered" in expected:
            self.assertEqual(translation.lowered_bytes, expected["lowered"].encode("utf-8"))
        if "used_collections" in expected:
            self.assertEqual(translation.used_collections, tuple(expected["used_collections"]))
        _wire_check(translation.lowered_map, _raw(case), translation.lowered_bytes)
        return result

    def _format(self, case):
        result = sx.format_source(_raw(case), _owner(case), edition=case.get("edition", sm.EDITION),
                                  translator=TRANSLATOR, empty_types=_rows(case))
        expected = case["expected"]
        self.assertEqual((result.status, result.source_status), (expected["format_status"], expected["source_status"]))
        if "after" in expected:
            self.assertEqual(result.after, None if expected["after"] is None else expected["after"].encode("utf-8"))
        if "rule" in expected:
            self.assertEqual(result.issues[0].rule, expected["rule"])
        if result.status == 2:
            self.assertIsNone(result.after)
            self.assertEqual(result.edits, ())
            self.assertIsNone(result.source_map)
        else:
            _wire_check(result.source_map, _raw(case), result.after)
            if "edits" in expected:
                self.assertEqual(result.edits, tuple(sx.FormatEdit(sm.ByteSpan(*row["span"]), row["replacement"].encode("utf-8"))
                                                     for row in expected["edits"]))
            rows = []
            for row in _rows(case):
                mapped = sm.generated_ranges(result.source_map, row.span, source=_raw(case), generated=result.after)
                self.assertEqual(len(mapped), 1)
                rows.append(sx.EmptyDisplayType(mapped[0], row.family, row.schema))
            second = sx.format_source(result.after, _owner(case), edition=case.get("edition", sm.EDITION),
                                      translator=TRANSLATOR, empty_types=tuple(rows))
            self.assertEqual(second.status, 0)
            self.assertEqual(second.after, result.after)
        return result

    def test_prepare_val_scaffold(self):
        for case in CASES["test_prepare_val_scaffold"]:
            with self.subTest(source=case["source"]):
                self._prepare(case)

    def test_prepare_val_forms(self):
        for case in CASES["test_prepare_val_forms"]:
            with self.subTest(source=case["source"]):
                self._prepare(case)
        # Added from root source review; original170 descriptors stay literal.
        result = sx.prepare_source(b"val fn = lambda x=1: x\n", OWNER, edition=sm.EDITION, translator=TRANSLATOR)
        self.assertEqual(result.status, 0)
        self.assertEqual(result.prepared.scaffold_bytes, b"fn = lambda x=1: x\n")
        self.assertIs(type(ast.parse(result.prepared.scaffold_bytes).body[0].value), ast.Lambda)

    def test_valid_reserved_names(self):
        for case in CASES["test_valid_reserved_names"]:
            with self.subTest(source=case["source"]):
                self._prepare(case)

    def test_nfkc_collisions(self):
        for case in CASES["test_nfkc_collisions"]:
            with self.subTest(source=case["source"]):
                result = self._prepare(case)
                if "ast_identifier" in case["expected"]:
                    node = ast.parse(result.prepared.scaffold_bytes).body[0]
                    self.assertEqual(node.targets[0].id, case["expected"]["ast_identifier"])
                    self.assertIn("café".encode("utf-8"), result.prepared.scaffold_bytes)

    def test_malformed_val_headers(self):
        for case in CASES["test_malformed_val_headers"]:
            with self.subTest(source=case["source"]):
                self._prepare(case)

    def test_malformed_val_contexts(self):
        for case in CASES["test_malformed_val_contexts"]:
            with self.subTest(source=case["source"]):
                self._prepare(case)

    def test_encoding_profile(self):
        for case in CASES["test_encoding_profile"]:
            with self.subTest(case=case):
                result = self._prepare(case)
                if case["expected"].get("authored_bom_hashed"):
                    self.assertEqual(result.prepared.authored_bytes, _raw(case))
                    self.assertNotEqual(result.prepared.scaffold_map.source.sha256, result.prepared.scaffold_map.generated.sha256)

    def test_token_parser_precedence(self):
        for case in CASES["test_token_parser_precedence"]:
            with self.subTest(source=case["source"]):
                if "EOF" in case["expected"]["stock_baseline"]:
                    with self.assertRaises(tokenize.TokenError) as observed:
                        list(tokenize.generate_tokens(io.StringIO(case["source"]).readline))
                    self.assertEqual(observed.exception.args, ("unexpected EOF in multi-line statement", (1, 0)))
                else:
                    scaffold = "x = 1\n_py alamode = 2\n"
                    with self.assertRaises(SyntaxError) as observed:
                        ast.parse(scaffold, feature_version=(3, 13))
                    self.assertEqual((observed.exception.lineno, observed.exception.offset,
                                      observed.exception.end_lineno, observed.exception.end_offset), (2, 5, 2, 12))
                # Independently assert the unchanged authored oracles: API03's
                # explicit EOF exception is rawEOF10/28, not stock start0.
                self._prepare(case)

    def test_disabled_edition(self):
        for case in CASES["test_disabled_edition"]:
            with self.subTest(case=case):
                self._prepare(case)

    def test_protected_text_bytes(self):
        for case in CASES["test_protected_text_bytes"]:
            with self.subTest(source=case["source"]):
                self._translate(case)

    def test_literal_constructors(self):
        for case in CASES["test_literal_constructors"]:
            with self.subTest(source=case["source"]):
                self._translate(case)

    def test_nested_display_order(self):
        for case in CASES["test_nested_display_order"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                tree = ast.parse(result.translation.lowered_bytes)
                if "ast_child_order" in case["expected"]:
                    call = tree.body[-1].value
                    self.assertEqual([ast.unparse(child) for child in call.args], case["expected"]["ast_child_order"])
                else:
                    original = tree.body[-1].value.args[0]
                    self.assertEqual([ast.unparse(pair.elts[1]) for pair in original.args], case["expected"]["ast_call_order"])

    def test_runtime_value_contexts(self):
        for case in CASES["test_runtime_value_contexts"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                tree = ast.parse(result.translation.lowered_bytes)
                families = [node.func.value.id.removeprefix("_pyalamode_syntax_") for node in ast.walk(tree)
                            if type(node) is ast.Call and type(node.func) is ast.Attribute
                            and type(node.func.value) is ast.Name and node.func.value.id.startswith("_pyalamode_syntax_")]
                if "expected_call_families" in case["expected"]:
                    self.assertCountEqual(families, case["expected"]["expected_call_families"])
                else:
                    self.assertEqual(families, ["Vector"])
                    self.assertEqual(ast.unparse(tree.body[-1].cases[0].pattern), "True")
                if case["expected"].get("import_before_decorator"):
                    self.assertLess(result.translation.lowered_bytes.index(b"from pyalamode"), result.translation.lowered_bytes.index(b"@decorate"))

    def test_annotation_subscript_pattern_exclusions(self):
        for case in CASES["test_annotation_subscript_pattern_exclusions"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                raw = result.translation.lowered_bytes
                if case["expected"].get("annotation_lists_preserved"):
                    self.assertIn(b"Callable[[int], int]", raw)
                    self.assertIn(b"Effectful[[int], int, IO]", raw)
                    self.assertIn(b"xs[0]", raw)
                if case["expected"].get("type_parameters_preserved"):
                    self.assertEqual(raw, _raw(case))

    def test_unsupported_display_forms(self):
        for case in CASES["test_unsupported_display_forms"]:
            with self.subTest(source=case["source"]):
                self._translate(case)

    def test_empty_display_feedback(self):
        for case in CASES["test_empty_display_feedback"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                if case["expected"].get("explicit_compatible_unchanged"):
                    self.assertEqual(result.translation.lowered_bytes, _raw(case).replace(b"val ", b""))

    def test_empty_direct_contexts(self):
        for case in CASES["test_empty_direct_contexts"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                self.assertEqual(result.translation.empty_types, _rows(case))

    def test_empty_alias_qualified_nested(self):
        for case in CASES["test_empty_alias_qualified_nested"]:
            with self.subTest(source=case["source"]):
                self._translate(case)

    def test_empty_whole_quoted_annotations(self):
        for case in CASES["test_empty_whole_quoted_annotations"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                output = result.translation.lowered_bytes
                self.assertIn(case["expected"]["compatible_initializer"].encode("utf-8"), output)
                tree = ast.parse(output)
                assignment = tree.body[-1]
                self.assertIs(type(assignment.annotation), ast.Constant)
                argument = assignment.value.func.value.slice
                mapped = sm.map_range(result.translation.lowered_map, _span(argument, output), source=_raw(case), generated=output)
                self.assertEqual(mapped.source_span, sm.ByteSpan(*case["expected"]["generated_argument_anchor"]))
                self.assertFalse(mapped.exact)
                self.assertEqual(ast.unparse(assignment.annotation), ast.unparse(ast.parse(result.translation.prepared.scaffold_bytes).body[-1].annotation))

    def test_empty_inner_quoted_and_unrenderable(self):
        for case in CASES["test_empty_inner_quoted_and_unrenderable"]:
            with self.subTest(source=case["source"]):
                self._translate(case)

    def test_invalid_empty_context_rows(self):
        for case in CASES["test_invalid_empty_context_rows"]:
            with self.subTest(case=case):
                if "exception" in case["expected"]:
                    with self.assertRaises(sm.SourceMapError):
                        sx.translate_source(_raw(case), OWNER, edition=sm.EDITION, translator=TRANSLATOR, empty_types=_rows(case))
                else:
                    # Deliberately caller-claimed schema; this is not a certificate.
                    raw = _raw(case)
                    row = sx.EmptyDisplayType(sm.ByteSpan(len(raw) - 3, len(raw) - 1), "Vector", "Vector[int]")
                    result = sx.translate_source(raw, OWNER, edition=sm.EDITION, translator=TRANSLATOR, empty_types=(row,))
                    self.assertEqual(result.status, 0)
                    self.assertIn(b"_pyalamode_syntax_Vector[Unknown].of()", result.translation.lowered_bytes)
                    self.assertFalse(hasattr(result.translation, "checked_contract"))
        # Root source-review addition: claimed canonical schemas are finite data.
        with self.assertRaises(sm.SourceMapError):
            sx.translate_source(b"val xs: Vector[int] = []\n", OWNER, edition=sm.EDITION, translator=TRANSLATOR,
                                empty_types=(sx.EmptyDisplayType(sm.ByteSpan(22, 24), "Vector", "Vector[call()]"),))

    def test_forged_prepared_records(self):
        original = sx.prepare_source(b"val x = 1\n", OWNER, edition=sm.EDITION, translator=TRANSLATOR).prepared
        reserved = sx.prepare_source(b"val = 1\n", OWNER, edition=sm.EDITION, translator=TRANSLATOR).prepared
        changed = b"x = 2\n"
        forged_map = _map(b"val x = 1\n", changed, [[0, len(changed), 0, 9, "anchor"]], generated_role="scaffold")
        mutants = [
            replace(original, authored_text="val x = 2\n"),
            replace(original, scaffold_bytes=changed, scaffold_map=forged_map),
            replace(original, vals=(replace(original.vals[0], target=sm.ByteSpan(0, 3)),)),
            replace(reserved, issues=()),
            replace(original, selected_edition="python-v1"),
            replace(original, vals=[original.vals[0]]),
        ]
        for case, mutant in zip(CASES["test_forged_prepared_records"], mutants):
            with self.subTest(case=case):
                with self.assertRaises(sm.SourceMapError):
                    sx.lower_source(mutant)
        with self.assertRaises(sm.SourceMapError):
            sx.lower_source(replace(original, vals=(replace(original.vals[0], target=sm.ByteSpan(True, 5)),)))

    def test_scaffold_mapping_unicode(self):
        case = CASES["test_scaffold_mapping_unicode"][0]
        raw = _raw(case)
        result = sx.prepare_source(raw, OWNER, edition=sm.EDITION, translator=TRANSLATOR)
        self.assertEqual(result.status, 0)
        self.assertIsNotNone(result.prepared)
        output = result.prepared.scaffold_bytes
        self.assertEqual(output, case["expected"]["scaffold"].encode("utf-8"))
        for field in ("keyword", "target"):
            self.assertEqual(getattr(result.prepared.vals[0], field), sm.ByteSpan(*case["expected"][field]))
        self.assertEqual((len(raw), len(output)), (41, 34))
        for key in ("whole_scaffold_query", "target_query"):
            row = case["expected"][key]
            mapped = sm.map_range(result.prepared.scaffold_map, sm.ByteSpan(*row["generated_span"]), source=raw, generated=output)
            self.assertEqual(mapped.source_span, sm.ByteSpan(*row["source_span"]))
            self.assertIs(mapped.exact, row["exact"])

    def test_constructor_import_header(self):
        for case in CASES["test_constructor_import_header"]:
            with self.subTest(source=case["source"]):
                result = self._translate(case)
                output = result.translation.lowered_bytes
                expected = case["expected"]
                if "import_anchor" in expected:
                    start = output.index(b"from pyalamode")
                    stop = output.index(b"@fun")
                    mapped = sm.map_range(result.translation.lowered_map, sm.ByteSpan(start, stop), source=_raw(case), generated=output)
                    self.assertEqual(mapped.source_span, sm.ByteSpan(*expected["import_anchor"]))
                    self.assertFalse(mapped.exact)
                    self.assertIn(b"# header\nfrom pyalamode", output)
                if "generated_import_newline" in expected:
                    self.assertIn(b"_pyalamode_syntax_Set\r\n", output)
                    self.assertTrue(output.startswith(b"# coding: utf-8\r\n# mode: fun\r\n"))
                if "import_order" in expected:
                    lines = [line.decode("ascii") for line in output.splitlines() if line.startswith(b"from pyalamode")]
                    self.assertEqual(lines, ["from pyalamode import " + family + " as _pyalamode_syntax_" + family for family in expected["import_order"]])

    def _positions(self, case):
        raw = _raw(case)
        for row in case["positions"]:
            observed = sm.position_at(raw, row["offset"])
            for key in ("line", "column", "utf16_column"):
                if key in row:
                    self.assertEqual(getattr(observed, key), row[key])
            expected_offset = 3 if row["offset"] == 0 and raw.startswith(b"\xef\xbb\xbf") else row["offset"]
            self.assertEqual(sm.offset_at(raw, observed.line, observed.column), expected_offset)
            self.assertEqual(sm.offset_at(raw, observed.line, observed.utf16_column, encoding="utf-16"), expected_offset)

    def test_positions_utf8_utf16(self):
        self._positions(CASES["test_positions_utf8_utf16"][0])

    def test_physical_line_endings(self):
        for case in CASES["test_physical_line_endings"]:
            with self.subTest(raw=case["raw"]):
                self._positions(case)

    def test_bom_cookie_eof(self):
        for case in CASES["test_bom_cookie_eof"]:
            with self.subTest(case=case):
                if "positions" in case:
                    self._positions(case)
                else:
                    result = self._prepare(case)
                    self.assertEqual(len(_raw(case)), 25)
                    self.assertEqual(sm.position_at(_raw(case), 25).byte_offset, 25)
                    self.assertEqual(result.prepared.authored_bytes, _raw(case))

    def test_invalid_coordinates(self):
        for case in CASES["test_invalid_coordinates"]:
            raw = _raw(case)
            for offset in case.get("invalid_offsets", []):
                with self.subTest(offset=offset), self.assertRaises(sm.SourceMapError):
                    sm.position_at(raw, offset)
            for encoding, key in (("utf-16", "invalid_utf16_columns"), ("utf-8-bytes", "invalid_utf8_columns")):
                for column in case.get(key, []):
                    with self.subTest(encoding=encoding, column=column), self.assertRaises(sm.SourceMapError):
                        sm.offset_at(raw, 1, column, encoding=encoding)
            for line in case.get("invalid_lines", []):
                with self.assertRaises(sm.SourceMapError):
                    sm.offset_at(raw, line, 1)
            if "invalid_encoding" in case:
                with self.assertRaises(sm.SourceMapError):
                    sm.offset_at(raw, 1, 1, encoding=case["invalid_encoding"])

    def test_closed_wire_types(self):
        raw = b"x = 1\n"
        value = _map(raw, raw, [[0, 6, 0, 6, "copy"]])
        original = sm.map_to_dict(value)
        mutations = [
            lambda row: row.update(extra=0),
            lambda row: row.pop("coordinate_encoding"),
            lambda row: row.update(schema=True),
            lambda row: row.update(kind="other"),
            lambda row: row["owner"].update(extra=0),
            lambda row: row["translator"]["files"].update({"pyalamode/syntax.py": row["translator"]["files"].pop("syntax.py")}),
            lambda row: row["source"].update(sha256="A" * 64),
            lambda row: row["source"].update(byte_count=True),
            lambda row: row.update(segments=tuple(row["segments"])),
        ]
        for label, mutation in zip(CASES["test_closed_wire_types"][0]["mutations"], mutations):
            with self.subTest(label=label):
                row = copy.deepcopy(original)
                mutation(row)
                with self.assertRaises(sm.SourceMapError):
                    _wire_check(value, raw, raw, row)
        with self.assertRaises(sm.SourceMapError):
            _wire_check(value, raw, raw, ForeignMap(original))
        self.assertEqual(set(original), set(CASES["test_closed_wire_types"][1]["expected_top_keys"]))
        self.assertEqual(set(original["translator"]["files"]), {"source_maps.py", "syntax.py"})
        original["owner"]["module"] = "changed"
        original["segments"][0]["source_start"] = 1
        self.assertEqual(value.owner, OWNER)
        self.assertEqual(value.segments[0].source_start, 0)

    def test_map_ownership_coverage_validation(self):
        raw = b"abcd"
        value = _map(raw, raw, [[0, 4, 0, 4, "copy"]])
        for path in ("/unit.pya", "../unit.pya", "a\\unit.pya", "a:unit.pya", "a\x00unit.pya", "a//unit.pya"):
            with self.subTest(path=path), self.assertRaises(sm.SourceMapError):
                sm.map_to_dict(replace(value, owner=sm.SourceOwner(path, "unit.py", "unit")))
        for module in ("class", "ｕnit", "unit..child"):
            with self.subTest(module=module), self.assertRaises(sm.SourceMapError):
                sm.map_to_dict(replace(value, owner=replace(OWNER, module=module)))
        for mutant in (
            replace(value, owner=replace(OWNER, runtime_path="other.py")),
            replace(value, source=replace(value.source, sha256="3" * 64)),
            replace(value, generated=replace(value.generated, sha256="3" * 64)),
            replace(value, generated=replace(value.generated, role="authored")),
            replace(value, segments=(sm.MapSegment(1, 4, 0, 3, "copy"),)),
            replace(value, segments=(sm.MapSegment(0, 0, 0, 0, "anchor"),)),
            replace(value, segments=(sm.MapSegment(0, 4, 0, 3, "copy"),)),
            replace(value, segments=(sm.MapSegment(0, 4, 0, 5, "anchor"),)),
        ):
            with self.subTest(mutant=mutant), self.assertRaises(sm.SourceMapError):
                _wire_check(mutant, raw, raw)
        with self.assertRaises(sm.SourceMapError):
            _wire_check(value, raw, raw, translator=replace(TRANSLATOR, files=(("source_maps.py", "3" * 64), ("syntax.py", "2" * 64))))
        unequal = _map(b"abcd", b"abce", [[0, 4, 0, 4, "copy"]])
        with self.assertRaises(sm.SourceMapError):
            _wire_check(unequal, b"abcd", b"abce")
        unicode = "é".encode()
        scalar = _map(unicode, b"x", [[0, 1, 1, 2, "anchor"]])
        with self.assertRaises(sm.SourceMapError):
            _wire_check(scalar, unicode, b"x")

    def _range_cases(self, name):
        for case in CASES[name]:
            with self.subTest(case=case):
                source, generated = case["source"].encode(), case["generated"].encode()
                value = _map(source, generated, case["segments"])
                if "query" in case:
                    observed = sm.map_range(value, sm.ByteSpan(*case["query"]), source=source, generated=generated)
                    self.assertEqual(observed.source_span, sm.ByteSpan(*case["expected"]["source_span"]))
                    self.assertIs(observed.exact, case["expected"]["exact"])
                    if "segments" in case["expected"]:
                        self.assertEqual(observed.segments, tuple(case["expected"]["segments"]))
                else:
                    observed = sm.generated_ranges(value, sm.ByteSpan(*case["reverse_query"]), source=source, generated=generated)
                    self.assertEqual(observed, tuple(sm.ByteSpan(*row) for row in case["expected"]["generated_ranges"]))

    def test_range_exactness(self):
        self._range_cases("test_range_exactness")

    def test_zero_range_reverse_occurrences(self):
        self._range_cases("test_zero_range_reverse_occurrences")

    def _composition_cases(self, name):
        for case in CASES[name]:
            with self.subTest(case=case):
                source, intermediate, generated = (case[key].encode() for key in ("source", "intermediate", "generated"))
                inner = _map(source, intermediate, case["inner"], generated_role="scaffold")
                outer = _map(intermediate, generated, case["outer"], source_role="scaffold")
                observed = sm.compose_maps(inner, outer, source=source, intermediate=intermediate, generated=generated)
                self.assertEqual(observed.segments, tuple(sm.MapSegment(*row) for row in case["expected"]["segments"]))
                _wire_check(observed, source, generated)
                if "whole_exact" in case["expected"]:
                    self.assertIs(sm.map_range(observed, sm.ByteSpan(0, len(generated)), source=source, generated=generated).exact, case["expected"]["whole_exact"])

    def test_composition_copy_splits(self):
        self._composition_cases("test_composition_copy_splits")

    def test_composition_anchor_hulls(self):
        self._composition_cases("test_composition_anchor_hulls")

    def test_composition_refusals(self):
        source, intermediate, generated = b"ab", b"ab", b"(ab)"
        inner = _map(source, intermediate, [[0, 2, 0, 2, "copy"]], generated_role="scaffold")
        outer = _map(intermediate, generated, [[0, 1, 0, 0, "anchor"], [1, 3, 0, 2, "copy"], [3, 4, 2, 2, "anchor"]], source_role="scaffold")
        mutants = [
            replace(outer, source=replace(outer.source, sha256="3" * 64)),
            replace(outer, owner=sm.SourceOwner("other.pya", "other.py", "other")),
            replace(outer, translator=replace(TRANSLATOR, files=(("source_maps.py", "3" * 64), ("syntax.py", "2" * 64)))),
            replace(outer, source=replace(outer.source, path="unit.pya", edition=sm.EDITION, role="formatted")),
        ]
        for mutant in mutants:
            with self.assertRaises(sm.SourceMapError):
                sm.compose_maps(inner, mutant, source=source, intermediate=intermediate, generated=generated)
        with self.assertRaises(sm.SourceMapError):
            sm.compose_maps(inner, outer, source=source, intermediate=b"ac", generated=generated)
        with patch.object(sm, "MAX_SEGMENTS", 2), self.assertRaises(sm.SourceMapError):
            sm.compose_maps(inner, outer, source=source, intermediate=intermediate, generated=generated)

    def test_derive_preserved_children(self):
        for case in CASES["test_derive_preserved_children"]:
            with self.subTest(source=case["source"]):
                raw = case["source"].encode()
                tree = ast.parse(raw)
                before = _fields(tree)
                origins = _origins(tree, raw)
                original_origins = dict(origins)
                result = _derive(raw, tree, origins)
                self.assertEqual(result.generated_bytes, case["expected_generated"].encode())
                self.assertEqual(_fields(tree), before)
                self.assertEqual(origins, original_origins)
                self.assertEqual(_fields(ast.parse(result.generated_bytes)), before)
                _wire_check(result.source_map, raw, result.generated_bytes)
                for node in ast.walk(ast.parse(result.generated_bytes)):
                    if type(node) is ast.Name and node.id == "x":
                        self.assertTrue(sm.map_range(result.source_map, _span(node, result.generated_bytes), source=raw, generated=result.generated_bytes).exact)

    def test_derive_debug_return_argument(self):
        raw = CASES["test_derive_debug_return_argument"][0]["source"].encode()
        tree = ast.parse(raw)
        tags = {id(node): sm.NodeOrigin(_span(node, raw), "copy") for node in ast.walk(tree) if _positioned(node)}
        function, original = tree.body[0], tree.body[0].body[0]
        argument = _span(function.args.args[0], raw)
        returned = _span(original, raw)
        arg_guard = _anchor(ast.parse("assert x is not None").body[0], argument, tags)
        assignment = _anchor(ast.Assign(targets=[ast.Name(id="_result", ctx=ast.Store())], value=ast.Constant(value=None)), returned, tags)
        assignment.value = original.value
        guard = _anchor(ast.parse("assert _result is not None").body[0], returned, tags)
        exit_node = _anchor(ast.Return(value=ast.Name(id="_result", ctx=ast.Load())), returned, tags)
        function.body = [arg_guard, assignment, guard, exit_node]
        ast.fix_missing_locations(tree)
        result = _derive(raw, tree, _origins(tree, raw, tags))
        generated = ast.parse(result.generated_bytes)
        self.assertEqual(_fields(generated), _fields(tree))
        moved = generated.body[0].body[1].value
        for child in (moved.left, moved.right):
            self.assertTrue(sm.map_range(result.source_map, _span(child, result.generated_bytes), source=raw, generated=result.generated_bytes).exact)
        observed = sm.map_range(result.source_map, _span(generated.body[0].body[0], result.generated_bytes), source=raw, generated=result.generated_bytes)
        self.assertEqual(observed.source_span, argument)
        self.assertFalse(observed.exact)
        _wire_check(result.source_map, raw, result.generated_bytes)

    def test_derive_facade_fields(self):
        raw = CASES["test_derive_facade_fields"][0]["source"].encode()
        original = ast.parse(raw)
        full = sm.ByteSpan(0, len(raw))
        tree = ast.parse("import p as _module\n_original = _module.f\ndef f(x=1, *, y=2):\n    validate(x, path='x')\n    result = _original(x, y=y)\n    return result\n")
        tags = {}
        _anchor(tree, full, tags)
        old_function, function = original.body[0], tree.body[-1]
        tags[id(function)] = sm.NodeOrigin(_span(old_function, raw), "anchor")
        function.args.defaults = old_function.args.defaults
        function.args.kw_defaults = old_function.args.kw_defaults
        for node in function.args.defaults + function.args.kw_defaults:
            tags[id(node)] = sm.NodeOrigin(_span(node, raw), "copy")
        origins = _origins(tree, raw, tags)
        result = _derive(raw, tree, origins)
        self.assertEqual(_fields(ast.parse(result.generated_bytes)), _fields(tree))
        _wire_check(result.source_map, raw, result.generated_bytes)
        missing = dict(origins)
        missing.pop(("body", 2, "args", "args", 0))
        with self.assertRaises(sm.SourceMapError):
            _derive(raw, tree, missing)

    def test_derive_finite_allowed_shapes(self):
        observed = set()
        for case in CASES["test_derive_finite_allowed_shapes"]:
            with self.subTest(source=case["source"]):
                raw = case["source"].encode()
                tree = ast.parse(raw)
                observed.update(type(node).__name__ for node in ast.walk(tree))
                result = _derive(raw, tree)
                self.assertEqual(_fields(ast.parse(result.generated_bytes)), _fields(tree))
                _wire_check(result.source_map, raw, result.generated_bytes)
        self.assertTrue({"Try", "ExceptHandler", "withitem", "match_case", "MatchClass", "MatchMapping", "MatchOr", "MatMult", "USub", "NotIn"} <= observed)

    def test_derive_topology_fail_closed(self):
        raw = b"x = 1\n"
        mutations = [ast.Constant(value=-1), ast.Constant(value=(1, 2)), ast.Set(elts=[]),
                     ast.Constant(value=float("nan")), ast.Constant(value=float("inf"))]
        for node in mutations:
            tree = ast.Module(body=[ast.Expr(value=node)], type_ignores=[])
            ast.fix_missing_locations(tree)
            origins = {path: sm.NodeOrigin(sm.ByteSpan(0, 5), "anchor") for path, child in _paths(tree) if _positioned(child)}
            with self.subTest(node=type(node).__name__), self.assertRaises(sm.SourceMapError):
                _derive(raw, tree, origins)
        for text in ("lambda: 1", "for x in y:\n    pass", "async def f():\n    pass", "(x := 1)", "def f():\n    yield 1", "f'{x}'"):
            tree = ast.parse(text)
            origins = {path: sm.NodeOrigin(sm.ByteSpan(0, 5), "anchor") for path, child in _paths(tree) if _positioned(child)}
            with self.subTest(text=text), self.assertRaises(sm.SourceMapError):
                _derive(raw, tree, origins)
        class ForeignNode(ast.Name):
            pass
        for node in (ForeignNode(id="x", ctx=ast.Load()), ast.Constant(value=Foreign())):
            tree = ast.Module(body=[ast.Expr(value=node)], type_ignores=[])
            ast.fix_missing_locations(tree)
            origins = {path: sm.NodeOrigin(sm.ByteSpan(0, 5), "anchor") for path, child in _paths(tree) if _positioned(child)}
            with self.assertRaises(sm.SourceMapError):
                _derive(raw, tree, origins)
        self.assertEqual(Foreign.calls, [])
        # Root source-review addition: malformed exact-stock container layout.
        tree = ast.Module(body=[ast.Try(body=[ast.Pass()], handlers=[Foreign()], orelse=[], finalbody=[])], type_ignores=[])
        with self.assertRaises(sm.SourceMapError):
            _derive(raw, tree, {(): sm.NodeOrigin(sm.ByteSpan(0, 6), "anchor")})
        self.assertEqual(Foreign.calls, [])

    def test_derive_origin_validation(self):
        raw = "x = '😀'\n".encode()
        original = ast.parse(raw)
        origins = _origins(original, raw)
        for label in CASES["test_derive_origin_validation"][0]["mutations"]:
            tree, rows = copy.deepcopy(original), dict(origins)
            if label == "missing root":
                rows.pop(())
            elif label == "missing positioned child":
                rows.pop(("body", 0, "value"))
            elif label == "unknown structural path":
                rows[("missing",)] = sm.NodeOrigin(sm.ByteSpan(0, 0), "anchor")
            elif label == "index true/-1":
                rows[("body", True)] = sm.NodeOrigin(sm.ByteSpan(0, 0), "anchor")
            elif label == "wrong copy byte extent":
                rows[("body", 0, "value")] = sm.NodeOrigin(sm.ByteSpan(0, 1), "copy")
            elif label == "span inside astral scalar":
                rows[("body", 0, "value")] = sm.NodeOrigin(sm.ByteSpan(6, 7), "anchor")
            elif label == "origin foreign subclass":
                class ForeignOrigin(sm.NodeOrigin):
                    pass
                rows[()] = ForeignOrigin(sm.ByteSpan(0, len(raw)), "copy")
            elif label == "foreign AST field value":
                tree.body[0].value.value = Foreign()
            else:
                tree.body[0].extra = 1
            with self.subTest(label=label), self.assertRaises(sm.SourceMapError):
                _derive(raw, tree, rows)
        self.assertEqual(Foreign.calls, [])
        before = (_fields(original), dict(origins), raw)
        _derive(raw, original, origins)
        self.assertEqual((_fields(original), origins, raw), before)

    def test_formatter_safe_edits(self):
        for case in CASES["test_formatter_safe_edits"]:
            with self.subTest(source=case["source"]):
                self._format(case)

    def test_formatter_protected_bytes(self):
        for case in CASES["test_formatter_protected_bytes"]:
            with self.subTest(source=case["source"]):
                self._format(case)

    def test_formatter_rebases_empty_rows(self):
        for case in CASES["test_formatter_rebases_empty_rows"]:
            with self.subTest(source=case["source"]):
                result = self._format(case)
                row = _rows(case)[0]
                rebased = sm.generated_ranges(result.source_map, row.span, source=_raw(case), generated=result.after)
                if "rebased_context" in case["expected"]:
                    self.assertEqual(rebased, (sm.ByteSpan(*case["expected"]["rebased_context"]["span"]),))
                translated = sx.translate_source(result.after, OWNER, edition=sm.EDITION, translator=TRANSLATOR,
                                                  empty_types=(sx.EmptyDisplayType(rebased[0], row.family, row.schema),))
                self.assertEqual(translated.status, 0)

    def test_formatter_status_axes(self):
        for case in CASES["test_formatter_status_axes"]:
            with self.subTest(source=case["source"]):
                self._format(case)

    def test_bounds_and_exact_argument_types(self):
        with self.assertRaises(sm.SourceMapError):
            sx.prepare_source(b" " * 1048577, OWNER, edition=sm.EDITION, translator=TRANSLATOR)
        with self.assertRaises(sm.SourceMapError):
            sx.prepare_source(b"x;" * 50001 + b"\n", OWNER, edition=sm.EDITION, translator=TRANSLATOR)
        raw = b"x = 1\n"
        # Root source-review addition: <100000 AST nodes/plain-field bounds,
        # but actual generated import tokens exceed100000 before reparse.
        generated_overflow = ast.Module(body=[ast.ImportFrom(module="p", names=[ast.alias(name="a", asname=None)], level=0)
                                             for _ in range(20000)], type_ignores=[])
        origins = {path: sm.NodeOrigin(sm.ByteSpan(0, 6), "anchor") for path, node in _paths(generated_overflow) if _positioned(node)}
        with self.assertRaises(sm.SourceMapError):
            _derive(raw, generated_overflow, origins)
        tree = ast.Module(body=[ast.Pass() for _ in range(100001)], type_ignores=[])
        with self.assertRaises(sm.SourceMapError):
            _derive(raw, tree, {(): sm.NodeOrigin(sm.ByteSpan(0, 6), "anchor")})
        child = ast.Name(id="x", ctx=ast.Load())
        for index in range(257):
            child = ast.UnaryOp(op=ast.USub(), operand=child)
        tree = ast.Module(body=[ast.Expr(value=child)], type_ignores=[])
        with self.assertRaises(sm.SourceMapError):
            _derive(raw, tree, {(): sm.NodeOrigin(sm.ByteSpan(0, 6), "anchor")})
        value = _map(raw, raw, [[0, 6, 0, 6, "copy"]])
        with self.assertRaises(sm.SourceMapError):
            sm.map_to_dict(replace(value, segments=(sm.MapSegment(0, 1, 0, 1, "copy"),) * 200001))
        with self.assertRaises(sm.SourceMapError):
            sm.source_identity(b" " * 8388609, path="unit.py", edition="python-v1", role="lowered")
        with patch.object(sm, "MAX_MAP_BYTES", 1), self.assertRaises(sm.SourceMapError):
            sm.map_to_dict(value)
        for raw_bad in (bytearray(raw), raw.decode(), Foreign()):
            with self.assertRaises(sm.SourceMapError):
                sx.prepare_source(raw_bad, OWNER, edition=sm.EDITION, translator=TRANSLATOR)
        with self.assertRaises(sm.SourceMapError):
            sm.position_at(raw, True)
        with self.assertRaises(sm.SourceMapError):
            sx.translate_source(raw, OWNER, edition=sm.EDITION, translator=TRANSLATOR, empty_types=[])
        with self.assertRaises(sm.SourceMapError):
            sx.prepare_source(raw, ForeignOwner("unit.pya", "unit.py", "unit"), edition=sm.EDITION, translator=TRANSLATOR)
        for payload in ("x" * 8388609, 1 << 8388608):
            tree = ast.Module(body=[ast.Expr(value=ast.Constant(value=payload))], type_ignores=[])
            with self.assertRaises(sm.SourceMapError):
                _derive(raw, tree, {(): sm.NodeOrigin(sm.ByteSpan(0, 6), "anchor")})
        tree = ast.Module(body=[ast.Pass()] * 400001, type_ignores=[])
        with self.assertRaises(sm.SourceMapError):
            _derive(raw, tree, {})
        tree = ast.parse(raw)
        for rows in ({(index,): sm.NodeOrigin(sm.ByteSpan(0, 0), "anchor") for index in range(100002)},
                     {("body",) * 513: sm.NodeOrigin(sm.ByteSpan(0, 0), "anchor")}):
            with self.assertRaises(sm.SourceMapError):
                _derive(raw, tree, rows)

    def test_detached_records_and_no_dispatch(self):
        case = CASES["test_detached_records_and_no_dispatch"][0]
        real_import = builtins.__import__
        calls = []
        def guarded_import(name, *arguments, **keywords):
            if name == "os":
                calls.append(name)
                raise AssertionError("authored import dispatched")
            return real_import(name, *arguments, **keywords)
        with patch.object(builtins, "__import__", guarded_import), patch.object(builtins, "exec", side_effect=AssertionError("source executed")), patch.object(builtins, "eval", side_effect=AssertionError("source evaluated")):
            result = self._translate(case)
        self.assertEqual(calls, [])
        self.assertIn(b"foreign()", result.translation.lowered_bytes)
        value = result.translation.lowered_map
        wire = sm.map_to_dict(value)
        validated = _wire_check(value, _raw(case), result.translation.lowered_bytes, wire)
        wire["owner"]["module"] = "other"
        wire["segments"].clear()
        self.assertEqual(validated, value)
        self.assertEqual(validated.owner.module, "unit")
        with self.assertRaises(FrozenInstanceError):
            validated.owner.module = "other"
        empty = sx.EmptyDisplayType(sm.ByteSpan(22, 24), "Vector", "Vector[int]")
        with self.assertRaises(FrozenInstanceError):
            empty.schema = "Map[str, int]"
        self.assertEqual(Foreign.calls, [])
