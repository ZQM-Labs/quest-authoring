<!-- markdownlint-disable MD033 MD012 -->

# Quest Authoring — ZQM Labs

<!-- ZQM-START -->
<p align="center">
  <strong>ZQM Labs — Z's Quests & Mischief</strong><br>
  <a href="https://zqmlabs.com">zqmlabs.com</a> •
  <a href="https://github.com/ZQM-Labs">GitHub</a>
</p>
<!-- ZQM-END -->



The quest-pack format: spec, validator, and authoring guide for building new
**ZQM Labs — Z's Quests & Mischief** location-game editions.

## Contents

| Path | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The quest-pack JSON format, field by field, including every validation rule the player enforces. |
| [`guide/authoring-guide.md`](guide/authoring-guide.md) | How to write good stops: puzzles, hint ladders, and all four Dial levels. |
| [`validator/validate_pack.py`](validator/validate_pack.py) | The validator. Run it on your pack before you ship it — the player rejects invalid packs wholesale. |

## Compatibility and release contract

The specification, Python validator, and player parser are separate enforcement points. A pack is not release-ready just because one of them accepts it.

For each release candidate:

1. Run the validator against the exact JSON artifact that will ship.
2. Load that same artifact in the target player version; record both commit/version identifiers.
3. Include negative fixtures for malformed JSON, missing required fields, invalid field types, unsupported values, and unexpected structures.
4. Confirm that validation failures are actionable and do not crash the player.
5. Playtest the pack on the intended route, including QR/manual entry, GPS failure, hint progression, offline resume, and observation-answer fallback.
6. Record any intentional differences between authoring validation and runtime validation as explicit compatibility notes.

The player currently enforces its own `validatePack` rules. Keep the [player repository](https://github.com/ZQM-Labs/lantern-player) and [playtest protocol](https://github.com/ZQM-Labs/playtests) in the release review; this repository's validator is not a substitute for runtime testing.

## Workflow

1. Draft your 6 stops (see the authoring guide).
2. Write the pack JSON (see the spec).
3. `python3 validator/validate_pack.py my-pack.json` — fix everything it
   flags.
4. Playtest it on foot (see
   [ZQM-Labs/playtests](https://github.com/ZQM-Labs/playtests)).
5. Publish via
   [ZQM-Labs/quest-packs](https://github.com/ZQM-Labs/quest-packs).

## More from ZQM Labs

- [quest-packs][qp] — edition catalog + free sample quest
- [organizer-toolkit][otk] — setup checklists, print specs, FAQ
- [playtests][pt] — playtest protocol and results
- [zqmlabs-site][site] — the public website

[qp]: https://github.com/ZQM-Labs/quest-packs
[otk]: https://github.com/ZQM-Labs/organizer-toolkit
[pt]: https://github.com/ZQM-Labs/playtests
[site]: https://github.com/ZQM-Labs/zqmlabs-site

Finished packs for the catalog:
<zqmcomputing@gmail.com> · <https://zqmlabs.com>

*Play more. Plan less.*


<!-- ZQM-FOOTER-START -->
---

<p align="center">
  <em>Play more. Plan less.</em><br>
  <a href="https://zqmlabs.com">zqmlabs.com</a> •
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a> •
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- ZQM-FOOTER-END -->


## Release-status boundary

Validation proves only the rules exercised by the validator and player version tested. It does not prove that an edition is publicly available, checkout works, a venue is approved, or an event is safe and accessible. For Wisp's Lost Lanterns or any future edition, attach the exact pack/version and validator output to a dated release record, then link the matching player test and field-playtest evidence. Checkout/payment/fulfillment must be verified separately. If those records are absent, document the release or field status as **unknown** rather than deriving it from a passing validator.
