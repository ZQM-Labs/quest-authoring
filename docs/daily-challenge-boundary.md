# Daily challenges are not six-stop quest packs

**Status: architecture note, not a new schema version or a supported game type.**
This document distinguishes emerging short-form browser games from the
canonical location-quest content format.

## Existing contract remains unchanged

SPEC v1 defines exactly **six** stops, each with latitude, longitude, a sign
code, a fallback observation puzzle, optional story levels, and three hints.
The validator and player enforce these rules. Do not redefine these fields or
weaken the validator to load unrelated products.

## A proposed separate daily-challenge format

A daily mystery is a **one-question, no-location-permission** experience with
a UTC date, a clue, three candidate answers, a single correct answer, and
optional spoiler-free share text. The proposed experimental implementation is in the
[ZQM Labs site source PR #86](https://github.com/ZQM-Labs/zqmlabs-site/pull/86).
Use the PR as the reviewable source until it merges; do not assume the
prototype is published or accessible from the public game directory. The example is **not** a v1
quest pack and must not be fed to validate_pack.py or the Wisp quest-player.

The experiment's 12 questions are editorial fixtures, not a production
catalog or licensed satellite collection. They are not claimed to be
published on the production website.

## Proposed v0 contract for later review (non-normative)

A future challenge pack could contain:

- schema/version identifier for challenge format, separate from SPEC v1;
- stable question ID, UTC publication date and expiration policy;
- human-reviewed clue and explicit language;
- 3 distinct answers, with exactly one correct candidate;
- source and factual-review metadata, asset license and attribution;
- accessible description of any map/satellite image;
- locale fallbacks and spoiler-free share formatting;
- deterministic date selection and content rotation.

This is a design checklist, not a parser, implementation or release promise.
If approved, create a separate versioned schema and validator with tests
for duplicate IDs, invalid dates, missing attribution, language coverage,
and answer leakage. Review client-side answer disclosure and cheating risk
before introducing competitive leaderboards.

## Content safety and reuse

- Do not collect GPS or map a participant's position for a desk-based quiz.
- Do not publish inferred private locations or user-submitted precise tracks.
- Use original or redistribution-approved imagery with attribution and
  accessible alternatives; no scraped third-party map tiles.
- Never blend paid answer keys, customer materials or QR location codes
  into a public daily-content bundle.
- Treat player submissions and community maps as untrusted; aggregate only
  with consent, privacy review and meaningful participation thresholds.
- Keep game content under ZQM Labs. Technical spatial benchmarks and
  professional GIS service examples belong under ZQM Computing.

## Promotion and release gates

A cross-brand social post can link to a live game and to a related
reproducible engineering demonstration, but neither link is a claim of
booking availability or professional certification. A prototype becomes
playable only after compatibility, accessibility, field/device, privacy,
security, content-rights and independent deployment verification.
