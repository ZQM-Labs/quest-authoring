# Quest Authoring — ZQM Labs

The quest-pack format: spec, validator, and authoring guide for building new
**ZQM Labs — Z's Quests & Mischief** location-game editions.

## Contents

| Path | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The quest-pack JSON format, field by field, including every validation rule the player enforces. |
| [`guide/authoring-guide.md`](guide/authoring-guide.md) | How to write good stops: puzzles, hint ladders, and the three Dial levels. |
| [`validator/validate_pack.py`](validator/validate_pack.py) | The validator. Run it on your pack before you ship it — the player rejects invalid packs wholesale. |

## Workflow

1. Draft your 6 stops (see the authoring guide).
2. Write the pack JSON (see the spec).
3. `python3 validator/validate_pack.py my-pack.json` — fix everything it flags.
4. Playtest it on foot (see [ZQM-Labs/playtests](https://github.com/ZQM-Labs/playtests)).
5. Publish via [ZQM-Labs/quest-packs](https://github.com/ZQM-Labs/quest-packs).

Finished packs for the catalog: zqmcomputing@gmail.com · https://zqmlabs.com

*Play more. Plan less.*
