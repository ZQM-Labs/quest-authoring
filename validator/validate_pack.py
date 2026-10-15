#!/usr/bin/env python3
"""Validate a ZQM Labs quest pack against SPEC.md.

Mirrors the player's validatePack() (ZQM-Computing/zqm-labs, lantern-player/app.js):
a pack that fails here will be rejected wholesale by the player, which falls
back to its built-in demo.

Deliberate strictness beyond the player: puzzle `type` is checked against
number/text (the player ignores `type` entirely). Everything else matches
the player's rules exactly.

Usage: python3 validate_pack.py <pack.json>
Exit 0 = valid, exit 1 = invalid (errors printed).
"""
import json
import sys

SCARE_LEVELS = ("cozy", "spooky", "afterdark", "overdrive")


def err(errors, msg):
    errors.append(msg)


def _blank(v):
    """Player-falsy: None, missing, empty, or whitespace-only."""
    return v is None or str(v).strip() == ""


def _haversine_m(lat1, lng1, lat2, lng2):
    """Great-circle distance in meters."""
    import math
    R = 6371000
    t = math.radians
    h = math.sin(t(lat2 - lat1) / 2) ** 2 + math.cos(t(lat1)) * math.cos(t(lat2)) * math.sin(t(lng2 - lng1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _spatial_warnings(stops):
    """Advisory geospatial checks: stop spacing and route length.

    These are warnings, not errors — a tight indoor venue or a long trail
    may be intentional. But GPS can't reliably distinguish stops <20m
    apart, and >1km between stops is a long walk for families.
    """
    warnings = []
    coords = []
    for s in stops:
        lat, lng = s.get("lat"), s.get("lng")
        if isinstance(lat, (int, float)) and isinstance(lng, (int, float)) \
                and not isinstance(lat, bool) and not isinstance(lng, bool):
            coords.append((s.get("id", "?"), float(lat), float(lng)))
    if len(coords) < 2:
        return warnings
    # Too close: check ALL pairs (GPS can't distinguish any two stops <20m apart)
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            idi, lati, lngi = coords[i]
            idj, latj, lngj = coords[j]
            d = _haversine_m(lati, lngi, latj, lngj)
            if d < 20:
                warnings.append(
                    f"spatial: stops {idi} and {idj} are only {d:.0f}m apart — "
                    f"GPS (±10-15m) may not distinguish them; use distinct sign codes")
    # Too far: check CONSECUTIVE stops only (the walking route)
    for i in range(len(coords) - 1):
        idi, lati, lngi = coords[i]
        idj, latj, lngj = coords[i + 1]
        d = _haversine_m(lati, lngi, latj, lngj)
        if d > 1000:
            warnings.append(
                f"spatial: stops {idi} → {idj} are {d/1000:.1f}km apart — "
                f"long walk, consider transport or a tighter cluster")
    # Total route length (in stop order)
    total = sum(_haversine_m(coords[i][1], coords[i][2], coords[i+1][1], coords[i+1][2])
                for i in range(len(coords) - 1))
    if total > 3000:
        warnings.append(
            f"spatial: total route is {total/1000:.1f}km — verify it's walkable for your audience")
    return warnings


def validate(pack):
    errors = []
    if not isinstance(pack, dict):
        return ["pack must be a JSON object"]
    stops = pack.get("stops")
    if not isinstance(stops, list) or len(stops) != 6:
        got = len(stops) if isinstance(stops, list) else type(stops).__name__
        err(errors, f"top-level: 'stops' must be an array of exactly 6 (got {got})")
        stops = stops if isinstance(stops, list) else []

    answers = []
    ids = []
    for s in stops:
        tag = f"stop {s.get('id', '?')}" if isinstance(s, dict) else "stop ?"
        if not isinstance(s, dict):
            err(errors, f"{tag}: stop must be an object")
            continue
        sid = s.get("id")
        if not isinstance(sid, int) or isinstance(sid, bool):
            err(errors, f"{tag}: 'id' must be an integer")
        else:
            ids.append(sid)
        for f in ("name", "code"):
            if _blank(s.get(f)):
                err(errors, f"{tag}: '{f}' must be a non-empty string")
        for f in ("lat", "lng"):
            v = s.get(f)
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                err(errors, f"{tag}: '{f}' must be numeric")
        story = s.get("story")
        if not isinstance(story, dict) or "cozy" not in story:
            err(errors, f"{tag}: 'story.cozy' is required")
        puzzle = s.get("puzzle")
        cozy = puzzle.get("cozy") if isinstance(puzzle, dict) else None
        if not isinstance(cozy, dict) or _blank(cozy.get("q")) or _blank(cozy.get("a")):
            err(errors, f"{tag}: 'puzzle.cozy.q' and 'puzzle.cozy.a' are required")
        else:
            a = cozy["a"]
            if str(a) != str(a).strip():
                err(errors, f"{tag}: 'puzzle.cozy.a' has leading/trailing whitespace "
                            f"(the player's answer check would never match it)")
            answers.append(str(a).strip().lower())
            if cozy.get("type") not in (None, "number", "text"):
                err(errors, f"{tag}: puzzle type must be 'number' or 'text'")
        for level in SCARE_LEVELS:
            for section in ("story", "puzzle"):
                variant = (s.get(section) or {}).get(level)
                if variant is not None and not isinstance(variant, (str, dict)):
                    err(errors, f"{tag}: {section}.{level} has wrong type")
        fb = s.get("fallback")
        if not isinstance(fb, dict) or _blank(fb.get("q")) or _blank(fb.get("a")):
            err(errors, f"{tag}: 'fallback.q' and 'fallback.a' are required")
        hints = s.get("hints")
        if not isinstance(hints, list) or len(hints) != 3:
            err(errors, f"{tag}: 'hints' must be an array of exactly 3 strings")

    if len(set(answers)) != len(answers):
        err(errors, f"cross-stop: puzzle.cozy.a answers must be unique (got {answers})")
    if len(set(ids)) != len(ids):
        err(errors, f"cross-stop: stop ids must be unique (got {ids})")
    for w in _spatial_warnings(stops):
        errors.append("WARNING: " + w)
    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: python3 validate_pack.py <pack.json>", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            pack = json.load(f)
    except FileNotFoundError:
        print(f"file not found: {sys.argv[1]}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"invalid JSON in {sys.argv[1]}: {e}", file=sys.stderr)
        return 2
    errors = validate(pack)
    if errors:
        print(f"INVALID: {len(errors)} error(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("VALID: pack passes all checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
