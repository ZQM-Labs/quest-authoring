<!-- markdownlint-disable MD033 MD012 -->

# Quest Authoring — ZQM Labs

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Labs — Z's Quests & Mischief</strong><br>
  <a href="https://zqmlabs.com">zqmlabs.com</a> •
  <a href="https://github.com/ZQM-Labs">GitHub</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

The quest-pack format: spec, validator, generator, and authoring guide for building new
**ZQM Labs — Z's Quests & Mischief** location-game editions.

## Repository role and status

**Status:** Active, public. Format authority for ZQM Labs quest packs.

**What this repository is:** The quest-pack JSON specification (`SPEC.md`), the authoring guide, and the Python tooling — `validator/validate_pack.py` and `validator/gen_quest_pack.py` — for building new location-game editions.

**What it contributes:** Every pack in quest-packs, and every community-submitted pack, is written against this spec and checked with this validator; quest-packs' own documentation points authors here for the generator. The player's runtime `validatePack` rules are a separate enforcement point (see the compatibility contract below), so this repo defines the format but does not by itself prove a pack will run.

## Contents

| Path | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The quest-pack JSON format, field by field, including every validation rule the player enforces. |
| [`guide/authoring-guide.md`](guide/authoring-guide.md) | How to write good stops: puzzles, hint ladders, and all four Dial levels. |
| [`validator/validate_pack.py`](validator/validate_pack.py) | The validator. Run it on your pack before you ship it — the player rejects invalid packs wholesale. |
| [`validator/gen_quest_pack.py`](validator/gen_quest_pack.py) | The generator. Feed it a YAML config, get a playable quest pack HTML + manifest. |

## Installation

```bash
pip install -e .
```

Requires Python 3.11+.

## Quick Start

```bash
# Generate a quest pack from YAML
python validator/gen_quest_pack.py my-quest.yaml

# Validate the output
python validator/validate_pack.py dist/my-quest-slug/manifest.json
```

## Usage

Write your quest pack as JSON following the spec in this repo, then run
it through the validator before publishing — a pack that validates will
load in the player. The [Quick Start](#quick-start) walks through a
minimal pack end to end.

## Compatibility and release contract

The specification, Python validator, and player parser are separate enforcement points. A pack is not release-ready just because one of them accepts it.

For each release candidate:

1. Run the validator against the exact JSON artifact that will ship.
2. Load that same artifact in the target player version; record both commit/version identifiers.
3. Include negative fixtures for malformed JSON, missing required fields, invalid field types, unsupported values, and unexpected structures.
4. Confirm that validation failures are actionable and do not crash the player.
5. Playtest the pack on the intended route, including QR/manual entry, GPS failure, hint progression, offline resume, and observation-answer fallback.
6. Record any intentional differences between authoring validation and runtime validation as explicit compatibility notes.

The player currently enforces its own `validatePack` rules. Keep the [player repository](https://github.com/ZQM-Labs/quest-player) and [playtest protocol](https://github.com/ZQM-Labs/playtests) in the release review; this repository's validator is not a substitute for runtime testing.

## License

MIT — see [LICENSE](LICENSE).

## Validation

This repository uses GitHub Actions for continuous integration. See [CI workflow](.github/workflows/ci.yml) for details.

To validate locally:

```bash
# Run documentation checks
python scripts/check_docs.py
```
