# Quest-Pack Spec (v1)

The player loads a quest pack as JSON and runs it through `validatePack()`.
**A pack that fails validation is rejected wholesale** — the player falls back
to its built-in demo. Validate before you ship.

## Top level

| Field | Type | Required | Meaning |
|---|---|---|---|
| `title` | string | no | Edition display title, e.g. `"Wisp's Lost Lanterns"` |
| `kit` | string | no | Kit ID binding the pack to a kit, e.g. `"DEMO"` |
| `stops` | array | **yes — exactly 6** | Must have length 6 |

## Per stop

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | number | yes | 1-based stop number; QR `?stop=N` target. |
| `name` | string | yes | Displayed as "Stop N: {name}" |
| `lat`, `lng` | number | yes | Map marker + GPS check (haversine) |
| `radius` | number | no | GPS radius in meters (default 30). |
| `code` | string | yes | On the sign + in the QR. Convention: `EDITION-N`. |
| `story` | object | yes — `cozy` required | Narrative; missing → `cozy`. |
| `puzzle` | object | yes — `cozy.q`+`a` | `q`, `a`, `type`; else `fallback`. |
| `fallback` | `{q, a}` | yes — both required | Backup for missing levels. |
| `hints` | string[3] or per-level object | yes — exactly 3 per level | Either a flat array of 3 (used at every level) or `{cozy, spooky, afterdark, overdrive}` with exactly 3 each. Hint 3 is the "Ranger assist". |

## Cross-stop rules

- All `puzzle.cozy.a` answers must be **unique** (case-insensitive),
  or the pack is rejected.

## Dial levels (4)

`cozy` (Li'l Z — family) · `spooky` (Classic Z) ·
`afterdark` (Mad Z) · `overdrive` (Full Madness — office/competitive).
Resolution: `story[level] || story.cozy`; `(puzzle[level] || puzzle.cozy) || fallback`.
Write `cozy` first — it's the only required variant. Add `spooky`/`afterdark`/`overdrive`
variants to taste; anything missing degrades gracefully to `cozy`.

> Player support note: the player UI offers all four Dial positions. Missing
> variants fall back to `cozy`; the authoring format does not require every
> variant to be present.

## Scoring (not in the pack)

The pack carries no scoring. The backend scores `solved.length * POINTS_PER_STOP`;
the player reports `solved`, `hintsUsed`, `scare`, team, and kit ID.

## Example

A complete valid 6-stop pack: [`wisp-sample.json`][sample] in
ZQM-Labs/quest-packs.

[sample]: https://github.com/ZQM-Labs/quest-packs/blob/main/sample-quest/wisp-sample.json
