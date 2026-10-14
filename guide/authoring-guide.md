# Authoring Guide — writing a great quest

## The shape of a stop

Every stop is a tiny story with a job: **get players looking at the real world.**
The puzzle answer must come from something players can see, count, or read at
the waypoint — never from trivia they can't observe on site.

Good: "How many wooden swings face the oak?" (countable on site)
Bad: "In what year was this oak planted?" (trivia, uncheckable, unfun)

## The Dial: three levels, one stop

Write `cozy` first — it's required and it's the default. Then escalate:

- **Cozy** — all ages. Concrete, countable, kind. ("How many pumpkins are smiling?")
- **Spooky** — teens+. Riddles, light mischief, atmosphere. ("I have a face but cannot see…")
- **After Dark** — adults/competitive. Wordplay, ciphers, multi-step. Harder, never meaner.

If a level has no variant, the player falls back gracefully — so a Cozy-only
pack is perfectly valid. Don't pad levels with weak puzzles; two strong levels
beat three mediocre ones.

## The hint ladder (exactly 3)

1. **Nudge** — restates where to look. ("Look low — lanterns love the ground.")
2. **Focus** — narrows it down. ("Count slowly, out loud, as a team.")
3. **Ranger assist** — near-answer. ("Ranger assist: the smiling pumpkins are 4.")

Hints are free in the current scoring. Write hint 3 so a stuck team *will*
finish — a finished quest beats an abandoned one.

## Puzzle types

- `"number"` — counting, arithmetic on observed digits. Most reliable.
- `"text"` — short answers (a color, a word on a sign). Keep answers to 1–2 words;
  the check is case-insensitive trimmed equality, so avoid answers with tricky
  spelling.

## The uniqueness rule

All six `puzzle.cozy.a` answers must differ (case-insensitive) — the validator
rejects duplicates. Plan your six answers before you write the puzzles.

## Route craft

- 6 stops, 2–4 minutes apart on foot. 30–60 minutes total.
- Vary the verbs: count, find, read, listen, spot-the-difference.
- End near the start — the finale gathering matters more than the last puzzle.
- Walk it yourself, in order, at the time of day players will. Every time.

## Before you ship

`python3 validator/validate_pack.py my-pack.json` — zero errors, then playtest
with real humans who haven't seen the answers. See
[ZQM-Labs/playtests](https://github.com/ZQM-Labs/playtests).
