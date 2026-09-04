from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
from typing import Any

FINGERPRINT_FIELD = "result_fingerprint_sha256"


def canonical_payload_bytes(payload: dict[str, Any]) -> bytes:
    """Return deterministic JSON bytes excluding the fingerprint itself."""
    obj = copy.deepcopy(payload)
    obj.pop(FINGERPRINT_FIELD, None)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def fingerprint_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload_bytes(payload)).hexdigest()


def attach_fingerprint(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out[FINGERPRINT_FIELD] = fingerprint_payload(out)
    return out


def verify_payload(payload: dict[str, Any]) -> dict[str, Any]:
    expected = payload.get(FINGERPRINT_FIELD)
    actual = fingerprint_payload(payload)
    return {
        "valid": bool(expected) and expected == actual,
        "expected": expected,
        "actual": actual,
        "algorithm": "sha256",
    }


def verify_result_file(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    result = verify_payload(payload)
    result["path"] = str(path)
    return result
