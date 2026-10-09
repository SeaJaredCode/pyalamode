"""Finite exact standard operations and eager immutable functional helpers.

Callbacks are ordinary exact Python functions. Their signature, effects,
captures and dependency contracts require static evidence or caller obligations;
the runtime does not register or certify callable behavior.
"""

from . import collections as _collections
from . import sums as _sums

__all__ = ["text_split", "text_join", "text_replace", "text_startswith", "text_slice",
           "integer_clamp", "integer_parse_decimal", "integer_format_decimal",
           "utf8_encode", "utf8_decode", "hex_encode", "hex_decode",
           "vector_scan", "vector_group_by", "compose", "partial_first", "result_traverse"]

_DIGITS = "0123456789"
_HEX_DIGITS = "0123456789abcdefABCDEF"
_DECIMAL_DIGITS = 4096
_DECIMAL_LIMIT = 10 ** _DECIMAL_DIGITS


def _exact(value, kind, path):
    if type(value) is not kind:
        _collections._invalid(path, "unsupported exact input type")


def _vector(values, path="values"):
    _exact(values, _collections.Vector, path)
    _collections._validate(values, path)
    return _collections._storage(values, "_items", path)


def text_split(text, separator, /):
    _exact(text, str, "text")
    _exact(separator, str, "separator")
    pieces = str.split(text, separator)
    return _collections._new(_collections.Vector, "_items", tuple(pieces))


def text_join(parts, separator, /):
    items = _vector(parts, "parts")
    _exact(separator, str, "separator")
    for part in items:
        _exact(part, str, "parts.item")
    return str.join(separator, items)


def text_replace(text, old, new, /):
    _exact(text, str, "text")
    _exact(old, str, "old")
    _exact(new, str, "new")
    return str.replace(text, old, new)


def text_startswith(text, prefix, /):
    _exact(text, str, "text")
    _exact(prefix, str, "prefix")
    return str.startswith(text, prefix)


def text_slice(text, start, stop, /):
    _exact(text, str, "text")
    _exact(start, int, "start")
    _exact(stop, int, "stop")
    return text[start:stop]


def integer_clamp(value, lower, upper, /):
    _exact(value, int, "value")
    _exact(lower, int, "lower")
    _exact(upper, int, "upper")
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    return lower if value < lower else upper if value > upper else value


def integer_parse_decimal(text, /):
    _exact(text, str, "text")
    negative = len(text) > 0 and text[0] == "-"
    digits = text[1:] if text and (text[0] == "+" or text[0] == "-") else text
    if not digits or len(digits) > _DECIMAL_DIGITS:
        raise ValueError("decimal requires one to 4096 ASCII digits")
    value = 0
    for character in digits:
        digit = ord(character) - 48
        if digit < 0 or digit > 9:
            raise ValueError("decimal requires ASCII digits without whitespace")
        value = value * 10 + digit
    return -value if negative else value


def integer_format_decimal(value, /):
    _exact(value, int, "value")
    negative = value < 0
    magnitude = -value if negative else value
    if magnitude >= _DECIMAL_LIMIT:
        raise ValueError("decimal magnitude exceeds 4096 digits")
    if magnitude == 0:
        return "0"
    digits = []
    while magnitude:
        digits.append(_DIGITS[magnitude % 10])
        magnitude //= 10
    digits.reverse()
    return ("-" if negative else "") + str.join("", digits)


def utf8_encode(text, /):
    _exact(text, str, "text")
    output = []
    for index, character in enumerate(text):
        point = ord(character)
        if point < 0x80:
            output.append(point)
        elif point < 0x800:
            output.append(0xC0 | (point >> 6))
            output.append(0x80 | (point & 0x3F))
        elif 0xD800 <= point <= 0xDFFF:
            end = index + 1
            while end < len(text) and 0xD800 <= ord(text[end]) <= 0xDFFF:
                end += 1
            raise UnicodeEncodeError("utf-8", text, index, end, "surrogates not allowed")
        elif point < 0x10000:
            output.append(0xE0 | (point >> 12))
            output.append(0x80 | ((point >> 6) & 0x3F))
            output.append(0x80 | (point & 0x3F))
        else:
            output.append(0xF0 | (point >> 18))
            output.append(0x80 | ((point >> 12) & 0x3F))
            output.append(0x80 | ((point >> 6) & 0x3F))
            output.append(0x80 | (point & 0x3F))
    return bytes(output)


def utf8_decode(data, /):
    _exact(data, bytes, "data")
    output = []
    index = 0
    size = len(data)
    while index < size:
        lead = data[index]
        if lead < 0x80:
            output.append(chr(lead))
            index += 1
            continue
        if 0xC2 <= lead <= 0xDF:
            width, point, second_low, second_high = 2, lead & 0x1F, 0x80, 0xBF
        elif 0xE0 <= lead <= 0xEF:
            width, point = 3, lead & 0x0F
            second_low = 0xA0 if lead == 0xE0 else 0x80
            second_high = 0x9F if lead == 0xED else 0xBF
        elif 0xF0 <= lead <= 0xF4:
            width, point = 4, lead & 0x07
            second_low = 0x90 if lead == 0xF0 else 0x80
            second_high = 0x8F if lead == 0xF4 else 0xBF
        else:
            raise UnicodeDecodeError("utf-8", data, index, index + 1, "invalid start byte")
        for offset in range(1, width):
            position = index + offset
            if position >= size:
                raise UnicodeDecodeError("utf-8", data, index, size, "unexpected end of data")
            value = data[position]
            lower = second_low if offset == 1 else 0x80
            upper = second_high if offset == 1 else 0xBF
            if value < lower or value > upper:
                raise UnicodeDecodeError("utf-8", data, index, position, "invalid continuation byte")
            point = (point << 6) | (value & 0x3F)
        output.append(chr(point))
        index += width
    return str.join("", output)


def hex_encode(data, /):
    _exact(data, bytes, "data")
    return bytes.hex(data)


def hex_decode(text, /):
    _exact(text, str, "text")
    if len(text) % 2:
        raise ValueError("hexadecimal requires even ASCII hex pairs without whitespace")
    for character in text:
        if character not in _HEX_DIGITS:
            raise ValueError("hexadecimal requires even ASCII hex pairs without whitespace")
    return bytes.fromhex(text)


def vector_scan(values, callback, initial, /):
    items = _vector(values)
    _collections._function(callback)
    _collections._validate(initial, "initial")
    output = [initial]
    accumulator = initial
    for value in items:
        accumulator = callback(accumulator, value)
        _collections._validate(accumulator, "scan.accumulator")
        output.append(accumulator)
    return _collections._new(_collections.Vector, "_items", tuple(output))


def vector_group_by(values, callback, /):
    items = _vector(values)
    _collections._function(callback)
    groups = []
    domain = None
    for value in items:
        key = callback(value)
        _collections._validate_key(key, "group.key")
        if domain is None:
            domain = type(key)
        elif type(key) is not domain:
            _collections._invalid("group.key", "group keys require one exact scalar domain")
        for previous, group in groups:
            if key == previous:
                group.append(value)
                break
        else:
            groups.append((key, [value]))
    entries = tuple((key, _collections._new(_collections.Vector, "_items", tuple(group))) for key, group in groups)
    return _collections._new(_collections.OrderedMap, "_entries", entries)


def compose(outer, inner, /):
    _collections._function(outer, "outer")
    _collections._function(inner, "inner")

    def applied(value, /):
        intermediate = inner(value)
        _collections._validate(intermediate, "compose.intermediate")
        result = outer(intermediate)
        _collections._validate(result, "compose.result")
        return result

    return applied


def partial_first(callback, bound, /):
    _collections._function(callback)
    _collections._validate(bound, "bound")

    def applied(value, /):
        result = callback(bound, value)
        _collections._validate(result, "partial.result")
        return result

    return applied


def result_traverse(values, callback, /):
    items = _vector(values)
    _collections._function(callback)
    output = []
    for value in items:
        result = callback(value)
        _collections._validate(result, "traverse.result")
        if type(result) is _sums.Err:
            return result
        if type(result) is not _sums.Ok:
            _collections._invalid("traverse.result", "expected exact Ok or Err")
        output.append(object.__getattribute__(result, "value"))
    return _sums.Ok(_collections._new(_collections.Vector, "_items", tuple(output)))
