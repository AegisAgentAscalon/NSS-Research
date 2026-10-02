"""Strict JSON and a deliberately small validator for the shipped JSON Schemas."""
import json
import re
from pathlib import Path

from .runtime import fail

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            fail("VALIDATION_FAILED", f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def decode(text):
    try:
        return json.loads(text, object_pairs_hook=_pairs,
                          parse_constant=lambda _: fail("VALIDATION_FAILED", "Non-finite JSON number"))
    except (ValueError, TypeError) as e:
        fail("VALIDATION_FAILED", f"Invalid JSON: {e}")


def read_json(path):
    try:
        return decode(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as e:
        fail("VALIDATION_FAILED", f"Unreadable JSON: {e}")


def validate(value, name):
    """Supports only the keywords used by our local schemas; no remote references."""
    _validate(value, read_json(SCHEMAS / name), "$")
    return value


def _validate(value, schema, path):
    if "$ref" in schema:
        ref = schema["$ref"]
        if Path(ref).name != ref:
            fail("VALIDATION_FAILED", "Only sibling schema references supported")
        return _validate(value, read_json(SCHEMAS / ref), path)
    kinds = {"object": dict, "array": list, "string": str, "integer": int,
             "boolean": bool, "null": type(None)}
    types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
    if not any(type(value) is kinds[t] for t in types):
        fail("VALIDATION_FAILED", f"{path}: wrong type")
    if "enum" in schema and value not in schema["enum"]:
        fail("VALIDATION_FAILED", f"{path}: invalid enum")
    if isinstance(value, dict):
        props = schema["properties"]
        if set(schema.get("required", [])) - value.keys() or set(value) - props.keys():
            fail("VALIDATION_FAILED", f"{path}: missing or unknown fields")
        for key, item in value.items():
            _validate(item, props[key], path + "." + key)
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", len(value)):
            fail("VALIDATION_FAILED", f"{path}: array size out of bounds")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            fail("VALIDATION_FAILED", f"{path}: duplicate items")
        for i, item in enumerate(value):
            _validate(item, schema["items"], f"{path}[{i}]")
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", len(value)) or ("pattern" in schema and not re.fullmatch(schema["pattern"], value)):
            fail("VALIDATION_FAILED", f"{path}: invalid string")
    elif type(value) is int:
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            fail("VALIDATION_FAILED", f"{path}: out of bounds")
