"""Detached closed task/setup rows; metadata grants no callable evidence."""
TASK_VERSION = 'pyalamode.tasks-v1'
TASK_ORDERING = 'exact Vector result in input order; controlled callback order is configured permutation; live starts input-index waves with unspecified within-wave execution'
TASK_CANCELLATION = 'controlled cutoff cancels unstarted suffix after successful prefix; live failure cancels later waves; no partial result or rollback'
TASK_FAILURE = 'controlled first scheduled failure; live lowest input-index worker failure in current wave; first coordinator BaseException takes precedence after bounded cleanup'
TASK_LIFETIME = 'synchronous eager call; no task handle escapes; borrowed external views close after each callback; owner thread and one active provider call'
TASK_NAMES = frozenset({'live_tasks', 'task_map', 'controlled_tasks', 'task_map_with'})
TASK_OPERATIONS = frozenset({'task_map', 'task_map_with'})
TASK_SETUPS = frozenset({'live_tasks', 'controlled_tasks'})
TASK_FOUNDATIONS = {
    '_thread': frozenset({'start_joinable_thread', 'get_ident', '_ThreadHandle'}),
    'builtins': frozenset({'sorted', 'ValueError', 'bool', 'range', 'list', 'int', 'min', 'len', 'TypeError', 'object', 'enumerate', 'str', 'type', '__build_class__', 'BaseException', 'tuple', 'any', 'frozenset', '__import__', 'RuntimeError', 'AttributeError'}),
    'sys': frozenset({'addaudithook'}),
}
_OPERATION_ALIASES = {'pyalamode.tasks.task_map': 'task_map',
 'pyalamode.tasks.task_map_with': 'task_map_with',
 'task_map': 'task_map',
 'task_map_with': 'task_map_with',
 'tasks.task_map': 'task_map',
 'tasks.task_map_with': 'task_map_with'}


def operation_contract(name):
    if type(name) is not str:
        return None
    operation = _OPERATION_ALIASES.get(name)
    if operation == 'task_map':
        return {'aliases': 'immutable input/result nested values may be reused; private mutable staging and handles never '
                    'escape; no live result view, retained capability or escaping task handle',
         'approval': 'product-shipped closed foundation; tasks policy, entry effect bounds, external trust and '
                     'ordinary execution assumptions remain separate',
         'behavior': 'live1/controlled caller-thread serial; live2..4 fixed input-index waves with one fresh native '
                     'joinable worker per message; no result until successful completion and cleanup',
         'bounds': {'controlled_schedule': 'exact input-index permutation; finite configured prefix; no arbitrary '
                                           'instruction scheduler',
                    'controlled_size': [0, 256],
                    'live_max_tasks': [1, 256],
                    'native_join_attempts_per_started_handle': 2,
                    'value_quotas': 'inherited data depth/resource behavior; no byte/integer/termination quota',
                    'workers': [1, 4]},
         'callback': {'captures': 'stable data and admitted checked callable captures; no capability, builder, live '
                                  'view, foreign mutable or changing cell',
                      'count': 'once per started message; successful completed batch once per input; bounded '
                               'failure/cancellation omits unstarted suffix/waves',
                      'representation': 'exact FunctionType at runtime; actual fixed '
                                        'signature/captures/dependencies/effects remain checked source or ordinary '
                                        'caller obligations'},
         'cancellation': 'controlled cutoff cancels unstarted suffix after successful prefix; live failure cancels '
                         'later waves; no partial result or rollback',
         'cleanup': 'all started native handles joined on ordinary callback/result failure before propagation; first '
                    'coordinator BaseException retained, failed joins retry once after initial joins; unresolved '
                    'retry permanently revokes provider; no running-thread preemption',
         'complexity': 'O(n) result/message references and callbacks plus complete ingress/each-result/final '
                       'validation and callback work; live workers>1 one native thread per message in '
                       'waves<=workers, O(workers) concurrent handles/stacks; controlled permutation membership '
                       'O(n^2) with n<=256; external loans add inherited lease-chain costs',
         'effects': ['Task', 'callback declared/conditional effect-bound union'],
         'evidence': 'trusted product implementation plus actual callback/source evidence; exact product/core/source '
                     'identities visible; no runtime registry or callable certificate from annotations',
         'failure': 'controlled first scheduled failure; live lowest input-index worker failure in current wave; '
                    'first coordinator BaseException takes precedence after bounded cleanup',
         'failures': ['RecursionError', 'RuntimeError', 'ValueError', 'callback raised-failure bounds'],
         'foundations': ['builtins.AttributeError',
                         'builtins.BaseException',
                         'builtins.RuntimeError',
                         'builtins.TypeError',
                         'builtins.ValueError',
                         'builtins.__build_class__',
                         'builtins.__import__',
                         'builtins.any',
                         'builtins.bool',
                         'builtins.enumerate',
                         'builtins.frozenset',
                         'builtins.int',
                         'builtins.len',
                         'builtins.list',
                         'builtins.min',
                         'builtins.object',
                         'builtins.range',
                         'builtins.sorted',
                         'builtins.str',
                         'builtins.tuple',
                         'builtins.type',
                         '_thread.get_ident private creating-thread ownership token',
                         '_thread._ThreadHandle exact native construction and fixed ident/join/is_done operations',
                         '_thread.start_joinable_thread(callback, handle=exact_handle, daemon=False) pinned native '
                         'creation/bootstrap',
                         'CPython 3.13.1 native GIL/thread-state/start/join/pending-call/audit-event/core and OS '
                         'thread lifetime implementation',
                         'sys.addaudithook analyzed actual registration invalidates task foundation; no runtime '
                         'hidden-hook registry inspection',
                         'object.__new__/__getattribute__/__setattr__ fixed opaque slots',
                         'exact tuple/list private indexing/staging/append/clear/reference copy and exact int '
                         'comparison/arithmetic',
                         'pyalamode.effects.Task/TaskCapability/_Provider/_CAPABILITIES/_FAMILIES/_new/_view/_live/_Lease/_Borrow/borrow',
                         'pyalamode.collections.Vector/_function/_invalid/_validate/_storage/_new',
                         'complete inherited effects/collections/records/domain native and product foundations'],
         'generic_arguments': 'T/R statically established and runtime-erased; ordinary runtime enforces inherited '
                              'deep stable data, not annotation-selected schemas',
         'identity': 'pyalamode.tasks.task_map',
         'implicit_dispatch': 'exact fixed native handles and product FunctionType/data/capability/lease operations '
                              'only; no arbitrary callable/iterator/getter/hash/formatter/annotation/default/capture '
                              'evaluation or runtime purity inference',
         'initialization': {'application_import': 'surrounding ordinary application initialization remains '
                                                  'unchecked; ordinary named setup separately reported',
                            'effects': [],
                            'evidence': 'trusted finite product/native imports, definitions and constants; no worker '
                                        'starts, application callbacks, owner sample or external provider '
                                        'observations at product import',
                            'failures': []},
         'inputs': ['exact live idle creating-thread TaskCapability',
                    'exact FunctionType with checked fixed data T->R contract',
                    'exact recursively stable Vector[T]'],
         'lifetime': 'synchronous eager call; no task handle escapes; borrowed external views close after each '
                     'callback; owner thread and one active provider call',
         'ordering': 'exact Vector result in input order; controlled callback order is configured permutation; live '
                     'starts input-index waves with unspecified within-wave execution',
         'ordinary_invalid_inputs': ['TypeError'],
         'output': 'exact Vector[R] in original message input order after successful callbacks, deep validation and '
                   'cleanup; no partial result on failure/cancellation',
         'owner': 'Pyalamode product',
         'phase': 'checked effectful function body with tasks=true; factories ordinary setup only; no functional '
                  'initialization/default invocation',
         'preconditions': ['exact admitted deeply stable messages/results and actual callback fixed '
                           'signature/effect/dependency/stable-capture evidence',
                           'creating owner thread, one active operation, live enclosing Task and external leases and '
                           'exclusive access to lent external provider',
                           'unchanged product/catalog/native/core dependencies and supported standard GIL runtime; '
                           'no application audit/trace/profile/monitoring hooks introducing unknown behavior; no '
                           'unchecked private forging, fork or interpreter shutdown during operation'],
         'rationale': 'bounded eager stable-message tasks with input-ordered results, explicit failure/cancellation '
                      'and serial external capability lending',
         'runtime': 'CPython 3.13.1 standard GIL macOS arm64/Linux aarch64 UTF8/surrogateescape',
         'scheduling': 'live start requests in input-index waves; within-wave callback entry/completion unspecified; '
                       'no next wave before joins; controlled serial configured permutation',
         'signature': '(TaskCapability, (T)->R, Vector[T], /)->Vector[R]; fixed pure or Effectful callback bound',
         'version': 'pyalamode.tasks-v1'}
    if operation == 'task_map_with':
        return {'aliases': 'immutable input/result nested values may be reused; private mutable staging and handles never '
                    'escape; no live result view, retained capability or escaping task handle',
         'approval': 'product-shipped closed foundation; tasks policy, entry effect bounds, external trust and '
                     'ordinary execution assumptions remain separate',
         'behavior': 'controlled or live1 serial on calling thread; live workers2..4 ValueError before callbacks; '
                     'fresh scoped external borrow per callback and result validation; every view closes on every '
                     'exit',
         'bounds': {'controlled_schedule': 'exact input-index permutation; finite configured prefix; no arbitrary '
                                           'instruction scheduler',
                    'controlled_size': [0, 256],
                    'live_max_tasks': [1, 256],
                    'native_join_attempts_per_started_handle': 2,
                    'value_quotas': 'inherited data depth/resource behavior; no byte/integer/termination quota',
                    'workers': [1, 4]},
         'callback': {'captures': 'stable data and admitted checked callable captures; no capability, builder, live '
                                  'view, foreign mutable or changing cell',
                      'count': 'once per started message; successful completed batch once per input; bounded '
                               'failure/cancellation omits unstarted suffix/waves',
                      'representation': 'exact FunctionType at runtime; actual fixed '
                                        'signature/captures/dependencies/effects remain checked source or ordinary '
                                        'caller obligations'},
         'cancellation': 'controlled cutoff cancels unstarted suffix after successful prefix; live failure cancels '
                         'later waves; no partial result or rollback',
         'cleanup': 'all started native handles joined on ordinary callback/result failure before propagation; first '
                    'coordinator BaseException retained, failed joins retry once after initial joins; unresolved '
                    'retry permanently revokes provider; no running-thread preemption',
         'complexity': 'O(n) result/message references and callbacks plus complete ingress/each-result/final '
                       'validation and callback work; live workers>1 one native thread per message in '
                       'waves<=workers, O(workers) concurrent handles/stacks; controlled permutation membership '
                       'O(n^2) with n<=256; external loans add inherited lease-chain costs',
         'effects': ['Task', 'callback declared/conditional effect-bound union'],
         'evidence': 'trusted product implementation plus actual callback/source evidence; exact product/core/source '
                     'identities visible; no runtime registry or callable certificate from annotations',
         'failure': 'controlled first scheduled failure; live lowest input-index worker failure in current wave; '
                    'first coordinator BaseException takes precedence after bounded cleanup',
         'failures': ['RecursionError',
                      'RuntimeError',
                      'ValueError',
                      'callback raised-failure bounds',
                      'injected capability and borrow failure bounds'],
         'foundations': ['builtins.AttributeError',
                         'builtins.BaseException',
                         'builtins.RuntimeError',
                         'builtins.TypeError',
                         'builtins.ValueError',
                         'builtins.__build_class__',
                         'builtins.__import__',
                         'builtins.any',
                         'builtins.bool',
                         'builtins.enumerate',
                         'builtins.frozenset',
                         'builtins.int',
                         'builtins.len',
                         'builtins.list',
                         'builtins.min',
                         'builtins.object',
                         'builtins.range',
                         'builtins.sorted',
                         'builtins.str',
                         'builtins.tuple',
                         'builtins.type',
                         '_thread.get_ident private creating-thread ownership token',
                         '_thread._ThreadHandle exact native construction and fixed ident/join/is_done operations',
                         '_thread.start_joinable_thread(callback, handle=exact_handle, daemon=False) pinned native '
                         'creation/bootstrap',
                         'CPython 3.13.1 native GIL/thread-state/start/join/pending-call/audit-event/core and OS '
                         'thread lifetime implementation',
                         'sys.addaudithook analyzed actual registration invalidates task foundation; no runtime '
                         'hidden-hook registry inspection',
                         'object.__new__/__getattribute__/__setattr__ fixed opaque slots',
                         'exact tuple/list private indexing/staging/append/clear/reference copy and exact int '
                         'comparison/arithmetic',
                         'pyalamode.effects.Task/TaskCapability/_Provider/_CAPABILITIES/_FAMILIES/_new/_view/_live/_Lease/_Borrow/borrow',
                         'pyalamode.collections.Vector/_function/_invalid/_validate/_storage/_new',
                         'complete inherited effects/collections/records/domain native and product foundations'],
         'generic_arguments': 'T/R statically established and runtime-erased; ordinary runtime enforces inherited '
                              'deep stable data, not annotation-selected schemas',
         'identity': 'pyalamode.tasks.task_map_with',
         'implicit_dispatch': 'exact fixed native handles and product FunctionType/data/capability/lease operations '
                              'only; no arbitrary callable/iterator/getter/hash/formatter/annotation/default/capture '
                              'evaluation or runtime purity inference',
         'initialization': {'application_import': 'surrounding ordinary application initialization remains '
                                                  'unchecked; ordinary named setup separately reported',
                            'effects': [],
                            'evidence': 'trusted finite product/native imports, definitions and constants; no worker '
                                        'starts, application callbacks, owner sample or external provider '
                                        'observations at product import',
                            'failures': []},
         'inputs': ['exact live idle creating-thread TaskCapability',
                    'one exact live '
                    'IOCapability/StateCapability/ClockCapability/RandomCapability/EnvironmentCapability; Task '
                    'excluded',
                    'exact FunctionType with checked fixed Effectful C,T->R contract and corresponding family bound',
                    'exact recursively stable Vector[T]'],
         'lifetime': 'synchronous eager call; no task handle escapes; borrowed external views close after each '
                     'callback; owner thread and one active provider call',
         'ordering': 'exact Vector result in input order; controlled callback order is configured permutation; live '
                     'starts input-index waves with unspecified within-wave execution',
         'ordinary_invalid_inputs': ['TypeError'],
         'output': 'exact Vector[R] in original message input order after successful callbacks, deep validation and '
                   'cleanup; no partial result on failure/cancellation',
         'owner': 'Pyalamode product',
         'phase': 'checked effectful function body with tasks=true; factories ordinary setup only; no functional '
                  'initialization/default invocation',
         'preconditions': ['exact admitted deeply stable messages/results and actual callback fixed '
                           'signature/effect/dependency/stable-capture evidence',
                           'creating owner thread, one active operation, live enclosing Task and external leases and '
                           'exclusive access to lent external provider',
                           'unchanged product/catalog/native/core dependencies and supported standard GIL runtime; '
                           'no application audit/trace/profile/monitoring hooks introducing unknown behavior; no '
                           'unchecked private forging, fork or interpreter shutdown during operation'],
         'rationale': 'bounded eager stable-message tasks with input-ordered results, explicit failure/cancellation '
                      'and serial external capability lending',
         'runtime': 'CPython 3.13.1 standard GIL macOS arm64/Linux aarch64 UTF8/surrogateescape',
         'scheduling': 'caller-thread serial only; live input order or controlled configured permutation; no native '
                       'worker or cross-thread resource loan',
         'signature': '(TaskCapability, C, (C,T)->R, Vector[T], /)->Vector[R]; C exact pre-M13 effect capability '
                      'with corresponding callback family',
         'version': 'pyalamode.tasks-v1'}
    return None


def operation_catalog():
    return [operation_contract('pyalamode.tasks.task_map'), operation_contract('pyalamode.tasks.task_map_with')]
_SETUP_ALIASES = {'controlled_tasks': 'controlled_tasks',
 'live_tasks': 'live_tasks',
 'pyalamode.tasks.controlled_tasks': 'controlled_tasks',
 'pyalamode.tasks.live_tasks': 'live_tasks',
 'tasks.controlled_tasks': 'controlled_tasks',
 'tasks.live_tasks': 'live_tasks'}


def setup_contract(name):
    if type(name) is not str:
        return None
    operation = _SETUP_ALIASES.get(name)
    if operation == 'live_tasks':
        return {'aliases': 'fresh private config/idle status, no stable data claim, caller-thread ownership and sequential '
                    'reuse',
         'behavior': '(workers, /, *, max_tasks=256)->TaskCapability; exact int workers1..4 and max_tasks1..256, '
                     'bool/subclasses TypeError; numeric outside bounds ValueError; fresh private opaque provider, '
                     'creating-thread identity bookkeeping only; no worker starts or external sample',
         'effects': [],
         'evidence': 'statically recognized ordinary provider setup; surrounding ordinary initialization/body '
                     'remains unchecked; runtime TypeError invalid shapes separate',
         'failures': ['ValueError'],
         'identity': 'pyalamode.tasks.live_tasks',
         'policy': 'refused in functional initialization/defaults; ordinary shell only',
         'version': 'pyalamode.tasks-v1'}
    if operation == 'controlled_tasks':
        return {'aliases': 'fresh private provider retaining one exact stable order tuple and fixed cutoff; finite serial '
                    'test coordination, no deterministic arbitrary threads or external observations',
         'behavior': '(order, /, *, cancel_after=None)->TaskCapability; exact tuple permutation range(len(order)) '
                     'with size0..256; exact int members; None/exact-int cutoff0..n; TypeError shape, ValueError '
                     'bounds/duplicate/permutation; invocation n must equal order length; creating-thread identity '
                     'bookkeeping only; no worker starts',
         'effects': [],
         'evidence': 'statically recognized ordinary provider setup; surrounding ordinary initialization/body '
                     'remains unchecked; runtime TypeError invalid shapes separate',
         'failures': ['ValueError'],
         'identity': 'pyalamode.tasks.controlled_tasks',
         'policy': 'refused in functional initialization/defaults; ordinary shell only',
         'version': 'pyalamode.tasks-v1'}
    return None


def setup_catalog():
    return [setup_contract('pyalamode.tasks.live_tasks'), setup_contract('pyalamode.tasks.controlled_tasks')]
