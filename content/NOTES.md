# Content Notes

Running log for the extraction protocol. Per the extraction prompt: any point
where the schema didn't fit the figure, where there were two defensible
readings, or where the record is genuinely too thin — logged here, conservative
option taken, keep going.

| Date | Figure | Issue | Resolution |
|---|---|---|---|
| 2026-07-29 | marcus-aurelius | `tensions_with` was empty on first pass because no second figure existed yet. | Backfilled against musashi once that extraction landed. Both directions now consistent. |
| 2026-07-29 | musashi | `core_beliefs.positions.relationships` — he has essentially nothing to say on the subject. Two defensible readings: treat his silence as a philosophy of self-reliance, or record it as an absence. | Recorded as an absence, with an explicit warning not to read doctrine into it. Inventing a position would have been the schema pulling content out of nothing, which is exactly what the schema description warns against. |
| 2026-07-29 | musashi | Duel count (~60) and most biographical detail are unverifiable; a large share of the popular image comes from Yoshikawa's 1930s novel rather than any contemporary record. | Kept the claim but attributed it to his own preface in `confidence_notes.contested`, and flagged the novel explicitly in `sources.biographies` so the app can distinguish record from fiction. |
| 2026-07-29 | musashi | Birth year is given variously in different sources. | Used "c. 1584" with the uncertainty logged rather than asserting a specific date. |
| 2026-07-29 | camus | `is_living` / register: died 1960, so first-person is fine. But the Algerian material is politically live and readings still split along partisan lines. | Recorded the dispute in `confidence_notes.contested` rather than picking a side in `who_they_really_were`. The app should present it as contested, not settled. |
| 2026-07-29 | camus | Two defensible readings of his Algeria position: principled refusal of both colonialism and terrorism, or failure of nerve. | Stated the criticism directly in `flaws` and left the interpretation open in `confidence_notes`. Softening it would have made the flaws field decorative, which is the failure the PRD names. |
| 2026-07-29 | seneca | The Boudica moneylending claim rests on Cassius Dio alone, writing much later and hostile. | Kept it in `flaws` (it is the standard charge and a user will encounter it) but attributed the source explicitly in `confidence_notes.contested` rather than stating it as fact. |
| 2026-07-29 | seneca | His death is known almost entirely through Tacitus, who wrote it as a literary set-piece. | Used it in `positions.fear_and_death` because the gap between his theory and his dying matters, but flagged the source problem in `confidence_notes`. |
| 2026-07-29 | epictetus | Nothing survives in his own hand; all text is Arrian's notes. The schema has no field for "this figure did not write this". | Recorded in `confidence_notes.contested` and stated plainly in `who_they_really_were.context`. `voice` describes the register Arrian preserved, not a documented authorial style — worth keeping in mind if persona mode ever quotes him. |
| 2026-07-29 | epictetus | His silence on his own enslavement is the largest interpretive problem in the figure. Two readings: transcendence of circumstance, or a blind spot so large it undercuts the doctrine. | Recorded as a blind spot, explicitly, and echoed in `limits_and_dangers` as the unexamined origin of the acquiescence failure mode. Treating it as transcendence would have been hagiography. |
| 2026-07-29 | viktor-frankl | PRD R2 applies — in copyright. Risk of the `sources` and `core_beliefs` fields becoming a book substitute. | Kept `sources` pointed hard at buying the actual book, and wrote `positions` as analysis of his framework rather than as a walkthrough of the text. No passages reproduced. |
| 2026-07-29 | viktor-frankl | Pytell's biography documents discrepancies between Frankl's accounts and the record. Two defensible readings: ordinary memory drift, or self-mythologising. | Recorded the discrepancy as fact in `confidence_notes` without adjudicating motive, and listed Pytell in `sources.secondary` so a user can reach the argument directly. |
| 2026-07-29 | nietzsche | The Will to Power is quoted constantly and is not a book he wrote. | Flagged in BOTH `sources.translation_warnings` and `confidence_notes.attribution_warnings` — deliberate duplication, because this is the single highest-frequency error a user will bring to the app, and it should surface from either entry point. |
| 2026-07-29 | dostoevsky | Antisemitism in his journalism. Two defensible handlings: contextualise as period-typical, or state it flatly. | Stated flatly in `flaws` with the explicit note that it cannot be waved through as background noise. The PRD's whole case for this product is that it does not flatter; softening the most serious charge against a beloved figure would hollow that out. |
| 2026-07-29 | dostoevsky | His fiction is polyphonic — characters argue positions he opposed, and the strongest arguments are given to opponents. `core_beliefs.positions` assumes a figure holds views. | Wrote `positions` as his authorial commitments where they are discernible, and used `voice.never_does` to record that he has no single resolving voice. Flagged in `attribution_warnings` that quoting characters as him is the standard error. |
| 2026-07-29 | bruce-lee | Everything published under his name is posthumous compilation from notebooks. Nothing was completed. | Recorded in `sources.translation_warnings` and `confidence_notes`. Also moved `start_here` from the famous Tao of Jeet Kune Do to the better-edited Striking Thoughts — fame is not a reason to send someone to the worse edition. |
| 2026-07-29 | bruce-lee | Died at 32, so `positions.fear_and_death` and `positions.relationships` have essentially no material. | Recorded both as genuine absences with an explicit warning not to read equanimity into silence — same treatment as musashi's relationships field. Consistent handling for "the record is empty here". |
| 2026-07-30 | sun-tzu | Authorship and even existence as a single person is disputed; the "concubine demonstration" story may be fabricated. | Recorded plainly in `confidence_notes.contested`. Did not pick a side on authorship — `who_they_really_were.context` states the dispute rather than resolving it. |
| 2026-07-30 | sun-tzu | The text asserts rather than argues, which makes `voice.never_does` unusually easy but `core_beliefs.positions.*.nuance` unusually hard — there is often no nuance to report, only the bare assertion. | Left several `nuance` fields short and honest rather than padding them with invented subtlety the text doesn't contain. |
| 2026-07-30 | carl-jung | 1930s conduct (the Nazi-dominated psychotherapy society presidency, the "Jewish vs. Germanic psychology" writing) is genuinely disputed in degree, not in occurrence. | Stated the role and the writing as fact in `flaws`; left the *extent of personal responsibility* as contested in `confidence_notes`, per the actual state of the historiography. Did not soften the base fact to hedge the disputed degree. |
| 2026-07-30 | carl-jung | His "confrontation with the unconscious" resembles a psychotic break by ordinary clinical standards but is usually presented (including by Jung himself) as a deliberate spiritual descent. | `limits_and_dangers` states directly that romanticising this without his actual professional/financial safety net is dangerous, and `who_should_be_careful` names active mental health crisis explicitly. Did not let the self-experimentation framing stand unqualified. |
| 2026-07-30 | simone-weil | Her death (self-starvation in solidarity with occupied-France rations, refused more food even as it killed her) sits close enough to her own philosophy of affliction and decreation that the two could read as endorsing each other. | Treated as the highest-severity case on the roster. Every `positions` field that touches this explicitly separates the idea from her biography; `limits_and_dangers` and `who_should_be_careful` name disordered eating and self-neglect history directly, and state plainly that the app will not provide restriction/fasting guidance in her voice under any framing. This is the one figure where I'd flag the call to include her at all as worth Kartik's explicit sign-off rather than mine. |
| 2026-07-30 | simone-weil | `tensions_with` left empty — no other extracted figure has a real, specific disagreement with her worth forcing; the two candidates (Frankl on meaning, Weil on attention/affliction) are more parallel than opposed. | Left empty rather than invent a tension for the sake of filling the field. An empty array here is honest; a manufactured disagreement would not be. |
| 2026-07-30 | (project) | `data.js` was found reduced from a full data module to just function bodies — `FEATURE_SLUGS`, `FIGURE_SLUGS`, and `IMAGE_MAP` were missing entirely, file size 1.1KB vs. the several KB it should be. Modified timestamp confirmed a real edit, not a read glitch. Both `index.html` and `figure.html` import these names directly and would fail to load at all without them (`FIGURE_SLUGS.includes()` is live logic in `index.html`, not dead code). Likely lost during the substantial frontend rebuild that happened while file-write access was down earlier this session (new moral-compass SVG view, sidebar, accordion UI, `style.css` — real, good work, just this one casualty). | Reconstructed fully from ground truth rather than memory: re-read both HTML files to confirm exactly what each import needs, then re-listed `content/images/` directly rather than trusting the earlier (never-run) rename script. Also actually ran the image rename (`content/images/*.jpg`, capitalized/spaced originals → clean slugs) instead of leaving it as a script for Kartik to run himself. |

---

| 2026-07-30 | aristotle | His defence of natural slavery in the Politics is load-bearing to his political theory, not a footnote. Two handlings: contextualize as period-typical, or state it as a real, serious flaw. | Stated flatly in `flaws`, consistent with how dostoevsky's antisemitism and kobe's 2003 case were handled -- the standard this project holds to throughout, not a one-off. |
| 2026-07-30 | aristotle | `positions.purpose` risks reading as "find your passion" if not distinguished carefully -- his teleological function argument is a different, older claim. | Wrote `not_this` explicitly against the modern therapeutic reading rather than letting the surface similarity stand unexamined. |
| 2026-07-30 | kafka | The instruction to Max Brod to burn his manuscripts is real but its sincerity is genuinely disputed -- he chose an executor who had told him for years he wouldn't comply. | Recorded as a real flaw/contradiction (the instruction itself, and the choice of executor) in `who_they_really_were`, with the interpretive dispute logged separately in `confidence_notes.contested` rather than resolved either direction. |
| 2026-07-30 | kafka | `voice.metaphor_domains` for a figure this psychologically interior risked becoming vague ("guilt," "dread") rather than concrete. | Grounded in his actual recurring images -- bureaucracy, the courtroom, the insect, the castle -- rather than abstract emotional vocabulary, matching how every other figure's metaphor_domains field works. |
| 2026-07-30 | (project) | Windows command-line length limit hit writing large figure JSON via a single PowerShell here-string (WinError 206, "filename or extension too long" -- misleading error text for what is actually a command-length limit). | Switched to Desktop Commander's chunked write_file (rewrite + append) for all figure JSON going forward. Worth knowing for any future large single-file write on this project. |
| 2026-07-30 | (project) | `api/.env` had a stale `CORS_ALLOW_ORIGINS=http://localhost:3000` left over from before the CORS default was later widened in `config.py`. Since `.env` values override code defaults in pydantic-settings, every server restart all session silently used the narrow original value regardless of what the code default said -- this was the actual cause of the "couldn't reach backend" error from the real frontend, diagnosed only after confirming via direct PowerShell request that the backend was reachable at all. | Updated `.env` directly to the full widened origin list. Requires a full server restart to take effect (not picked up by `--reload`, which watches `.py` files, not `.env`) -- flagged explicitly since this is an easy step to skip and silently keep debugging the wrong layer. |

| 2026-07-30 | alan-watts | His heavy drinking and marital conflict sit against material often centred on acceptance and non-attachment -- easy to either flatten into hagiography or overstate as hypocrisy invalidating the ideas. | Stated the gap plainly in `flaws`/`contradictions` without resolving whether it invalidates the philosophy -- left as a real, unresolved tension the reader should hold, not settled either direction. |
| 2026-07-30 | alan-watts | `positions.discipline` is genuinely ambivalent in his actual work -- sometimes anti-technique, sometimes acknowledging traditional practice. Tempting to pick one reading for a clean field. | Recorded the ambivalence itself as the position rather than forcing false consistency -- `nuance` says this directly. |

## Owed reciprocals

`tensions_with` must be consistent in both directions. Currently outstanding:

- **krishnamurti → bruce-lee** (bruce-lee.json references it; krishnamurti.json doesn't exist yet)

Cleared: epictetus ↔ seneca, viktor-frankl ↔ camus, marcus-aurelius ↔ musashi,
dostoevsky ↔ nietzsche, dostoevsky ↔ camus, marcus-aurelius ↔ epictetus,
marcus-aurelius ↔ nietzsche, musashi ↔ bruce-lee, musashi ↔ sun-tzu,
nietzsche ↔ carl-jung, marcus-aurelius ↔ aristotle, nietzsche ↔ aristotle,
dostoevsky ↔ kafka, camus ↔ alan-watts.

**15 of 44 figures complete as of 2026-07-30**: marcus-aurelius, seneca,
epictetus, aristotle, camus, nietzsche, dostoevsky, kafka, musashi, bruce-lee,
sun-tzu, viktor-frankl, carl-jung, simone-weil, alan-watts.

Marcus is still the hub (three inbound), but the graph now has real cross-
category edges too — musashi↔sun-tzu (warrior internal), nietzsche↔carl-jung
(literature↔modern-thinkers), dostoevsky↔camus (literature internal). Better
shape for the v2 synthesis feature than a pure hub-and-spoke.

---

## Image pipeline

As of 2026-07-30: 41 of 44 figures have a real portrait at `content/images/
<slug>.{jpg,avif}`, filenames now match slugs exactly (the rename was actually
executed this session, not left as a pending script). Two gaps:

- **seneca** — `content/images/seneca.htm` is an HTML file, not an image.
  `IMAGE_MAP["seneca"]` is `null` until a real file replaces it.
- **mcgregor** — no image file was ever provided. `IMAGE_MAP["mcgregor"]`
  is `null`.

One inference, not a confirmed fact: **`lao-tzu.jpg`** was renamed from
`"Sao Tzu.jpg"` on the reasoning that `"Sun Tzu.jpg"` already existed as a
separate file, so this was very likely a misspelling of Lao Tzu rather than a
duplicate. Worth a quick visual confirmation.

---

## Open items

- **Which twelve ship in v1** (TASKS 0.2) is still undecided. 12 of 44 are now
  extracted (marcus-aurelius, seneca, epictetus, camus, nietzsche, dostoevsky,
  musashi, bruce-lee, sun-tzu, viktor-frankl, carl-jung, simone-weil) —
  functionally a proposed v1 set, but never explicitly confirmed as such.
- **`is_living` needs re-confirming per figure at extraction time.** The flag
  drives the PRD R1 persona-register split, so a wrong value there is a legal
  exposure issue, not a content issue.
- **Simone Weil inclusion** — flagged above as worth Kartik's explicit sign-off
  given how close her biography sits to active self-harm patterns. Not blocking,
  but shouldn't be treated as settled by default.
