# How to write your first six-stop scavenger hunt (SPEC v1)

**Answer:** start from the public JSON sample, choose **six host-approved**
accessible locations, write one observable puzzle and three hints for
each, validate the result, then verify the target player and route with a
real-device playtest. Editing JSON or running a generator alone does **not**
publish a bookable game.

Audience: a first-time organizer, teacher, museum educator or community
host. No Google Maps scraping, paid service, account, customer data or
new backend is required to learn the format.

## First choose: browser demo, study sample, or hosted experience

| Goal | Correct path | What it does **not** prove |
| --- | --- | --- |
| Try the game immediately | Use the [Wisp's Lost Lanterns browser demo](https://zqmlabs.com/games/hunt-for-wisps/play/?demo=1) **where the current deployment is verified** | A demo is not your own authorized route or an event booking |
| Read a complete pack | Inspect [Wisp's Warm-Up JSON](https://github.com/ZQM-Labs/quest-packs/blob/main/sample-quest/wisp-sample.json) | Original example coordinates, objects and answers are not verified for your venue |
| Prepare a real host kit | Follow this walkthrough, test the exact player and review all six venues | The content validator alone does not make signs, grant site permissions or process payment |

## 1. Inspect the current real spec and source example

Clone the authoring format and the public sample into separate sibling
folders. From their common parent:

```bash
git clone https://github.com/ZQM-Labs/quest-authoring.git
git clone https://github.com/ZQM-Labs/quest-packs.git
python3 quest-authoring/validator/validate_pack.py \
  quest-packs/sample-quest/wisp-sample.json
```

The validator prints `VALID: pack passes all checks` for a compatible fixture;
nonfatal spatial warnings may also appear. The validator does not prove
the sample can be run safely in any neighborhood.

## 2. Plan six **permitted** story/observation stops

Make a one-page table before touching coordinates:

| Stop | Purpose | Example type of observable prompt | Required host action |
| --- | --- | --- | --- |
| 1 | Welcome | Count objects in a host-owned printed illustration | Get sign/venue permission |
| 2 | Place story | Read a verified text panel the host may reproduce | Verify the source and rights |
| 3 | Creative detail | Identify a pattern from licensed artwork | Provide text alternative |
| 4 | Cooperation | Team solves a short visual or word task together | Confirm safe stationary participation |
| 5 | Nature | Observe a non-sensitive feature from a safe path | Verify mobility access and weather plan |
| 6 | Finale | Recap answers at a permitted gathering point | Provide a no-race exit option |

Do not use mailboxes, private homes, school student identities,
restricted sites, dangerous crossings, cliff edges or unlicensed signs
as public location targets. The example pack is a **fixture**, not
venue due diligence.

A typical stop must contain:

```json
{
  "id": 1,
  "name": "Welcome Display",
  "lat": 0.0,
  "lng": 0.0,
  "code": "HOST-1",
  "story": {
    "cozy": "A welcome poster invites your group to start together."
  },
  "puzzle": {
    "cozy": {
      "q": "How many stars are printed on the approved host poster?",
      "a": "4",
      "type": "number"
    }
  },
  "fallback": {
    "q": "How many stars did the organizer announce?",
    "a": "4"
  },
  "hints": [
    "Look at the welcome display.",
    "Count the shapes with five points.",
    "Ranger assist: there are four stars."
  ]
}
```

**That is only a single-stop illustration, not a valid pack.**
Coordinates at 0,0 are deliberately a placeholder and **must never**
be presented as a verified route. A valid pack requires **exactly six
distinct stop IDs (1–6)** and practical, verified host locations.
Check the current [SPEC.md](../SPEC.md) for all constraints. Use
unique `puzzle.cozy.a` answers; the validator normalizes answers.

## 3. Edit the sample JSON and validate it

Copy the sample into a **private working directory** for a planned
edition. Update every stop's name, coordinates, puzzle answers,
fallback clues, three-hint ladder and code. Review the story's
alternate Dial levels: only Cozy is required; absent higher levels
fall back to Cozy. Review exact spelling and the values that real
players are expected to observe. If your venue is indoors or GPS is
unreliable, do not assume an arbitrary radius fixes the issue:
verify the real player and its QR/manual fallback first.

```bash
python3 quest-authoring/validator/validate_pack.py \
  path/to/your-private-six-stop-pack.json
```

Repeat until no errors remain. Warnings about spacing or route
length require human review, even when the command exits successfully.
Store any paid answer keys, nonpublic venue details and access codes
privately. Do not commit them to the public cookbook or sample repo.

## 4. Generate appropriate organizer signage

Follow the [existing QR kit guide](https://github.com/ZQM-Labs/organizer-toolkit/blob/main/qr-kit/README.md).
The QR kit expects a **separate, internally consistent** JSON sign
configuration containing the correct `kit_id`, access code,
six stop codes/names and the intended *verified player URL*. Keep the
configuration private if it contains paid access material.

The authoring repository's **YAML**
`validator/gen_quest_pack.py` creates a **static HTML clue/answer
preview and a metadata manifest**. It is **not** the v1 JSON runtime-pack
compiler, does not validate against SPEC v1, and its static HTML
**displays puzzle answers**. Treat that output as organizer-only; never
publish the answer preview as a secure or paid playable quest.

## 5. Prove the experience before hosting

Record the exact pack SHA/version, QR sign configuration, player commit,
venue approval, device/browser, time and access needs. Test at each
planned stop with the intended participants or representative
accessibility reviewers. Validate:

- GPS check, camera/QR/manual-code fallback, and permission-denied paths.
- Offline/low-connectivity replay, app reopen, battery interruption and
  active service-worker/source-pin version on the actual target device.
- Three-hint ladder, fallback puzzle, all advertised Dial variants, and
  a completion without impossible real-world trivia.
- The safe crossing/stop order, weather and lighting, rest breaks, mobility
  alternatives, opt-out and no-chase policies.
- Sensitive data handling and explicit consent for any event photograph.

Use [ZQM Labs Playtests](https://github.com/ZQM-Labs/playtests)
for a versioned acceptance report. CI and the JSON validator are
necessary but not sufficient field-release evidence.

## 6. Offer an organizer experience only after commercial review

A free browser demo, published sample JSON, approved six-stop
edition and paid hosted event are **different states**. Confirm
regional availability, staff/support capacity, rights, cost, clear
written scope, checkout/fulfillment and any permits before describing
the experience as bookable or white-label.

For human-run schedules and optional observation prompts, see the
[Community Day planner](https://github.com/ZQM-Labs/organizer-toolkit/tree/main/event-kit).
It generates **static plans**, not runtime timed unlocks, live multiplayer,
a global scoreboard or participant location tracking.

**Next step:** validate one private six-stop draft and run one supervised,
authorized field test. That yields more useful evidence than producing
unverified city pages or dozens of fictional editions.
