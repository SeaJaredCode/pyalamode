# Separate installed consumer

Use a supported CPython 3.13.1 standard-GIL macOS arm64 or Linux aarch64 environment with one installed Pyalamode product. Start from the repository root and choose fresh outside paths:

```sh
pyalamode build --wheel --root examples/distribution/producer --output /tmp/pricing-wheel/checked_pricing-1.0.0-py3-none-any.whl --json
python -m pip install --no-deps --no-compile /tmp/pricing-wheel/checked_pricing-1.0.0-py3-none-any.whl
```

Copy `consumer/pyproject.toml` and `consumer/use_quote.py` into a separate project directory. Run its check and build from that directory with the installed environment:

```sh
pyalamode check --root . --json
pyalamode build --root . --output /tmp/pricing-consumer-build --json
cd /tmp/pricing-consumer-build
python -c 'from use_quote import total; assert total(40) == 1200; print(total(40))'
```

The consumer declaration selects the exact distribution name, version and package namespace. Its gate reanalyzes current installed original source and writers under its own current policy. Export schemas, callable/effect/failure/trust assumptions, module initialization and actual guard coverage remain separate. Producer permissions cannot approve an external operation for the consumer. A current checked core can have ordinary unchecked parent initialization; callers preserve that separately reported assumption.

The producer exports `Invoice`, `InvoiceStatus`, `quote`, `encode_invoice` and `decode_invoice`. Original calls use `checked_pricing.core`; selected generated data guards are normally imported from `checked_pricing._pyalamode_exports.core`. `Invoice` carries an exact canonical `Map[str,str]` and a closed status. The codecs preserve those schemas and values with the bounded stable format. They do not serialize arbitrary Python objects or execute restoration hooks.

`--no-compile` leaves caches absent, which is valid. Ordinary imports may create valid caches afterward. A present relevant cache must match the exact supported runtime/source/path/optimization compiler output; relocated stale caches can refuse and should be removed or regenerated from unchanged owned source. Wheel bytes are reproducible for identical source, policy, provenance and runtime/native environment across fresh output paths. Moving provenance roots or platforms requires independent consumer verification; byte equality across those changes is not promised.

This workflow has development controls; final source-frozen engineering observations belong to root verification. Human onboarding and integration usefulness remain UNMEASURED with zero participants and attempts.
