"""Individually checked payload functions; external import setup is ordinary."""
from typing import Callable
from pyalamode import fun, Vector, compose, Result, Ok, Err, Failure, failure_value
from pyalamode.integrations import base64_encode, base64_decode, sha256_digest


@fun
def encode(payload: bytes) -> bytes:
    return base64_encode(payload)


@fun
def decode(transport: bytes) -> bytes:
    return base64_decode(transport)


@fun
def content_key(payload: bytes) -> bytes:
    return sha256_digest(payload)


@fun
def prepare(payload: bytes) -> tuple[bytes, bytes]:
    return encode(payload), content_key(payload)


@fun
def recover(transport: bytes) -> Result[bytes, Failure]:
    try:
        return Ok(decode(transport))
    except ValueError as caught:
        return Err(failure_value(caught))


@fun
def digest_factory() -> Callable[[bytes], bytes]:
    return compose(content_key, decode)


@fun
def attachment_keys(transports: Vector[bytes]) -> Vector[bytes]:
    return transports.map(digest_factory())
