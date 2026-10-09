"""Narrow ordinary adapters with separately approved external assumptions.

Importing this module performs ordinary native backend setup. These functions do
not consult project approval or provide runtime purity/dependency certification.
"""

import binascii as _binascii
import _sha2 as _sha2

__all__ = ("base64_encode", "base64_decode", "sha256_digest")

_MAX_BYTES = 1_048_576
_MAX_BASE64_BYTES = 1_398_104


def _exact_bytes(data, limit, /):
    if type(data) is not bytes:
        raise TypeError("integration input requires exact bytes")
    if len(data) > limit:
        raise ValueError("integration input exceeds the published byte limit")


def base64_encode(data: bytes, /) -> bytes:
    """Encode at most one MiB as canonical padded Base64 without newlines."""
    _exact_bytes(data, _MAX_BYTES)
    return _binascii.b2a_base64(data, newline=False)


def base64_decode(data: bytes, /) -> bytes:
    """Decode only canonical padded Base64 yielding at most one MiB."""
    _exact_bytes(data, _MAX_BASE64_BYTES)
    try:
        decoded = _binascii.a2b_base64(data, strict_mode=True)
    except _binascii.Error:
        decoded = None
    # Raising after the native handler ends avoids retaining native Error state
    # in the replacement ValueError's context; no native error fields are read.
    if decoded is None:
        raise ValueError("invalid canonical base64")
    if len(decoded) > _MAX_BYTES:
        raise ValueError("decoded data exceeds the published byte limit")
    if _binascii.b2a_base64(decoded, newline=False) != data:
        raise ValueError("invalid canonical base64")
    return decoded


def sha256_digest(data: bytes, /) -> bytes:
    """Return the fixed 32-byte SHA-256 digest of at most one MiB."""
    _exact_bytes(data, _MAX_BYTES)
    return _sha2.sha256(data, usedforsecurity=False).digest()
