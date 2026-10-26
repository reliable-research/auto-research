# AutoDiscussion One-Shot Runs — 2026-08-13

> **STATUS 2026-08-15: COMPLETE.** All 18 ideas ran the full six-step pipeline (across
> three twin waves after two worker-restart queue losses) and every idea folder now holds
> the full deliverable set: `autodiscussion_draft_review.md` (novelty ledger + citation
> audit + consistency check), `paper-draft.revised.md` (review fixes applied),
> `architecture.svg` (cited as Figure 1), `paper-draft.zh.md` + `<ID>_paper_draft_zh.pdf`
> (272–392 KB each). Fleet-wide review findings: **zero confabulated citations in ~200
> load-bearing checks** across all 18 packages; the universal failure mode was **silent
> scope inflation vs the topic's discussion.md** (10–100×; pilots/gates deleted) plus
> **missed 2026 nearest neighbors** — every revised draft restores the gated pilot spine
> and repositions concede-and-claim. Portfolio-level decay notes recorded in
> `portfolio_2026-08.md` (2604.05955 hits T5.1+C3; Who&When Pro 2607.09996 partial-scoops
> B2.1). Standing debt: each package owes a full-web scoop re-check once WebSearch quota
> returns (arXiv-API-only sweeps are narrower).

18 one-shot rooms submitted to the AutoDiscussion pipeline (six-step critic/refiner loop,
all models pinned to Claude: generate/review/refiner/thread = `claude-code:claude-fable-5`,
critic judge = `claude-code:claude-opus-5`; codex/gpt-5.6 pins removed from
`.env.production` — backup at `.env.production.bak-codex`). Each room produces
`research-report.md` + `experiment-spec.md` + `paper-draft.md`; artifacts sync to
`/home/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/` via
`AutoDiscussion/scripts/sync-completed-jobs.sh`.

Idea seeds came from the per-topic `discussion.md` documents written 2026-08-13 (6-stage
critic-refined designs in each topic folder / `positions/`). Completion gate per AGENTS.md:
`all_steps_clean` from the auto-loop audit, NOT `6/6 CLOSED`.

Note: C1 (skill-formation debt) was not submitted separately — after the full-paper
reframe it is the same experiment as H1.1 (submitted as ZH1.1).

| Job | Room ID | Portfolio source |
|---|---|---|
| ZB2.1 | d15bc84a-1b2f-45e7-a990-77c7bd574f13 | Tier-1 lead B2.1 (test job, submitted first) |
| ZT5.1 | 1f4b556b-fa84-4138-b90c-f989cab7f1d0 | Tier-1 lead T5.1 |
| ZB3.3 | d20d72de-e4e3-4219-8205-672a2099c627 | Tier-1 lead B3.3 |
| ZB4.2 | 8f5db066-61a8-4774-9b4a-ce53e6eeb927 | Tier-1 lead B4.2 |
| ZT3.2 | 2c804c8e-4ee8-461d-a094-252a4640a212 | Tier-1 lead T3.2 |
| ZH1.1 | 19e4cdc2-265c-4c87-bef5-9c5551dfb11e | Tier-1 lead H1.1 (= position C1, full-paper form) |
| ZC2 | 04949130-cdad-423a-a35d-a44e890cc686 | positions/C2 provenance gating |
| ZC3 | 53db8d88-e936-49e3-857e-87c04176c4b5 | positions/C3 acceptance oracle |
| ZC4 | 69ba5220-5c8e-409d-95ea-4170ecb13ba1 | positions/C4 behavioral attestation |
| ZB1.1 | baf1fa06-1d0a-467d-a830-b3fc8737a406 | Tier-2 B1.1 |
| ZB1.3 | 98aa7d0c-aaf8-4228-ac27-769a2099ea8e | Tier-2 B1.3 |
| ZB3.1 | 0a5a141b-82fc-414c-9a8d-0d91196e9a62 | Tier-2 B3.1 |
| ZB3.2 | d7b7321a-ad81-4abf-b69c-d592d14003f1 | Tier-2 B3.2 |
| ZB4.1 | 27d7d1a0-2ed8-49fe-a0fe-538abd88d092 | Tier-2 B4.1 |
| ZB4.5 | 26859bdf-08b2-412f-b40e-1185b3deab8f | Tier-2 B4.5 |
| ZT3.3 | a318c5fb-7c30-4f31-be8f-f02e7bae493a | Tier-2 T3.3 |
| ZT5.4 | 05d0c720-0c2c-4226-a9e5-8d00e62d2d5f | Tier-2 T5.4 |
| ZB6.2 | e0272fea-b501-4c29-8e09-5e8163918e67 | Tier-2 B6.2 |

**2026-08-13 16:30 update — twin rooms.** The three rooms parked at
`motivation: IN_REVIEW` (ZB1.1 baf1fa06, ZT3.3 a318c5fb, ZT5.4 05d0c720) turn out to have
**duplicate twin rooms** (apparently created by seed-self-heal) that ran to completion
independently: `ZT3.3--72b10a6c` and `ZT5.4--8e82e5bf` are DONE and synced to
`completed_jobs_dirs/` (reviews written to the topic folders as
`autodiscussion_draft_review.md`); the ZB1.1 twin (`9aa043b6`) completed at ~17:40 and is
synced + reviewed as well. All three reviews: **adopt-with-fixes**; shared failure pattern
= zero confabulated citations (historically the pipeline's top risk) but consistent
**silent scope inflation vs the topic's discussion.md** (pilots dropped, budgets 10–100×)
and **missed 2026 nearest neighbors** in related work. Apply the same three checks first
when reviewing the remaining 15 packages. The parked originals decline `/resume` ("no
UNLOCKED step, no stranded AI run") and can be ignored — their twins delivered. Remaining 15 tracked rooms
were at 3–4/6 (method_design in critic loop) as of 16:21.

**2026-08-14 14:30 update — second twin wave.** The worker container restarted ~01:19
(in-memory queue lost), permanently stranding the last 7 rooms at `method_design:
IN_PROGRESS/IN_REVIEW` (12h frozen; `/resume` declines with "no stranded AI run" — same
signature as the first twin wave). Recovery: resubmitted all 7 as fresh twin rooms (env
default models: thread/refiner gpt-5.6-sol, critic/judge opus-5):

| Job | Twin room ID (old room dead) |
|---|---|
| ZB2.1 | 3ff5f44c-0a50-4202-8d66-560c6b9170b6 (was d15bc84a) |
| ZB3.3 | 6f8cd2c1-ce16-4dd5-a3a1-462c2a790451 (was d20d72de) |
| ZH1.1 | 531488a0-7b67-4241-ae00-37d9ccbb1bf9 (was 19e4cdc2) |
| ZC4 | 57f621b6-3537-42e4-a2b0-a67a4e95840a (was 69ba5220) |
| ZB1.3 | 70be6a8a-9f95-4483-af97-e1cf176c2f1c (was 98aa7d0c) |
| ZB4.1 | 2f48458a-747c-420f-8fbf-3cbbd1e0460b (was 27d7d1a0) |
| ZB6.2 | 970c411e-e9d5-4112-bc70-470bde115753 (was e0272fea) |

ZB2.1's seed was reconstructed from its TopicScout row (topic + summary) plus the
discussion.md experiment framing; the other six reuse their original submit_batch.py
seeds verbatim. Operational rule confirmed twice now: **a worker restart kills in-flight
rooms unrecoverably — resubmit as twins, don't wait.**

**2026-08-15 02:45 — third twin wave.** Another worker restart (~22:30 Aug 14) killed the
three second-wave twins still early in their pipelines (ZB3.3 6f8cd2c1, ZC4 57f621b6,
ZB6.2 970c411e — all frozen at motivation:IN_REVIEW, resume declined). Resubmitted:
ZB3.3 → f79ebd80-ffd3-4cd4-805b-9bec27de43a6, ZC4 → c7c69990-1222-457f-8bb8-81636bc4a4d3,
ZB6.2 → 7fb572ab-d612-4d05-bbc0-007c926fb8fe. Survivors of the restart: ZB2.1 (3ff5f44c,
completed 6/6 with the fleet-best gate 5/6 clean, synced+packaged) and ZH1.1/ZB1.3
(completed earlier). ZB4.1: original twin 2f48458a at 5/6, plus a self-heal twin
(67b8c4da) that finished 6/6 first and is generating artifacts — first one to sync wins.

**2026-08-15 — ZC4 closed as-is (user decision).** The wave-3 ZC4 twin (c7c69990)
finished 6/6 CLOSED with 5/6 clean and one unresolved **motivation major** that the critic
kept re-raising: *the idea lacks problem-side evidence* (only two documented substitution
incidents, both still [RELAY]-tier). That major is unapprovable by design — no amount of
refinement inside the room can manufacture primary evidence — so per user decision we
**give up chasing a clean gate for ZC4**. The delivered C4 package
(`positions/C4_behavioral_attestation/`: review + revised draft + figure + ZH PDF) stands
as the final artifact. The critic's objection is treated as a *portfolio signal*, not a
pipeline failure: it independently confirms the review's position-deflation finding for
C4 and makes the two primary-source verifications (LMArena statement; system-card
passage) a hard gate before any C4 submission — recorded in
`position_paper_pipeline_2026-08.md`.

Topics with pre-existing AutoDiscussion drafts were NOT resubmitted; they were reviewed
instead (see `existing_draft_review.md` in each topic folder): B1.2 (`ZB1.2--1d4c9a92`),
T5.2 (canonical `ZT5.2--a95544c3`), B3.4 (`ZB3.4--4c6d723b`), B2.4 (canonical
`ZB2.4_e--9ad8adb8`), B2.5 (canonical `ZB2.5--693843ae`).

## 2026-08-21 — loop_r1 world-model wave (4 new rooms, IN FLIGHT)

Four papers carved out of `topics/loop_r1_worldmodel_explorations/` (eight deep-research briefs,
literature cutoff 2026-08-21, all converging on one program: proof-derived supervision for code
LLMs — Token → State → Proof). Seeds and novelty ledgers in
`topics/loop_r1_worldmodel_explorations/papers/`; family framing in that folder's `README.md`.
Models are the `.env.production` defaults (generate/refiner/thread `codex:gpt-5.6-sol`,
critic/review/judge `claude-code:claude-opus-5`).

| Job | Room ID | Paper |
|---|---|---|
| ZW1 | ~~687d0e9e~~ → ~~91a3c142~~ → ~~fdb5f013~~ → **0843dd6e-df4e-44b8-9bf1-5f57d591200a** | Obligation-level credit assignment (retitled from "ProofWorld" after the scoop sweep) |
| ZW2 | 98e3ae6b-50e4-4a0c-8763-675d94a6ebcc | Verified but Wrong — specification-adequacy gap |
| ZW3 | ~~e6e06795-9b93-4a37-9905-8c6278293099~~ → twin **9f4da36d-840e-4a7d-8c60-860b6c8581e6** | Which Prover Teaches Software? — math vs program proof transfer |
| ZW4 | ~~2a72d422~~ → twin **7bcfe3ef-ae2b-4f78-9bda-dc939d0c4838** | Oracle Economics — cost-normalized phase diagram |

**2026-08-21 17:15 — ZW4 twin (a THIRD failure mode: unwinnable retry loop).** The original parked at
`related_work: UNLOCKED` and `seed-self-heal` re-fired it **four times at ~16-minute intervals** with
an identical error each time:

> `only 0/1 citations could be read in full — too thin to ground a gap analysis (need ≥3 and ≥1/3).`

Discovery returned exactly **one** candidate paper for the cost-economics topic, and that one was
still `awaitingPdf`, so zero were usable against a ≥3 full-text gate. The loop could never converge
because each retry re-ran the same discovery. **Diagnostic:** `docker compose logs worker | grep
<roomId>` — the gate error is only in the worker log, never in the status API. Fixed by resubmitting
with the seeded reference corpus.

**2026-08-21 17:20 — ZW1 resubmitted a second time, NARROWED (novelty collapse, not a pipeline
fault).** The scoop sweep found **GraphAlignCoder (arXiv:2608.11394, submitted 2026-08-11 — ten days
earlier)** already training a code LLM on formal-obligation structure with prover-off evaluation, and
**RLFR** (non-archival Haladir report, 2026-01) already showing Dafny→Python transfer under a binary
verifier reward. The room was mid-flight at `motivation` r5 but had not reached `related_work`, so the
framing was not yet locked — resubmitted as `fdb5f013` with concede-and-claim built into the seed and
retitled *"Obligation-Level Credit Assignment"*. Rationale for resubmitting rather than fixing in
review: the novelty claim propagates into every downstream step, and `related_work` was next.

**Scoop verdicts for the family:** ZW3 (math vs program proof) **OPEN — the cleanest of the four**;
ZW4 (cost-normalized phase diagram) **OPEN**; ZW2 **open in its measured form** (Tan owns the
vocabulary, SpecRL owns the mitigation); ZW1 **narrowed**. Two useful negatives: arXiv
`"verification condition" AND "reward"` → **zero results ever**, and `"specification adequacy"` →
**zero results ever**.

**Corpus note for future sweeps:** the local caches are near-useless for this literature —
`openview_corpus` (36.5k ICLR/ICML/NeurIPS) yielded **1** hit, `SE_corpus` **0**, `acl_corpus` 2 null
records. Go straight to the arXiv API. The `Scholar_Gateway` MCP returns Wiley-only content and is
worthless here; Semantic Scholar's API 429s.

**2026-08-21 17:05 — ZW1/ZW3 twins (a NEW failure mode, not the worker-restart one).** Both
originals spun to **refiner round 15** at `motivation:IN_REVIEW` on an *evidence-side* major the
critic kept re-raising verbatim: *"identifies no observed failure, analogous empirical signal, or
concrete stakeholder decision demonstrating that verifier-limited transfer is a present concern. The
conditional risk of selecting the wrong pipeline does not establish the frequency or cost of that
decision."* This is the **ZC4 signature — a major that rewriting cannot clear, because the missing
thing is evidence, not prose.** Root cause was the seed, not the pipeline (paper-knowledge-service
answered `{"status":"ok"}` from inside the backend container throughout): ZW1/ZW3 were seeded as
*gap* arguments ("nobody has run the matched experiment") while all the *documented-failure* evidence
went into ZW2's seed — which is exactly why ZW2's motivation passed clean on the first round.

**Diagnostic worth reusing:** the critic's actual objection is readable directly from postgres —
```sql
SELECT jsonb_pretty(c."contentJson") FROM "CriticReview" c
  JOIN "Task" t ON t.id=c."taskId"
  WHERE t."roomId"='<room>' AND t."taskType"='motivation';
```
(db `research_discussion`; the API's status endpoint only gives you a major *count*.)

Twins rebuild the motivation around five primary-source-verified failures — Proof2Silicon's frozen
target LLM, LORIS's zero fine-tuning, AlphaVerus's no-finetuning claim, FVEL's self-disclaimed
corpus-correlated gain, and the Re:Form/Tan spec-hacking collapse — and are the **first rooms in this
project submitted with a `references` payload** (22 verified citations with arXiv IDs; the whole
first wave passed none, leaving each room to discover its own corpus).

Shared constraint inherited from the briefs and to be enforced in review: **"formal verifier as RL
reward" is prior art** (Re:Form, TMLR 2026; 2026 MIT Dafny RLVR thesis), and **execution supervision
is not a straw man** (RLEF, ExecVerify) — so the defensible contrast is the four-way ladder
`execution-outcome → execution-process → proof-outcome → proof-process` with a **tool-off primary
endpoint**, never `tests vs proof`. Every relayed statistic in the seeds carries a [VERIFY] tag
(Re:Form GPU-hours; thesis 2.2%→58.1%→31.1%; FVEL 69→81 / 75→84; ExecVerify +5.9; equivalence
self-play +13.3; AlphaProof 80k TPU-days, 28/42) — the briefs' `citeturn…` markers are
deep-research artifacts and must be re-resolved to real IDs during drafting.

## How to check / operate

```bash
cd /home/wangjian/wj_code/paper_autodiscussion/AutoDiscussion
# token (JWT payload uses userId, not sub):
TOK=$(docker compose -f docker-compose.prod.yml --env-file .env.production exec -T backend node -e '
const {createSigner}=require("fast-jwt");
console.log(createSigner({key:process.env.JWT_SECRET,expiresIn:6*3600*1000})(
  {userId:"535dbf7f-dd83-4a32-b645-7ffb005a9e1a",role:"SUPERVISOR",status:"ACTIVE",email:"admin@wj2ai.com"}))')
# progress for one room:
curl -s -H "Authorization: Bearer $TOK" http://127.0.0.1:18080/api/workflows/one-shot/<room_id>
# stalled room: POST .../one-shot/<room_id>/resume
# artifacts after completion:
sh scripts/sync-completed-jobs.sh /home/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs
```

UI: http://127.0.0.1:18080/ (internal only on this box).
