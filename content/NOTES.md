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
| 2026-07-29 | seneca | `tensions_with` references `epictetus`, which has no figure file yet. | Left in. The frontend degrades to the feature-only view for missing slugs, and the reciprocal must be added when epictetus is extracted. **Resolved — epictetus.json now carries the reciprocal.** |
| 2026-07-29 | epictetus | Nothing survives in his own hand; all text is Arrian's notes. The schema has no field for "this figure did not write this". | Recorded in `confidence_notes.contested` and stated plainly in `who_they_really_were.context`. `voice` describes the register Arrian preserved, not a documented authorial style — a distinction worth keeping in mind if persona mode ever quotes him. |
| 2026-07-29 | epictetus | His silence on his own enslavement is the largest interpretive problem in the figure. Two readings: transcendence of circumstance, or a blind spot so large it undercuts the doctrine. | Recorded as a blind spot, explicitly, and echoed in `limits_and_dangers` as the unexamined origin of the acquiescence failure mode. Treating it as transcendence would have been hagiography. |
| 2026-07-29 | viktor-frankl | PRD R2 applies — in copyright. Risk of the `sources` and `core_beliefs` fields becoming a book substitute. | Kept `sources` pointed hard at buying the actual book, and wrote `positions` as analysis of his framework rather than as a walkthrough of the text. No passages reproduced. |
| 2026-07-29 | viktor-frankl | Pytell's biography documents discrepancies between Frankl's accounts and the record. Two defensible readings: ordinary memory drift, or self-mythologising. | Recorded the discrepancy as fact in `confidence_notes` without adjudicating motive, and listed Pytell in `sources.secondary` so a user can reach the argument directly. |
| 2026-07-29 | nietzsche | The Will to Power is quoted constantly and is not a book he wrote. | Flagged in BOTH `sources.translation_warnings` and `confidence_notes.attribution_warnings` — deliberate duplication, because this is the single highest-frequency error a user will bring to the app, and it should surface from either entry point. |
| 2026-07-29 | nietzsche | `tensions_with` references `dostoevsky`, not yet extracted. | Left in; degrades gracefully. **Resolved — dostoevsky.json now carries the reciprocal.** |
| 2026-07-29 | dostoevsky | Antisemitism in his journalism. Two defensible handlings: contextualise as period-typical, or state it flatly. | Stated flatly in `flaws` with the explicit note that it cannot be waved through as background noise. The PRD's whole case for this product is that it does not flatter; softening the most serious charge against a beloved figure would hollow that out. |
| 2026-07-29 | dostoevsky | His fiction is polyphonic — characters argue positions he opposed, and the strongest arguments are given to opponents. `core_beliefs.positions` assumes a figure holds views. | Wrote `positions` as his authorial commitments where they are discernible, and used `voice.never_does` to record that he has no single resolving voice. Flagged in `attribution_warnings` that quoting characters as him is the standard error. |
| 2026-07-29 | bruce-lee | Everything published under his name is posthumous compilation from notebooks. Nothing was completed. | Recorded in `sources.translation_warnings` and `confidence_notes`. Also moved `start_here` from the famous Tao of Jeet Kune Do to the better-edited Striking Thoughts — fame is not a reason to send someone to the worse edition. |
| 2026-07-29 | bruce-lee | Died at 32, so `positions.fear_and_death` and `positions.relationships` have essentially no material. | Recorded both as genuine absences with an explicit warning not to read equanimity into silence — same treatment as musashi's relationships field. Consistent handling for "the record is empty here". |
| 2026-07-29 | bruce-lee | `tensions_with` references `krishnamurti`, not yet extracted. | Left in; degrades gracefully. **Owed: krishnamurti → bruce-lee.** |

---

## Owed reciprocals

`tensions_with` must be consistent in both directions. Currently outstanding:

- **krishnamurti → bruce-lee** (bruce-lee.json references it; krishnamurti.json doesn't exist yet)

Cleared: epictetus ↔ seneca, viktor-frankl ↔ camus, marcus-aurelius ↔ musashi,
dostoevsky ↔ nietzsche, dostoevsky ↔ camus, marcus-aurelius ↔ epictetus,
marcus-aurelius ↔ nietzsche, musashi ↔ bruce-lee.

Marcus is now the hub — three inbound tensions, all backfilled. Worth watching
that he doesn't become the default comparison for every figure simply because
he was extracted first; a roster where everything is defined against one node
is a weaker synthesis graph than one with real cross-category edges.

---

## Open items

- **Which twelve ship in v1** (TASKS 0.2) is still undecided. Extraction order
  is currently following the figures named in the design doc and the marked
  pilot, not a confirmed launch list.
- **`is_living` needs re-confirming per figure at extraction time.** The flag
  drives the PRD R1 persona-register split, so a wrong value there is a legal
  exposure issue, not a content issue.
