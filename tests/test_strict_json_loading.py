"""Strict input preflight regression tests for the public quest-pack CLI."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validator.validate_pack import MAX_PACK_BYTES, load_pack, validate

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "tests" / "fixtures" / "wisp-sample.json"
CLI = ROOT / "validator" / "validate_pack.py"


class StrictInputTests(unittest.TestCase):
    def write(self, root: Path, data: bytes) -> Path:
        path = root / "pack.json"
        path.write_bytes(data)
        return path

    def test_existing_valid_sample_preserved(self):
        loaded = load_pack(VALID)
        self.assertEqual(loaded, json.loads(VALID.read_text(encoding="utf-8")))
        self.assertEqual(validate(loaded), [])

    def test_reject_duplicate_keys_at_any_depth(self):
        inputs = (
            b'{"title":"one","title":"two","stops":[]}',
            b'{"nested":{"code":"one","code":"two"}}',
            b'{"nested":{"code":"one","\\u0063ode":"two"}}',
        )
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            for data in inputs:
                with self.subTest(data=data), self.assertRaisesRegex(ValueError, "duplicate JSON object key"):
                    load_pack(self.write(root, data))

    def test_reject_js_incompatible_nonfinite_tokens_anywhere(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            for token in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(token=token), self.assertRaisesRegex(ValueError, "non-finite JSON"):
                    load_pack(self.write(root, ('{"unused":' + token + '}').encode()))

    def test_reject_oversized_and_malformed_utf8(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            with self.assertRaisesRegex(ValueError, "4 MiB"):
                load_pack(self.write(root, b" " * (MAX_PACK_BYTES + 1)))
            with self.assertRaises(UnicodeDecodeError):
                load_pack(self.write(root, b"\xff"))

    def test_cli_returns_usage_error_for_ambiguous_source(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            src = self.write(root, b'{"kit":"SECRET-ONE","kit":"SECRET-TWO","stops":[]}')
            proc = subprocess.run(
                [sys.executable, str(CLI), str(src)],
                cwd=ROOT, capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("duplicate JSON object key", proc.stderr)
            self.assertNotIn("SECRET-ONE", proc.stderr)
            self.assertNotIn("SECRET-TWO", proc.stderr)
            self.assertNotIn("VALID: ", proc.stdout)

    def test_duplicate_answers_do_not_leak_solution_text(self):
        data = load_pack(VALID)
        data["stops"][0]["puzzle"]["cozy"]["a"] = "PRIVATE-PUZZLE-ANSWER"
        data["stops"][1]["puzzle"]["cozy"]["a"] = "private puzzle answer"
        errors = validate(data)
        self.assertTrue(any("must be unique" in error for error in errors))
        self.assertNotIn("PRIVATE-PUZZLE-ANSWER", "\n".join(errors))
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            src = self.write(root, json.dumps(data).encode("utf-8"))
            proc = subprocess.run(
                [sys.executable, str(CLI), str(src)],
                cwd=ROOT, capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertIn("INVALID", proc.stdout)
            self.assertNotIn("PRIVATE-PUZZLE-ANSWER", proc.stdout)


if __name__ == "__main__":
    unittest.main()
