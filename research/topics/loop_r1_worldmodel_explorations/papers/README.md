# Package layout and file status

Four papers, each in its own folder. Every folder mixes **unedited AutoDiscussion output** with
**reviewed deliverables**, and the two are not distinguishable by filename alone — hence this table
and the status banner at the top of every file.

| File | Status | What it is |
|---|---|---|
| `paper-draft.revised.md` | ✅ **CURRENT** | The manuscript. Carries every review correction; revision log at the end |
| `experiment-spec.md` | ✅ **CURRENT** | The implementation spec. **Edited in place** — there is no `.revised` sibling |
| `paper-draft.md` | ⚠️ superseded | Unedited AutoDiscussion output, kept for provenance and for diffing |
| `research-report.md` | ⚠️ superseded | Unedited AutoDiscussion report. **Still contains defects that were corrected elsewhere** |
| `seed.md` | 📌 input | The `idea_text` that drove the room, plus the novelty ledger. **Not the delivered design** — ZW1's and ZW2's contain instructions the manuscripts now contradict |
| `autodiscussion_draft_review.md` | 📖 record | Review as of 2026-08-21. **ZW2's and ZW4's each endorse a design later reversed.** Absent for ZW1 — see below |
| `major_fix*.md` | 📖 record | Diagnosis written before a fix could be merged |

**The asymmetry is deliberate but was not planned.** `paper-draft.md` was copied and revised into a
sibling, so the original survives in-package. `experiment-spec.md` was edited in place, so it has no
in-package original. Both unedited originals — and `research-report.md`'s — survive upstream in
`paper_autodiscussion/completed_jobs_dirs/<job>--<room>/`. Renaming the spec now would break every
line reference in `MAJORS.md` and in the review history, so the convention is documented rather than
retrofitted.

**ZW1 has no `autodiscussion_draft_review.md`.** Its room review was written directly into
`major_fix_rlfr_anchor.md` because the RLFR anchor was the only finding worth recording, and the file
was never renamed. Nothing is missing; the inventory is just not uniform. Documented rather than
retrofitted, for the same reason as the spec asymmetry above.

**`research-report.md` is the trap.** It is the one file that looks authoritative, is never marked as
draft output by its own content, and still contains superseded designs — the `V`-based estimand in
ZW2, Hájek weighting in ZW3, the saturated factorial and bisection in ZW4, `assume false;` stubs in
ZW1. It was never reviewed in any of the five rounds, because every round examined `paper-draft` and
`experiment-spec` only. Each copy now opens with a banner naming what in it is stale.

## Reading order

For the design: `paper-draft.revised.md`, then `experiment-spec.md`.
For why it looks like that: `../README.md` (family framing and the verification record), then
`MAJORS.md` (every major, verbatim, with where it was fixed and which round found it).

## Status

| Paper | Room | Gate at close | Majors found across 5 rounds |
|---|---|---|---|
| ZW1 Typed Obligation Verdicts | `29167d1d` | 5/6 clean, 1 major | 5 room + 9 review |
| ZW2 Verified but Wrong | `98e3ae6b` | 5/6 clean, 1 major | 5 room + 7 review |
| ZW3 Which Prover Teaches Software | `9f4da36d` | 4/6 clean, 2 majors | 4 room + 3 review — **first to pass a strict full-package review** |
| ZW4 Oracle Economics | `7bcfe3ef` | 5/6 clean, 1 major | 5 room + 8 review |

Round 9 re-read all four packages after the round-7 corrections and the round-8 scoop-sweep wording
changes, and ZW3 passed clean for the third consecutive round. Round 10's edits (three mirror-failure
fixes, below) post-date that strict pass and have not themselves been re-read.

Ten adversarial passes, forty-four indexed findings — all in `MAJORS.md`. Round 3 found a defect
introduced by round 2; round 5 found two invisible to any single-artifact review; round 6 read the
four `seed.md` inputs and three `autodiscussion_draft_review.md` records for the first time and found
nine more, including two record files that endorse designs their own manuscripts now argue against
and one third-party attribution error that had been corrected everywhere except the file it
originated in.

**Every file in all four packages has been read in review, in full, from byte one.** Round 7 found
that three of the four specs opened with an agent's stray chat narration above the title — invisible
to six rounds that all began reading at the `#` heading — so "reviewed" now means the whole file, not
the sections that look like content. Treat "no known majors" as exactly that.

Round 8 (2026-08-23) was a different kind of pass: a fresh **internet scoop re-sweep** of all four
packages by four parallel web auditors before repository publication. Zero scoops. ZW1 and ZW4 CLEAR;
ZW2 and ZW3 took wording-level narrowings (applied same day to manuscript and seed); one round-4
provenance correction (the RLFR Wayback record) was itself corrected. Details in `MAJORS.md` § Round 8
and in each seed's dated re-sweep block.

Round 10 (2026-08-23) ran a different instrument: the deer-flow `academic-paper-review` +
`deep-research` skills, four parallel web-grounded structured reviews, one
`deerflow_review_2026-08-23.md` per package. All four: Weak Accept as pre-registered designs,
Moderate contribution. Three majors applied same day — a fourth fixed-`K=32` survivor in ZW1's RQ4,
five residual reversed-estimand `V−B` passages in ZW2's Method/Experiments (+ one spec mirror), and
ZW4's never-absorbed round-8 citations plus its JURY-RL-falsified "unmeasured" universal. The
mirror-failure pattern held for a third consecutive round. Details in `MAJORS.md` § Round 10.

Round 9 (2026-08-23) re-read all four packages after those edits and found five more, three of them
the same shape: **a defect fixed in one artifact and never mirrored into the other.** ZW1's manuscript
still asserted the fixed-`K=32` packet design that round 7 had excised from its spec in ten places —
one sentence contradicting the paragraph beneath it — and still named an arm `G3b`, an identifier
from the withdrawn six-arm seed table that is defined in neither current artifact. ZW2's Related Work
still framed the paper's contribution against the estimand round 2 reversed. The pattern is that
**Related Work is where a withdrawn design hides longest**: written early, restating the contribution
in its own words, untouched by any later fix to the method. Details in `MAJORS.md` § Round 9.
