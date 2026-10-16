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
| [`guide/authoring-guide.md`](guide/authoring-guide.md) | How to write good stops: puzzles, hint ladders, and the three Dial levels. |
| [`validator/validate_pack.py`](validator/validate_pack.py) | The validator. Run it on your pack before you ship it — the player rejects invalid packs wholesale. |

## Workflow

1. Draft your 6 stops (see the authoring guide).
2. Write the pack JSON (see the spec).
3. `python3 validator/validate_pack.py my-pack.json` — fix everything it flags.
4. Playtest it on foot (see [ZQM-Labs/playtests](https://github.com/ZQM-Labs/playtests)).
5. Publish via [ZQM-Labs/quest-packs](https://github.com/ZQM-Labs/quest-packs).

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
