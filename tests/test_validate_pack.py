"""Regression tests for pack validation and advisory spatial warnings."""
import math
import unittest

from validator.validate_pack import _spatial_warnings, validate


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


if __name__ == "__main__":
    unittest.main()
