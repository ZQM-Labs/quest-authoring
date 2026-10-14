#!/usr/bin/env python3
"""Validate a ZQM Labs quest pack against SPEC.md.

Mirrors the player's validatePack(): a pack that fails here will be rejected
wholesale by the player, which falls back to its built-in demo.

Usage: python3 validate_pack.py <pack.json>
Exit 0 = valid, exit 1 = invalid (errors printed).
"""
import json
import sys

SCARE_LEVELS = ("cozy", "spooky", "afterdark", "overdrive")


def err(errors, msg):
    errors.append(msg)


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
    for s in stops:
        tag = f"stop {s.get('id', '?')}" if isinstance(s, dict) else "stop ?"
        if not isinstance(s, dict):
            err(errors, f"{tag}: stop must be an object")
            continue
        for f in ("id", "name", "code"):
            if f not in s:
                err(errors, f"{tag}: missing required field '{f}'")
        for f in ("lat", "lng"):
            if not isinstance(s.get(f), (int, float)):
                err(errors, f"{tag}: '{f}' must be numeric")
        story = s.get("story")
        if not isinstance(story, dict) or "cozy" not in story:
            err(errors, f"{tag}: 'story.cozy' is required")
        puzzle = s.get("puzzle")
        cozy = puzzle.get("cozy") if isinstance(puzzle, dict) else None
        if not isinstance(cozy, dict) or "q" not in cozy or "a" not in cozy:
            err(errors, f"{tag}: 'puzzle.cozy.q' and 'puzzle.cozy.a' are required")
        else:
            answers.append(str(cozy["a"]).strip().lower())
            if cozy.get("type") not in (None, "number", "text"):
                err(errors, f"{tag}: puzzle type must be 'number' or 'text'")
        for level in SCARE_LEVELS:
            for section in ("story", "puzzle"):
                variant = (s.get(section) or {}).get(level)
                if variant is not None and not isinstance(variant, (str, dict)):
                    err(errors, f"{tag}: {section}.{level} has wrong type")
        fb = s.get("fallback")
        if not isinstance(fb, dict) or "q" not in fb or "a" not in fb:
            err(errors, f"{tag}: 'fallback.q' and 'fallback.a' are required")
        hints = s.get("hints")
        if not isinstance(hints, list) or len(hints) != 3:
            err(errors, f"{tag}: 'hints' must be an array of exactly 3 strings")

    if len(set(answers)) != len(answers):
        err(errors, f"cross-stop: puzzle.cozy.a answers must be unique (got {answers})")
    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: python3 validate_pack.py <pack.json>", file=sys.stderr)
        return 2
    with open(sys.argv[1]) as f:
        pack = json.load(f)
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
