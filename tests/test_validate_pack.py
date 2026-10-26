"""Regression tests for pack validation and advisory spatial warnings."""
import json
import math
import os
import unittest

from validator.validate_pack import _spatial_warnings, validate

LEVELS = ("cozy", "spooky", "afterdark", "overdrive")
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def sample_pack():
    stops = []
    for i in range(6):
        stops.append({
            "id": i + 1,
            "name": f"Stop {i + 1}",
            "code": f"CODE-{i + 1}",
            "lat": 29.0 + i * 0.0001,
            "lng": -80.9,
            "story": {"cozy": "A story."},
            "puzzle": {"cozy": {"q": f"Question {i + 1}?", "a": f"answer-{i + 1}", "type": "text"}},
            "fallback": {"q": "Fallback?", "a": "fallback"},
            "hints": ["Hint one", "Hint two", "Hint three"],
        })
    return {"title": "Test pack", "stops": stops}


class ValidatePackTests(unittest.TestCase):
    def test_close_stops_are_warnings_not_validation_errors(self):
        pack = sample_pack()
        self.assertEqual(validate(pack), [])
        self.assertTrue(_spatial_warnings(pack["stops"]))

    def test_latitude_out_of_range_is_error(self):
        pack = sample_pack()
        pack["stops"][0]["lat"] = 91
        self.assertTrue(any("out of geographic bounds" in e for e in validate(pack)))

    def test_non_finite_coordinates_are_errors(self):
        pack = sample_pack()
        pack["stops"][0]["lng"] = math.nan
        self.assertTrue(any("must be finite" in e for e in validate(pack)))
        # Invalid coordinates must not crash advisory diagnostics.
        _spatial_warnings(pack["stops"])


class ParityTests(unittest.TestCase):
    """Pin the validator/player parity contract (SPEC.md): tiers are
    optional with a cozy fallback, but a tier that IS present must be
    well-formed. Mirrors quest-player's tests/pack-validator.test.cjs."""

    def test_flat_hints_accepted(self):
        pack = sample_pack()
        self.assertTrue(all(isinstance(s["hints"], list) for s in pack["stops"]))
        self.assertEqual(validate(pack), [])

    def test_per_level_hint_objects_accepted(self):
        pack = sample_pack()
        for s in pack["stops"]:
            s["hints"] = {level: [f"{level} hint {n}" for n in (1, 2, 3)] for level in LEVELS}
        self.assertEqual(validate(pack), [])

    def test_incomplete_per_level_hints_rejected(self):
        pack = sample_pack()
        hints = {level: ["a", "b", "c"] for level in LEVELS}
        del hints["overdrive"]
        pack["stops"][0]["hints"] = hints
        self.assertTrue(any("hints.overdrive" in e for e in validate(pack)))
        pack = sample_pack()
        hints = {level: ["a", "b", "c"] for level in LEVELS}
        hints["spooky"] = ["only", "two"]
        pack["stops"][0]["hints"] = hints
        self.assertTrue(any("hints.spooky" in e for e in validate(pack)))

    def test_whitespace_padded_answer_accepted(self):
        # The player normalizes both sides of an answer check, so padding
        # alone must not make a pack invalid.
        pack = sample_pack()
        pack["stops"][0]["puzzle"]["cozy"]["a"] = "  answer-1  "
        self.assertEqual(validate(pack), [])

    def test_answers_differing_only_by_padding_and_case_are_duplicates(self):
        pack = sample_pack()
        pack["stops"][1]["puzzle"]["cozy"]["a"] = " Answer-1 "
        self.assertTrue(any("must be unique" in e for e in validate(pack)))

    def test_malformed_present_story_tier_rejected(self):
        pack = sample_pack()
        pack["stops"][0]["story"]["spooky"] = ""
        self.assertTrue(any("story.spooky" in e for e in validate(pack)))
        pack = sample_pack()
        pack["stops"][1]["story"]["afterdark"] = {"text": "not a string"}
        self.assertTrue(any("story.afterdark" in e for e in validate(pack)))

    def test_malformed_present_puzzle_tier_rejected(self):
        pack = sample_pack()
        pack["stops"][0]["puzzle"]["spooky"] = {"q": "   ", "a": "ghost"}
        self.assertTrue(any("puzzle.spooky" in e for e in validate(pack)))
        pack = sample_pack()
        pack["stops"][1]["puzzle"]["afterdark"] = {"q": "A question?"}
        self.assertTrue(any("puzzle.afterdark" in e for e in validate(pack)))
        pack = sample_pack()
        pack["stops"][2]["puzzle"]["overdrive"] = "not a puzzle object"
        self.assertTrue(any("puzzle.overdrive" in e for e in validate(pack)))

    def test_wellformed_present_tiers_accepted(self):
        pack = sample_pack()
        for s in pack["stops"]:
            s["story"]["spooky"] = "A spookier telling."
            s["puzzle"]["spooky"] = {"q": "Spooky question?", "a": "boo", "type": "text"}
            s["puzzle"]["afterdark"] = {"q": "How many?", "a": 7, "type": "number"}
        self.assertEqual(validate(pack), [])

    def test_missing_non_cozy_tiers_accepted(self):
        pack = sample_pack()
        for s in pack["stops"]:
            self.assertEqual(set(s["story"]), {"cozy"})
            self.assertEqual(set(s["puzzle"]), {"cozy"})
        self.assertEqual(validate(pack), [])

    def test_exactly_six_stops_required(self):
        pack = sample_pack()
        pack["stops"] = pack["stops"][:5]
        self.assertTrue(any("exactly 6" in e for e in validate(pack)))
        pack = sample_pack()
        extra = dict(pack["stops"][0])
        extra["id"] = 7
        pack["stops"].append(extra)
        self.assertTrue(any("exactly 6" in e for e in validate(pack)))

    def test_duplicate_cozy_answers_rejected(self):
        pack = sample_pack()
        pack["stops"][1]["puzzle"]["cozy"]["a"] = pack["stops"][0]["puzzle"]["cozy"]["a"]
        self.assertTrue(any("must be unique" in e for e in validate(pack)))

    def test_answers_equivalent_after_player_normalization_are_duplicates(self):
        cases = [
            ("Old oak", "the old oak"),
            ("lanterns", "lantern"),
            ("red-blue", "red blue"),
            ("4,015", "4015"),
        ]
        for first, second in cases:
            with self.subTest(first=first, second=second):
                pack = sample_pack()
                pack["stops"][0]["puzzle"]["cozy"]["a"] = first
                pack["stops"][1]["puzzle"]["cozy"]["a"] = second
                self.assertTrue(
                    any("must be unique" in e for e in validate(pack)),
                    f"{first!r} and {second!r} should collide under player normalization",
                )

    def test_answers_not_equivalent_after_player_normalization_remain_valid(self):
        pack = sample_pack()
        pack["stops"][0]["puzzle"]["cozy"]["a"] = "old oak"
        pack["stops"][1]["puzzle"]["cozy"]["a"] = "old elm"
        self.assertFalse(any("must be unique" in e for e in validate(pack)))

    def test_real_sample_pack_fixture_validates(self):
        # Vendored verbatim from ZQM-Labs/quest-packs
        # sample-quest/wisp-sample.json (the official free sample: story
        # cozy+spooky, puzzle cozy only, flat hints) — the same fixture
        # quest-player's regression tests use.
        with open(os.path.join(FIXTURES, "wisp-sample.json"), encoding="utf-8") as f:
            pack = json.load(f)
        self.assertEqual(validate(pack), [])


if __name__ == "__main__":
    unittest.main()
