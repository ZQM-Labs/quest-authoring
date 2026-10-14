# Quest-Pack Spec (v1)

The player loads a quest pack as JSON and runs it through `validatePack()`.
**A pack that fails validation is rejected wholesale** — the player falls back
to its built-in demo. Validate before you ship.

## Top level

| Field | Type | Required | Meaning |
|---|---|---|---|
| `title` | string | no | Edition display title, e.g. `"Wisp's Lost Lanterns"` |
| `kit` | string | no | Kit ID binding the pack to a kit, e.g. `"DEMO"` |
| `stops` | array of stop objects | **yes — exactly 6** | `stops.length !== 6` → rejected |

## Per stop

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | number | yes | 1-based stop number; also the QR `?stop=N` deep-link target. Must match the stop's `order` in the kit config. |
| `name` | string | yes | Displayed as "Stop N: {name}" |
| `lat`, `lng` | number | yes | Map marker + GPS "you're here" check (haversine, 30 m radius) |
| `code` | string | yes | Printed on the physical sign; encoded in the stop QR; manual unlock compares `input.toUpperCase() === code`. Convention: `EDITION-N` (e.g. `LANTERN-1`). |
| `story` | object keyed by Dial level | yes — `story.cozy` required | Narrative shown at the stop. Keys: `cozy`, `spooky`, `afterdark`, `overdrive`. A missing level falls back to `cozy`. |
| `puzzle` | object keyed by Dial level | yes — `puzzle.cozy.q` and `puzzle.cozy.a` required | Each variant: `q` (question), `a` (answer), `type` (`"number"` or `"text"`). Answer check is case-insensitive trimmed equality. If no variant exists for the chosen Dial level, `fallback` is used. |
| `fallback` | `{q, a}` | yes — both required | Backup puzzle when no variant exists for the scare level. |
| `hints` | array of strings | yes — exactly 3 | Hint ladder. Convention: hint 3 is the "Ranger assist" (near-answer). |

## Cross-stop rules

- All `puzzle.cozy.a` answers must be **unique** across the 6 stops (case-insensitive), or the pack is rejected.

## Dial levels (4)

`cozy` (Li'l Z — family) · `spooky` (Classic Z) · `afterdark` (Mad Z) · `overdrive` (Full Madness — office/competitive).
Resolution: `story[level] || story.cozy`; `(puzzle[level] || puzzle.cozy) || fallback`.
Write `cozy` first — it's the only required variant. Add `spooky`/`afterdark`/`overdrive`
variants to taste; anything missing degrades gracefully to `cozy`.

> Player support note: the player UI currently offers the first three Dial
> positions; `overdrive` variants in a pack are valid and ignored until the
> player learns the fourth position (a small pending update — the format is
> already ready for it).

## Scoring (not in the pack)

The pack carries no scoring. The backend scores `solved.length * POINTS_PER_STOP`;
the player reports `solved`, `hintsUsed`, `scare`, team, and kit ID.

## Example

A complete valid 6-stop pack: [`wisp-sample.json`](https://github.com/ZQM-Labs/quest-packs/blob/main/sample-quest/wisp-sample.json) in ZQM-Labs/quest-packs.
