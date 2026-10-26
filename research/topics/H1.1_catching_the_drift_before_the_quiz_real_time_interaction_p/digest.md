# Digest: Catching the Drift Before the Quiz: Real-Time Interaction-Pattern Classification as a Just-in-Time Intervention Against AI-Induced Skill Erosion

> **REVERSE-DIGEST NOTICE.** No paper exists yet. This is speculative scaffolding for research
> planning, built from a seed idea (topic code H1.1, family H1 — new, not a sub-topic of any
> existing B/T family) as if a paper answering the seed's core question had already been written.
> Tags: **[GIVEN]** = from the seed README; **[HYPOTHESIS]** = reasoned elaboration, not fact;
> **[PLACEHOLDER]** = unknowable until the work is done; **[GROUNDED:web-read]** = a REAL paper
> whose abstract page and/or full text was fetched and read on 2026-08-13 (not inferred from a
> secondhand relay); **[GROUNDED:web-search]** = a REAL paper whose title/authors/venue/abstract
> were confirmed via search-result text, but whose full text was not fetched — weaker than
> web-read, flagged accordingly. Do not cite [HYPOTHESIS]/[PLACEHOLDER] content as fact.

---

## Origin and freshness note

This topic did not come from `38_topics.txt`, from a paper corpus scan, or from an arXiv
trend-mining pass — it came from mining YouTube industry-commentary transcripts
(`workenv_chanllege/bestpartners`, `workenv_chanllege/whycallqq`) for signals outside this
repo's existing B1-B6/T3/T5 taxonomy (see `industry_signal_scan_2026-08.md` Part 2 §9). Two
channels independently described what sounded like two separate skill-atrophy studies. **On
primary-source verification (2026-08-13), these turned out to be the SAME paper** — Shen &
Tamkin's `arXiv:2601.20245`, described once as "Anthropic's Trio-library RCT" and once as "How
AI Impacts Skill Formation, n=52" by two different YouTubers narrating the same release. This is
exactly the failure mode the freshness-check discipline (first applied to topic B1.6) exists to
catch: **the original "triple corroboration" claim in the industry-signal-scan doc is corrected
to a double corroboration** — two genuinely independent studies (Shen & Tamkin's coding RCT, and
Kosmyna et al.'s EEG essay-writing study), not three. Both are now read in full below, along with
two more directly relevant papers found via targeted search (Yao's `2606.06253`; Aouad, Lykouris
& Zhong's `2605.11350`) and one established HCI anchor (Cao & Huang, CSCW2 2022). This is a
materially stronger grounding set than the industry scan alone provided, and the correction
matters: the core question below is scoped against what these five papers actually do, not
against a miscounted signal.

---

## N0 Metadata

- **title** [GIVEN]: "Catching the Drift Before the Quiz: Real-Time Interaction-Pattern
  Classification as a Just-in-Time Intervention Against AI-Induced Skill Erosion" (seed README).
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper exists.
- **abstract** [HYPOTHESIS] (drafted, not real):
  > "A randomized controlled trial recently showed that developers learning a new library with
  > AI assistance score 17 percentage points lower on post-task comprehension and debugging
  > quizzes than developers working unaided, and identified six distinct AI-interaction patterns,
  > three of which preserve learning and three of which erode it — but that measurement happens
  > only after the fact, in a quiz. We ask whether the same interaction-pattern signal can be
  > detected *during* the task, early enough to intervene before the skill-erosion outcome is
  > locked in, and whether a lightweight, real-time intervention (nudging a learner from a
  > code-delegation query pattern toward a comprehension-preserving one) measurably improves the
  > downstream quiz outcome relative to an unintervened AI-assistance control. We extend a
  > published skill-formation RCT design with a third arm — real-time classification plus
  > just-in-time intervention — and report whether early behavioral signal is both detectable and
  > actionable, not merely diagnostic after the damage is done."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: primary `"SE"` (developer-tooling / software-engineering
  education), secondary `"HCI"` (real-time reliance-calibration intervention design, per Cao &
  Huang's precedent), tertiary `"AI/ML"` (the interaction-pattern classifier itself).

**Status:** PARTIAL — placeholder/hypothesis only.
**absence_comment:** {"what_missing": "No actual paper exists.", "why_matters": "Any bibliographic claim here would be fabricated if presented as fact.", "implication": "Re-derive N0 from the real paper once written."}

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS]: "measure whether a real-time classifier — trained to recognize
  the early behavioral signature of the three skill-eroding interaction patterns [HallucAI
  note: not a real citation key, see N3] Shen & Tamkin already identified (AI delegation,
  progressive AI reliance, iterative AI debugging) — can detect a learner drifting into one of
  those patterns early enough in a task to trigger a just-in-time intervention, and whether that
  intervention causally improves the downstream skill-formation outcome (post-task quiz score)
  relative to unintervened AI assistance, using the same task/quiz instrument as the published
  baseline RCT for direct comparability."
  - Self-check: kind of task = a causal intervention study extending a published RCT with a
    third arm; domain = novice/early-career developers learning an unfamiliar library with AI
    assistance; outcome shape = a quiz-score delta directly comparable to the base paper's own
    50%/67% numbers, plus a detection-lag statistic (how early the classifier fires). All three
    land, and the direct numeric comparability to a real, published baseline is a strong design
    property this topic gets for free.
- **inputs** [HYPOTHESIS]:
  1. The base paper's task design: an unfamiliar-library coding task (Trio, or a comparable
     substitute if Trio-specific materials are not reusable) with a post-task quiz.
  2. A real-time interaction-pattern classifier operating on session-observable features only
     (query text, query timing, whether a query requests runnable code vs. an explanation,
     whether a follow-up question is asked after code is returned, error/retry counts) — no
     model-internal access required, matching what an interaction pattern actually is per the
     base paper's own qualitative taxonomy.
  3. A library of just-in-time interventions the AI assistant can trigger (e.g., appending a
     comprehension-check question to its next response instead of only returning runnable code;
     temporarily withholding a fully-runnable answer in favor of a partial one plus a guiding
     question) — a **design space**, not a single fixed intervention, since which intervention
     works (if any) is itself part of what's unknown.
  4. A held-out validation set of session transcripts pre-labeled by the base paper's own
     taxonomy (six patterns) to check the classifier's real-time predictions against the
     eventual ground-truth pattern label a human coder would assign in hindsight.
- **outputs** [HYPOTHESIS]:
  1. Per-participant: assigned condition (hand-coding / AI-assist-only / classify-and-intervene),
     quiz score, detection lag (how many queries elapsed before the classifier's first
     eroding-pattern flag, if any), and whether/which intervention fired.
  2. A classifier precision/recall report against the hindsight-labeled validation set —
     detecting a pattern in real time from a partial session is a strictly harder problem than
     the base paper's own post-hoc, full-session labeling, and this must be reported honestly as
     its own result, not assumed to work.
  3. A quiz-score comparison across all three arms, directly plotted against the base paper's own
     published 50%/67% two-arm numbers.
- **constraints** [GIVEN/CONFIRMED, revised after reading the full base paper]: the base paper's
  own stated scope limits apply here too — the population is developers with prior general
  programming experience but no experience with the specific library, and its own limitations
  note the setup "differs from agentic coding products" and that effects there "are likely to be
  more pronounced" — so this topic's results should be read as a lower bound on real-world
  agentic-coding-tool skill-erosion risk, not an upper bound; ground truth for the outcome is the
  base paper's own quiz instrument, not a novel one, so results are comparable rather than
  incommensurable.

**Status:** PARTIAL — inferred from the seed and the now fully-read base paper.
**absence_comment:** {"what_missing": "No written Problem Formulation exists.", "why_matters": "The real-time classifier's feasibility is itself unverified — see N5/N6 for why this is the central open risk of the whole topic.", "implication": "Treat this as the most conservative reading consistent with the confirmed base paper."}

---

## N2 Motivation

**motivations:**
- **motivation_text** [GROUNDED:web-read]: "Shen & Tamkin's RCT (`arXiv:2601.20245`, Anthropic,
  Jan 2026) is the field's first clean causal evidence that AI assistance can measurably impair
  skill formation: 52 developers learning the Trio library scored 50% (AI-assisted) vs. 67%
  (hand-coding) on a post-task quiz (Cohen's d=0.738, p=0.01), with the largest gap on debugging
  questions. Crucially, the paper does not treat this as inevitable — it identifies six
  interaction patterns, three of which (fully delegating code generation, progressively
  offloading more work, using AI only to debug rather than to understand) score below 40%, and
  three of which (generating code then asking follow-up comprehension questions; hybrid
  code-plus-explanation queries; purely conceptual questions) score 65-86%. The paper's own
  stated open questions include exactly the gap this topic targets: whether the effect
  'dissipates longitudinally' and — most directly — it never asks whether the *pattern itself*,
  which it only characterizes in hindsight across a full completed session, could be detected
  and acted on *while the session is still happening*."
- **motivation_text** [GROUNDED:web-read]: "An independent study using a completely different
  method and domain — Kosmyna et al. (MIT Media Lab, `arXiv:2506.08872`, preprint, not yet
  peer-reviewed) — found EEG evidence of the same qualitative direction in essay writing: LLM
  users showed the weakest, least distributed brain connectivity of three conditions
  (LLM/search-engine/brain-only), the lowest self-reported sense of essay ownership, and reduced
  memory recall. This is genuinely independent corroboration (different task, different
  instrument, different population) of the same underlying concern Shen & Tamkin's coding RCT
  raises, which is why this topic treats 'AI assistance can erode the skill/comprehension it
  appears to accelerate' as a load-bearing premise rather than a single-study fluke — while
  being explicit that this is *two* independent findings, not three (see the freshness note
  above for the miscount this correct)."
- **motivation_text** [GROUNDED:web-read]: "Yao's `arXiv:2606.06253` ('When the Scaffold Stays
  On') shows a related behavioral signature — 'more first-attempt acceptances, fewer debugging
  retries' — is detectable at scale from competitive-programming platform submission data across
  AI-rollout cohorts, and that AI-prohibited evaluation gates (ICPC, IOI) successfully screen for
  which practice style produced durable skill. This establishes that *behavioral signatures of
  AI-usage style are observable in naturalistic data*, which is direct precedent for this topic's
  central technical bet (a real-time classifier on interaction features) — but Yao's signature is
  observational/retrospective at the cohort level, not built to fire mid-session on an individual
  learner, and never closes the loop into an intervention."
- **motivation_text** [GROUNDED:web-search]: "Cao & Huang (CSCW2, 2022, 'Understanding User
  Reliance on AI in Assisted Decision-Making') already established, in the adjacent
  AI-assisted-decision-making literature, that a real-time behavioral proxy (eye-gaze duration on
  an AI suggestion) correlates with reliance more informatively than retrospective self-report —
  direct precedent for 'a cheap, real-time, non-invasive behavioral signal can substitute for a
  post-hoc measurement of reliance/reliance-quality.' That literature has not, to this digest's
  knowledge, been connected to the skill-*formation* (not just decision-accuracy) outcome Shen &
  Tamkin measure, nor extended into a closed-loop intervention."
- **motivation_text** [HYPOTHESIS]: "Aouad, Lykouris & Zhong's theoretical model
  (`arXiv:2605.11350`) formalizes conditions under which AI assistance produces 'skill
  polarization' when AI literacy is heterogeneous — giving this topic a theoretical account of
  *why* real-time intervention could matter: if the polarizing mechanism operates through
  early, compounding differences in how learners interact with AI (matching Shen & Tamkin's
  interaction-pattern framing empirically), then an early intervention that shifts a learner's
  trajectory before compounding sets in is exactly the lever the theory predicts should work —
  though this is this digest's inference connecting a theory paper to an empirical design, not a
  claim either paper makes itself."

**Status:** PARTIAL — five real, verified sources ground the motivation; the causal chain linking
early-intervention design to the theory paper's polarization mechanism is this digest's inference.
**absence_comment:** {"what_missing": "No paper-level Motivation exists; the linking argument between Aouad et al.'s theory and this topic's intervention design is speculative.", "why_matters": "A reviewer could reasonably ask for a sharper theoretical justification for why early intervention specifically (rather than, say, post-hoc retraining) should work.", "implication": "Treat the theory connection as motivating color, not as a claim requiring its own falsification — the empirical RQ1/RQ2 below carry the real weight."}

---

## N3 Related Works

Search protocol actually run: targeted web search (not the local `topics/corpus/ideas.jsonl`,
which returned only noise — the local corpus is OpenReview ML/NeurIPS/ICLR + Nature
Communications through ~2025, and this is a 2025-2026 HCI/CS-education/labor-economics
crossover subfield it doesn't cover) for (a) the two studies the industry-scan transcripts named,
confirming they are the same paper; (b) directly adjacent recent work on AI-and-skill-formation;
(c) an established anchor in the real-time-reliance-detection HCI literature. Four of five works
below were fetched and read in full or near-full (title+abstract+extracted body); one
(Cao & Huang) was confirmed via search-result text only, not full-text-fetched, and is flagged
weaker accordingly.

**works:**

1. **citation_key**: `[SkillFormationRCT, Shen & Tamkin, arXiv:2601.20245]` —
   [GROUNDED:web-read; full text fetched 2026-08-13]
   **approach_summary**: "Randomized controlled trial: 52 developers (1+ year Python experience,
   unfamiliar with the Trio async library) split into AI-assisted vs. hand-coding conditions on a
   two-task Trio exercise, then a post-task quiz. AI-assisted group scored 50% vs. 67% for
   hand-coders (Cohen's d=0.738, p=0.01), with no significant time savings. Identifies six
   interaction patterns by qualitative coding of session transcripts: three delegation-heavy
   patterns score <40%, three comprehension-seeking patterns score 65-86%. States as future work:
   effects beyond coding, whether the effect dissipates longitudinally, and whether AI assistance
   differs from human assistance while learning."
   **paper_url**: https://arxiv.org/abs/2601.20245
2. **citation_key**: `[CognitiveDebt, Kosmyna et al., arXiv:2506.08872]` — [GROUNDED:web-read;
   summary page fetched 2026-08-13; preprint, not peer-reviewed]
   **approach_summary**: "54 participants (18 in a session-4 crossover) write essays under three
   conditions (LLM-assisted, search-engine-assisted, brain-only) across four sessions, with EEG
   measurement of neural connectivity plus NLP scoring of essays. LLM users show the weakest,
   least distributed brain connectivity; lowest self-reported essay ownership; reduced memory
   recall of their own writing. Session-4 crossover: LLM-to-brain-only switchers show reduced
   alpha/beta connectivity (under-engagement); brain-to-LLM switchers show connectivity closer to
   search-engine users."
   **paper_url**: https://www.media.mit.edu/publications/your-brain-on-chatgpt/
3. **citation_key**: `[ScaffoldStaysOn, Yao, arXiv:2606.06253]` — [GROUNDED:web-read; abstract
   fetched 2026-08-13]
   **approach_summary**: "Analyzes competitive-programming submission patterns across Codeforces
   (unproctored, AI-permitted) vs. ICPC/IOI (AI-prohibited, proctored) to identify an
   'AI-prompt signature' — more first-attempt acceptances, fewer attempts, fewer debugging
   retries — that emerges in unproctored settings post-AI-rollout across entry cohorts. Within
   the AI-prohibited settings, the same signature predicts *higher* performance for newer
   entrants, interpreted as AI-style practice supporting frontier skill development when gated by
   evaluation controls that screen out substitute-use. Concludes institutional design
   (AI-prohibited evaluation gates) matters more than blanket prohibition."
   **paper_url**: https://arxiv.org/abs/2606.06253
4. **citation_key**: `[ProductivityParadox, Aouad, Lykouris & Zhong, arXiv:2605.11350]` —
   [GROUNDED:web-read; abstract fetched 2026-08-13]
   **approach_summary**: "A mathematical model of workers with heterogeneous skill making effort
   decisions under AI assistance, showing that when skill development or AI reliability is
   endogenous, increased AI assistance can degrade steady-state productivity, and that
   heterogeneity in AI literacy (ability to recognize and correct flawed AI output) can produce
   skill polarization rather than convergence. Purely theoretical/simulated; no human-subjects
   data."
   **paper_url**: https://arxiv.org/pdf/2605.11350
5. **citation_key**: `[RelianceGaze, Cao & Huang, CSCW2 2022]` — [GROUNDED:web-search; abstract
   confirmed via search results only, full text not fetched]
   **approach_summary**: "In an AI-assisted spatial-reasoning decision task, shows percent
   gaze-duration on an AI suggestion correlates strongly with both AI-agreement behavior and
   self-reported reliance, and that user agency is best preserved when task difficulty is low or
   AI performance is inconsistent — establishing a real-time, non-self-report behavioral proxy
   for reliance quality as a viable alternative to retrospective measurement."
   **paper_url**: https://dl.acm.org/doi/10.1145/3555572

**Status:** PARTIAL — four of five works read from fetched pages; one (Cao & Huang) confirmed
only via search snippets, flagged as the weakest-grounded citation in this set.
**absence_comment:** {"what_missing": "The local project corpus (`topics/corpus/ideas.jsonl`) contains no relevant works for this subfield — all five anchors came from live web search, a different sourcing method than every other topic in this repo's map. Cao & Huang's full text was not read.", "why_matters": "A real paper needs a fuller HCI-reliance-calibration literature review than these five anchors, and should verify the Cao & Huang summary against the actual paper text.", "implication": "Before drafting the real paper, fetch and read Cao & Huang in full (or find an accessible mirror — the ACM DL page returned HTTP 403), and run a broader search for the appropriate-reliance/automation-bias literature this topic's intervention design draws on."}

---

## N4 Prior Limitations

**limitations:**
1. **limitation_text** [GROUNDED:web-read — confirmed against the full paper]: "[SkillFormationRCT]
   measures its six interaction patterns by *post-hoc qualitative coding of complete session
   transcripts* — it never attempts real-time classification, and its own stated future work
   ('whether this effect dissipates longitudinally') is about time-since-training, not about
   within-session early detection. It also explicitly notes its own sample is small and its
   setup 'differs from agentic coding products,' where effects are expected to be more
   pronounced — this topic inherits that same population-scope caveat."
   **affects_works**: ["[SkillFormationRCT, Shen & Tamkin, arXiv:2601.20245]"]
   **limitation_type**: "generalizability"
2. **limitation_text** [GROUNDED:web-read]: "[CognitiveDebt] is a preprint, not peer-reviewed,
   uses only one LLM (ChatGPT), and studies essay writing, not coding — it corroborates the
   *direction* of the skill/comprehension-erosion concern but cannot be used as coding-domain
   evidence, and its own limitations note results 'can't be generalized to other models.'"
   **affects_works**: ["[CognitiveDebt, Kosmyna et al., arXiv:2506.08872]"]
   **limitation_type**: "generalizability"
3. **limitation_text** [GROUNDED:web-read]: "[ScaffoldStaysOn]'s AI-prompt signature is derived
   from aggregate, cross-cohort platform submission data — it is a strong existence proof that
   AI-usage-style signatures are observable in naturalistic behavioral data, but it was never
   built or evaluated as a real-time, individual-session classifier, and it never tests an
   intervention; it only observes that gated environments (which exclude AI entirely) happen to
   screen for better practice, not that a live nudge changes an individual's trajectory."
   **affects_works**: ["[ScaffoldStaysOn, Yao, arXiv:2606.06253]"]
   **limitation_type**: "generalizability"
4. **limitation_text** [GROUNDED:web-read]: "[ProductivityParadox] is purely theoretical/
  simulated — it offers no empirical validation that real learners' interaction patterns actually
  follow the polarization dynamics it models, and it proposes no detection or intervention
  mechanism at all."
   **affects_works**: ["[ProductivityParadox, Aouad, Lykouris & Zhong, arXiv:2605.11350]"]
   **limitation_type**: "other"
5. **limitation_text** [HYPOTHESIS, since full text unread]: "[RelianceGaze] measures reliance
   quality in a single-shot *decision-making* task (does the user correctly override or accept an
   AI suggestion), not a *skill-formation* task with a delayed comprehension outcome, and its
   behavioral proxy (eye-gaze) requires eye-tracking hardware, which is a much higher deployment
   bar than the purely text/query-log-based features this topic's classifier would need. Whether
   a text-only proxy can match the eye-gaze proxy's demonstrated signal quality is untested by
   this paper and is itself a risk this topic inherits."
   **affects_works**: ["[RelianceGaze, Cao & Huang, CSCW2 2022]"]
   **limitation_type**: "precision"

**grounding_check**: `true` — every limitation cites an `affects_works` entry matching an N3
`citation_key` exactly.

**Status:** PARTIAL — limitations 1-4 confirmed against fetched text; limitation 5 is this
digest's inference since Cao & Huang's full text was not read.
**absence_comment:** {"what_missing": "None of the five works states these limitations about itself in these terms; each is derived from what its method demonstrably does not cover relative to H1.1's core question.", "why_matters": "Limitation 5 in particular should be re-verified once Cao & Huang's full text is actually read.", "implication": "Treat limitations 1-4 as reliable; re-check limitation 5 before relying on it."}

---

## N5 Challenges

**challenges:**
- **C1** [HYPOTHESIS, the central and hardest challenge]: "Real-time classification from a
  *partial* session is strictly harder than [SkillFormationRCT]'s own post-hoc labeling from a
  *complete* session — a learner who ends up in a comprehension-seeking pattern may still start
  with a code-delegation-looking query or two, and a classifier that fires too early on
  insufficient evidence risks a high false-positive rate (nudging learners who would have
  self-corrected anyway), while one that waits for high confidence may fire too late to matter.
  This precision/timing tradeoff is not addressed by any of the five grounded works, since none
  of them attempt real-time classification at all."
- **C2** [HYPOTHESIS, derived from the intervention-design-space input]: "It is not obvious *any*
  lightweight intervention actually works, or that the same intervention works for all three
  eroding patterns — a learner in 'iterative AI debugging' (asking AI to verify/fix code without
  seeking to understand why) may need a different nudge than one in 'progressive AI reliance'
  (gradually escalating delegation). A single fixed intervention risks null results that
  conflate 'interventions don't help' with 'this specific intervention doesn't help.'"
- **C3** [HYPOTHESIS, from the Hawthorne/reactivity risk inherent to any live-nudge design]: "An
  intervention that visibly interrupts a learner's flow (e.g., withholding runnable code) could
  produce a quiz-score improvement through irritation-driven increased effort/attention rather
  than through the intended comprehension-building mechanism — the study needs a way to
  distinguish 'the nudge built understanding' from 'the nudge annoyed the learner into trying
  harder,' which have different implications for real deployment."
- **C4** [HYPOTHESIS, from C1 grounded in [RelianceGaze]'s eye-gaze precedent]: "Whether
  text/query-log-only features (no eye-tracking, no model-internal access) carry enough signal
  to match the real-time detection quality [RelianceGaze] demonstrated with eye-gaze in a
  decision-making task is untested — this topic's entire technical bet depends on a proxy
  (query behavior) that has not been validated for this specific purpose (skill-formation-pattern
  detection) even though a related proxy (gaze) has been validated for a related purpose
  (reliance detection)."
- **C5** [HYPOTHESIS, generalizability boundary]: "Any result is specific to the single
  task/library/population [SkillFormationRCT] used (Trio, junior-to-mid Python developers) unless
  deliberately replicated across a second library/task — a real risk given [SkillFormationRCT]'s
  own admission that its setup differs from (and likely understates) effects in real agentic
  coding products."

**conflation_check**: `true` — each challenge targets a distinct obstacle (real-time detection
precision/timing, intervention-design uncertainty, reactivity confound, proxy-validity gap,
task/population generalizability).

**Status:** PARTIAL — inferred from the seed and the five grounded works' explicit gaps.
**absence_comment:** {"what_missing": "No Challenges section exists in a real paper; these are this digest's decomposition.", "why_matters": "C1 and C2 together mean the topic could produce an uninformative null result even if the underlying phenomenon is real, simply from classifier or intervention-design weakness — this is the central execution risk.", "implication": "The pilot design in N6 treats C1 as a hard gate: classifier validation against hindsight labels must clear a minimum bar before any intervention arm is run."}

---

## N6 Methodology

**overview** [HYPOTHESIS]: "Extend [SkillFormationRCT]'s two-arm design (Trio-library task, same
quiz instrument) with a third arm. Before running any human subjects in the third arm, first
validate a real-time interaction-pattern classifier offline against session transcripts labeled
by the base paper's own six-pattern taxonomy (obtained either by replicating a data-collection
pass matching the base paper's method, or, if the base paper's own transcripts are shared as an
artifact, by using those directly) — this offline validation is a hard gate (see Feasibility)
before any live intervention is attempted with real participants."

**Staged plan.** *Pilot stage:* (a) Classifier validation: collect or reuse a set of AI-assisted
sessions with known session-end pattern labels (from a fresh small-scale replication of
[SkillFormationRCT]'s AI-assist arm, hand-coded post-hoc the same way the base paper did); train
a real-time classifier on session-prefix features only (simulating "as if observed live") and
measure precision/recall against the hindsight labels at multiple prefix lengths (after 1, 3, 5,
10 queries). Decision gate: proceed only if the classifier reaches a pre-specified minimum
precision (e.g., ≥70%) for flagging an eroding pattern within the first half of a typical
session — otherwise the real-time premise is not yet viable and the topic must either improve
the classifier or narrow its scope (e.g., detect only the most extreme pattern, "AI delegation,"
which the base paper's own taxonomy suggests is the most behaviorally distinct). *Live pilot:*
if the gate clears, run the three-arm study (hand-coding / AI-assist-only / classify-and-intervene)
with ~60-90 new participants (comparable scale to the base paper), using a single fixed
intervention design chosen from the M4 design space based on which pattern the classifier most
often flags in the offline validation data. *Scale-up:* if the pilot shows a directional effect,
test multiple interventions matched to different flagged patterns (addressing C2), and add a
second task/library to test generalizability (addressing C5).

**key_components:**
- **M1** — name="Real-time interaction-pattern classifier"; text="Operates on session-prefix
  features only: query type (code-request vs. explanation-request vs. hybrid), whether a
  follow-up question follows a code delivery, time-to-next-query, and running counts of each
  query type — deliberately restricted to features observable without model-internal access,
  matching what an interaction pattern actually is in the base paper's own qualitative coding."
  [HYPOTHESIS]
- **M2** — name="Hindsight-label validation harness"; text="A held-out set of complete sessions
  labeled by the base paper's own six-pattern scheme (via replication of their qualitative
  coding protocol), used to score M1's real-time predictions at multiple truncation points
  against the eventual true label — directly operationalizing C1's precision/timing tradeoff as a
  measured precision-at-prefix-length curve rather than a single number." [HYPOTHESIS]
- **M3** — name="Detection-lag instrumentation"; text="For every session in the live arm, records
  the query index at which M1 first flags an eroding pattern (if ever), so that C1's
  timing question — did the flag come early enough to matter — is a measured quantity, not an
  assumption." [HYPOTHESIS]
- **M4** — name="Just-in-time intervention design space"; text="A small library of candidate
  nudges (append a comprehension-check question; temporarily deliver a partial rather than
  complete code answer; surface an explicit 'want an explanation too?' prompt), explicitly
  designed as a *space* to search rather than a single fixed choice, directly answering C2's
  concern that a single intervention choice risks an uninformative null." [HYPOTHESIS]
- **M5** — name="Reactivity-control instrumentation"; text="A no-content placebo-nudge condition
  (a visually similar but content-free interruption) in the scale-up stage, letting the study
  separate 'the nudge's content built understanding' from 'any interruption increases effort',
  directly addressing C3." [HYPOTHESIS]
- **M6** — name="Cross-domain generalizability check"; text="A second task/library replication
  in the scale-up stage (following [SkillFormationRCT]'s own explicitly-flagged 'effects beyond
  coding' open question, though staying within coding to keep the quiz instrument comparable),
  addressing C5." [HYPOTHESIS]

**challenge_arguments:**
- {challenge_id: "C1", argument_text: "M2's precision-at-prefix-length validation, gated before
  any live participant is run, turns the timing/precision tradeoff into a measured curve and a
  hard go/no-go decision rather than an untested assumption.", mechanism_components: ["M1","M2"],
  source: HYPOTHESIS}
- {challenge_id: "C2", argument_text: "M4's explicit design space (rather than one fixed
  intervention), tested pattern-by-pattern in the scale-up stage, prevents a single bad
  intervention choice from masking a real underlying effect.", mechanism_components: ["M4"],
  source: HYPOTHESIS}
- {challenge_id: "C3", argument_text: "M5's placebo-nudge control isolates content-driven
  comprehension gains from generic interruption/reactivity effects.",
  mechanism_components: ["M5"], source: HYPOTHESIS}
- {challenge_id: "C4", argument_text: "M2's validation IS the direct test of whether
  text/query-log features carry adequate signal — a low precision result would directly falsify
  the proxy-validity assumption C4 raises, rather than leaving it untested.",
  mechanism_components: ["M1","M2"], source: HYPOTHESIS}
- {challenge_id: "C5", argument_text: "M6's second-task replication in the scale-up stage
  directly tests whether results generalize beyond the single library/population the pilot
  uses.", mechanism_components: ["M6"], source: HYPOTHESIS}

**unaddressed_challenges**: [] — every challenge has at least a partial, staged answer; C2's full
resolution (which intervention works for which pattern) is explicitly deferred to the scale-up
stage rather than left unaddressed.

**Feasibility** [HYPOTHESIS — order-of-magnitude estimates]:
- *Classifier validation (hard gate):* requires a labeled session dataset comparable in scale to
  [SkillFormationRCT]'s own (order of 25-30 AI-assisted sessions minimum for a first pass) — the
  single biggest feasibility question is whether the base paper's own session transcripts can be
  obtained/reused as a research artifact (check this before collecting new data) rather than
  requiring a full fresh data-collection pass; ~2-3 person-weeks either way.
- *Live pilot:* ~60-90 participants across 3 arms, comparable recruiting cost/difficulty to the
  base paper's own 52-participant study (roughly 1.5-2x); ~3-4 person-weeks including the
  intervention-design build.
- *Scale-up:* multiple interventions × a second task/library roughly doubles the live pilot's
  scope; ~4-6 additional person-weeks.
- *Single biggest feasibility risk:* the classifier-validation gate (M2) failing outright — if
  text/query-log features cannot predict the eventual pattern label better than a trivial
  baseline (e.g., "always predict the most common pattern") within the first half of a session,
  the entire real-time-intervention premise is not viable as scoped, and the topic would need to
  either narrow to detecting only the single most distinctive pattern or pivot to a
  longer-observation-window design that abandons the "just-in-time" framing.

**Status:** PARTIAL — entirely inferred; no methodology exists to extract.
**absence_comment:** {"what_missing": "No implemented method exists.", "why_matters": "This topic's core technical bet (M1/M2) is genuinely unvalidated by any of the five grounded works — none of them attempted real-time classification.", "implication": "Treat the M2 validation gate as the first and most important thing to build, before any human-subjects design work."}

---

## N7 Contributions

- **CO1** [HYPOTHESIS]: "A real-time interaction-pattern classifier and a hindsight-label
  validation methodology extending [SkillFormationRCT]'s taxonomy from post-hoc coding to
  live, session-prefix prediction (M1+M2), including an honest precision-at-prefix-length
  characterization." contribution_type: `dataset`; is_testable: true; has_rq: true
- **CO2** [HYPOTHESIS]: "A three-arm causal extension of a published skill-formation RCT, testing
  whether just-in-time intervention on a detected eroding pattern measurably improves the
  downstream quiz outcome, with results directly comparable to the base paper's own published
  50%/67% numbers." contribution_type: `empirical_finding`; is_testable: true; has_rq: true
- **CO3** [HYPOTHESIS]: "A characterization of which intervention designs help (if any) for which
  detected pattern, and whether any benefit is content-driven or merely reactivity-driven (M4+M5)."
  contribution_type: `empirical_finding`; is_testable: true; has_rq: true
- **CO4** [HYPOTHESIS]: "A methodological argument, conditional on CO1-CO3's direction, about
  whether AI-assistance products should incorporate real-time skill-erosion detection as a
  design feature, versus relying on post-hoc/longitudinal measurement as the base literature
  currently does exclusively." contribution_type: `conceptual_framework`; is_testable: false;
  has_rq: false

**Status:** PARTIAL — hypothesized from the method sketch.
**absence_comment:** {"what_missing": "No stated contributions exist.", "why_matters": "If M2's validation gate fails, CO2-CO4 may need to be dropped entirely and the paper narrowed to CO1's negative/limited result alone — a real and acceptable possible outcome.", "implication": "Treat CO1 as the load-bearing contribution; CO2-CO4 are conditional on it clearing the gate."}

---

## N8 Research Questions

**research_questions:**
- **RQ1** [GIVEN] (the seed's core question): "Can a real-time interaction-pattern classifier
  detect a learner drifting into a skill-eroding AI-usage pattern early enough within a session
  to enable a just-in-time intervention, before the pattern is fully established?"
  (id: "RQ1"; rq_source: "explicit"; addresses_challenges: ["C1","C4"]; evaluates_mechanisms:
  ["M1","M2","M3"]; tests_contributions: ["CO1"]; answered_by_experiment: "M2's
  precision-at-prefix-length validation against hindsight-labeled sessions — this is the hard
  gate the rest of the topic depends on.")
- **RQ2** [GIVEN] (the seed's second half): "Does a just-in-time intervention triggered by that
  detection causally improve the downstream skill-formation outcome (quiz score) relative to
  unintervened AI assistance, and how does that compare to the base paper's own published
  hand-coding-vs-AI-assist gap?"
  (rq_source: "explicit"; addresses_challenges: ["C2","C3"]; evaluates_mechanisms: ["M3","M4",
  "M5"]; tests_contributions: ["CO2","CO3"]; answered_by_experiment: "three-arm live pilot,
  primary endpoint = quiz score, classify-and-intervene arm vs. AI-assist-only arm, directly
  plotted against the base paper's own 50%/67% two-arm numbers.")
- **RQ_INF_1** [HYPOTHESIS, inferred from C5 and the base paper's own stated open question about
  effects "beyond coding"]: "Does the detection-and-intervention effect (if any) replicate across
  a second task/library, or is it specific to the Trio/async-programming setting the base paper
  used?"
  (rq_source: "inferred"; addresses_challenges: ["C5"]; evaluates_mechanisms: ["M6"];
  tests_contributions: ["CO2"]; answered_by_experiment: "scale-up-stage second-task replication,
  same design, same quiz-comparability logic.")

**datasets** [HYPOTHESIS]: {names: ["A labeled session-transcript set for classifier validation
(M2) — either a reuse of [SkillFormationRCT]'s own materials if obtainable as a research
artifact, or a fresh small-scale replication of their AI-assist condition", "A new three-arm live
pilot dataset (hand-coding / AI-assist-only / classify-and-intervene), same task/quiz instrument
as [SkillFormationRCT]"], source: HYPOTHESIS, location: null}
**baselines** [HYPOTHESIS]: {names: ["Hand-coding arm (replicating [SkillFormationRCT]'s own
control, for direct comparability)", "AI-assist-only arm (replicating their treatment arm)",
"Trivial classifier baseline (always predict the most common of the six patterns) for M2's
precision comparison", "Placebo-nudge arm (M5, scale-up stage only)"], source: HYPOTHESIS,
location: null}
**metrics** [HYPOTHESIS]: {names: ["Classifier precision/recall at prefix lengths {1,3,5,10
queries} against hindsight labels", "Quiz score, directly comparable to the base paper's own
50%/67% figures", "Detection lag = query index of first eroding-pattern flag", "Content-vs-
reactivity effect decomposition (scale-up stage, via M5)"], source: HYPOTHESIS, location: null}

**Analysis plan** [HYPOTHESIS — pre-registerable]:
- *Classifier gate:* pre-specify minimum precision (e.g., ≥70%) at the ≤half-session prefix
  length as the go/no-go criterion for proceeding to the live pilot; report the full
  precision-at-prefix-length curve regardless of outcome.
- *Primary live-pilot test:* quiz score, classify-and-intervene vs. AI-assist-only, same test
  family as the base paper (t-test/Cohen's d) for direct numeric comparability; secondary
  contrast against the hand-coding arm to confirm the base effect replicates in this topic's own
  data collection before trusting the three-arm comparison.
- *Detection-lag reporting:* descriptive, not hypothesis-tested alone, but cross-tabulated
  against quiz-score outcome to check whether earlier detection correlates with larger
  intervention benefit (a secondary, exploratory analysis).
- *Reactivity decomposition (scale-up):* quiz score, content-nudge vs. placebo-nudge vs.
  no-nudge, three-way comparison.

**Status:** PARTIAL — RQ1/RQ2 given; RQ_INF_1, datasets, baselines, metrics, and analysis plan
inferred.
**absence_comment:** {"what_missing": "No real RQ list, dataset, or analysis plan exists in a paper.", "why_matters": "The classifier-gate threshold (≥70%) is an arbitrary placeholder, not derived from any base-rate estimate.", "implication": "Re-derive the gate threshold from the actual precision achievable on a small initial labeled set before committing to it as a hard pre-registered criterion."}

---

## N9 Results

> **CRITICAL — no experiment has been run. Nothing below is a real result.**

- **rq_id**: "RQ1"
  **result_text** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]: "Predicted direction: the
  classifier can distinguish the most behaviorally distinctive pattern ('AI delegation' — pure
  code-request queries with no follow-up) with reasonably high precision fairly early (within the
  first 3-5 queries), but struggles to distinguish the subtler patterns (e.g., 'iterative AI
  debugging' vs. 'hybrid code-explanation') until later in the session — i.e., RQ1 is predicted
  to hold only partially, for a subset of patterns."
  **result_type**: `quantitative` (predicted); **evidence_strength**: `missing`;
  **rq_answered**: `false`
  **FALSIFICATION CONDITION**: "Refuted if precision at any prefix length is statistically
  indistinguishable from the trivial most-common-pattern baseline for all six patterns."

- **rq_id**: "RQ2"
  **result_text** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]: "Predicted direction: the
  classify-and-intervene arm scores measurably higher than the AI-assist-only arm, but likely
  does not fully close the gap to the hand-coding arm's 67% — a partial mitigation, not a full
  fix, consistent with the base paper's framing that AI-enhanced productivity is 'not a shortcut
  to competence.'"
  **result_type**: `quantitative` (predicted); **evidence_strength**: `missing`;
  **rq_answered**: `false`
  **FALSIFICATION CONDITION**: "Refuted if the classify-and-intervene arm's quiz score is
  statistically indistinguishable from the AI-assist-only arm's, or if it is not statistically
  distinguishable from the hand-coding arm despite RQ1 only partially succeeding (which would be
  a suspiciously convenient result worth extra scrutiny)."

- **rq_id**: "RQ_INF_1"
  **result_text** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]: "Predicted direction: a smaller
  but same-direction effect on a second task/library, given the base paper's own framing that its
  effect should generalize qualitatively across unfamiliar-library learning tasks."
  **result_type**: `quantitative` (predicted); **evidence_strength**: `missing`;
  **rq_answered**: `false`
  **FALSIFICATION CONDITION**: "Refuted if the second-task replication shows no effect or an
  effect in the opposite direction."

**Status:** NOT_FOUND (by construction).
**absence_comment:** {"what_missing": "No real results exist.", "why_matters": "Presenting a direction as a finding would fabricate empirical support.", "implication": "Re-populate only after the classifier-gate and live pilot actually run."}

---

## N10 Threats / Self-Limitations

**threats:**
- **t1** [HYPOTHESIS]: category=`construct`; description: "The entire topic depends on a proxy
  (text/query-log features) whose validity for this specific purpose is unestablished — the
  closest precedent (Cao & Huang's eye-gaze proxy) used a different signal and a different
  outcome (decision accuracy, not skill formation)." mitigation: "M2's hard validation gate,
  reported honestly even if it fails."
- **t2** [HYPOTHESIS]: category=`internal`; description: "Any live-nudge intervention risks a
  reactivity confound (C3) — an observed benefit could be non-specific rather than
  comprehension-building." mitigation: "M5's placebo-nudge control in the scale-up stage; the
  pilot stage alone cannot rule this out and should not claim a mechanism, only an effect."
- **t3** [HYPOTHESIS]: category=`external`; description: "Findings are specific to the
  Trio-library/junior-developer population until M6's replication runs, and the base paper's own
  admission that real agentic coding products likely show larger effects means this topic's
  numbers may understate real-world stakes even if internally valid." mitigation: "State the
  scope limit explicitly; treat results as a lower bound."
- **t4** [HYPOTHESIS]: category=`conclusion`; description: "A three-arm design with a
  classifier-gate gives multiple opportunities for false-positive conclusions if not
  pre-registered." mitigation: "Pre-register the M2 gate threshold and the primary RQ2 test
  before data collection; report the gate's actual pass/fail regardless of how convenient a
  different threshold might look after the fact."
- **t5** [HYPOTHESIS]: category=`reproducibility`; description: "If the base paper's own session
  transcripts cannot be obtained/reused, M2's validation set is a fresh, smaller-scale collection
  that may not match the base paper's population/task fidelity exactly." mitigation: "Report
  recruitment/task-fidelity details transparently; flag any deviation from the base paper's
  protocol explicitly rather than assuming equivalence."

**Status:** PARTIAL — anticipated, not author-acknowledged (no author exists yet).
**absence_comment:** {"what_missing": "No written Limitations section exists.", "why_matters": "N10 necessarily holds this digest's forecasts.", "implication": "Replace with the real paper's own limitations once written."}

---

## N11 Artifacts

**artifacts**: []
**has_code**: `false` [PLACEHOLDER]
**has_data**: `false` [PLACEHOLDER]
**has_model**: `false` [PLACEHOLDER]

**Status:** NOT_FOUND.
**absence_comment:** {"what_missing": "No code, dataset, or model has been released.", "why_matters": "A reader should not assume any artifact (classifier, intervention library, labeled session set) exists.", "implication": "The planned releases are the M1 classifier, the M2 validation harness/labeled set, and the M4 intervention-design library, once built."}

---

## N12 Contribution Type

**value**: `empirical` [HYPOTHESIS]

**rationale** [HYPOTHESIS]: "RQ1 and RQ2 are measurement/intervention-evaluation questions —
whether a mechanism (real-time classification) works, and whether an intervention built on it
causally changes an outcome (quiz score) — the hypothesized outputs in N9 are
precision/recall curves and quiz-score deltas, i.e., what an empirical study reports. M1's
classifier and M4's intervention library are built as instruments for this measurement, not as a
leaderboard-style benchmark product. If the classifier or intervention library becomes broadly
reused as a standalone tool independent of this study's causal claim, reclassify to `tool`/
`benchmark`."

**Status:** FOUND. No absence_comment required.

---

## Claims

1. **[HYPOTHESIS]** "A real-time classifier operating only on session-observable query features
   can detect at least the most behaviorally distinctive skill-eroding AI-interaction pattern
   (full code delegation) with useful precision within the first half of a typical learning
   session." — RQ1's core, partial-success-expected prediction.
2. **[HYPOTHESIS]** "A just-in-time intervention triggered by that detection produces a
   measurable, but likely partial (not fully baseline-closing), improvement in downstream
   skill-formation outcome relative to unintervened AI assistance." — RQ2's core prediction.
3. **[HYPOTHESIS]** "Any observed intervention benefit is at least partly content-specific
   (comprehension-building), not purely a reactivity/interruption artifact." — the scale-up
   stage's C3-directed prediction, the hardest of the three to establish cleanly.
4. **[PLACEHOLDER]** "The actual classifier precision, intervention effect size, and
   content-vs-reactivity decomposition are unknown until the classifier-validation gate and live
   pilot are run — no number here should be treated as evidence." — flags N9 as entirely
   speculative.
5. **[CONFIRMED, 2026-08-13]** "The originating industry-signal-scan document's claim of 'three
   independent studies' triangulating AI-induced skill atrophy was itself a research artifact
   worth catching: two of the three descriptions (from two different YouTube channels) turned out
   to be secondhand retellings of the *same* paper (Shen & Tamkin, `arXiv:2601.20245`). The real
   count is two independent studies (Shen & Tamkin's coding RCT; Kosmyna et al.'s EEG essay-
   writing study), not three — corrected here and in `industry_signal_scan_2026-08.md`. This does
   not weaken the topic (two independent, differently-instrumented studies converging is still
   real corroboration, and three more directly relevant papers — Yao; Aouad, Lykouris & Zhong;
   Cao & Huang — were found and read in the course of grounding this digest, strengthening the
   literature base beyond what the industry scan alone offered) — but it is the exact kind of
   error the primary-source-verification step exists to catch before it propagates into a real
   paper's related-work section."