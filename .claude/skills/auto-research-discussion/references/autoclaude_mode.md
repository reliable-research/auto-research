# Autoclaude mode reference

The user pointed this skill at a **codebase or project folder** rather than a research idea. In autoclaude mode, Claude does the whole pipeline by itself: it reads the repo to figure out what the project is doing, then runs the six-stage discussion loop as **both** student and teacher, until they converge on a confirmed output for every stage. Final deliverables are the same three artifacts as any other run of this skill — paper draft, standalone experiment design spec, and the full discussion trace — plus the seed brief (see Final deliverables below).

This file covers three things: how to scan the repo, how to keep the self-play honest, and how the loop differs from the regular interactive flow.

## Why this mode is different from "autonomous"

Autonomous mode still requires the user to provide a seed idea. Autoclaude requires only a path. The student's "seed" is reconstructed from the repo. That reconstruction is itself a research act — what is this project actually about? — and the teacher gets to push back on it.

So autoclaude has one extra step at the front (repo scan + seed extraction), and one extra discipline throughout (anti-sycophancy in self-play). Otherwise it's the same six stages with the same rubric.

---

## Step 0: Repo scan and seed extraction

Read in this order. Stop early if you have what you need; don't try to read every file.

### Priority 1 — orienting documents (read these first, every time)

- `README.md` / `README.*` at the repo root
- Any `ARCHITECTURE.md`, `ROADMAP.md`, `DESIGN.md`, `OVERVIEW.md`, `CONTRIBUTING.md` at the root
- A top-level `docs/` or `doc/` directory — at least the index/landing page and the table of contents
- Any `paper/`, `writeup/`, `report/`, `manuscript/` directories
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` for the project's stated description and dependencies — these often have a one-line summary that's better than nothing
- `LICENSE` is irrelevant; skip it

If there's a `README.md` and it has a paragraph that explains what the project does, you have your seed candidate. Most of your time should go to refining it, not searching for more.

### Priority 2 — top-level structure

- Run a `view` on the repo root to see the directory layout. Don't recurse deeply — two levels is enough.
- Note the major top-level directories: `src/`, `frontend/`, `backend/`, `lib/`, `tests/`, etc. The shape of the directory tree tells you what kind of project it is (CLI tool, web app, ML pipeline, library, research code, …).
- If there's a `Makefile`, `justfile`, or top-level scripts directory, glance at the available commands — they describe the project's operations in user-facing language.

### Priority 3 — entry points (skim, don't deep-read)

- `main.py`, `app.py`, `index.ts`, `server.ts`, `cmd/main.go`, etc. — the *first* file someone running this project would touch.
- For a frontend, the home page / landing page often contains the most concise human-readable description of the product — sometimes one paragraph, sometimes a short features list. Either way it's usually the single best source for "what does this actually do" in plain language, better than inferring it from route names.
- For a library, the public API surface — usually `__init__.py`, `lib.rs`, or whatever exports things.

### Priority 4 — only if needed

- Tests, only if the README and entry points don't tell you what the project does. Tests describe behavior in human-readable language.
- Issues / changelog if present and Priority 1 was thin.

### What you're extracting

After scanning, write a short internal **seed brief** before doing anything else:

```
Seed brief
- One-sentence description of what the project does (from README or entry points)
- Apparent inputs to the system
- Apparent outputs of the system
- Closest research areas / vocabulary used in the docs
- What's clearly out of scope vs. in scope
- Confidence: high | medium | low (low = the docs were thin and you guessed a lot)
```

If confidence is `low`, surface this to the user before running the full loop and offer to ask them one or two clarifying questions instead of running on guesses. This is the only point in autoclaude where you should stop for input.

---

## Self-play discipline (the part that makes this work)

When both the student and the teacher are Claude, the failure mode isn't disagreement — it's premature agreement. The student capitulates to the teacher's first comment; the teacher softens because the student already conceded. The loop terminates instantly with a draft nobody really vetted. **You have to actively guard against this.**

Three rules. Apply them every round, in every stage.

### Rule 1: The student commits to evidence-grounded positions

Every claim in the student's draft must be traceable to something concrete:
- A file in the repo (cite the path)
- A specific line or block of the README/docs
- A behavior described by the code structure or tests

When the student proposes the stage 1 problem statement, they should be able to say: "The input is an audio transcript, per `frontend/app/page.tsx` line 70, and the output is a 'chapter-segmented summary,' which is the language the docs themselves use."

The teacher can attack the *interpretation* but not the *evidence*. If the teacher says "I don't think this is really the input," they have to point at evidence too — another file, a contradicting passage. **No vibes-based critiques.** This is the asymmetry that prevents collapse.

### Rule 2: The student gets one defense per round

When the teacher (critic) raises a `[major]` flag, the student is allowed exactly one round to push back if the flag misreads the repo. The pushback goes in a `defenses` field of the next draft:

```
defenses:
  - { critic_comment_idx: 1, repo_evidence: "src/parser.py line 14: input is plain text, not PDFs", reason: "The critic flagged that the input is underspecified — the README says 'PDFs' but the actual entry point only handles plain text. Going with what the code does." }
```

If the teacher accepts the defense in the next round, the flag is dropped. If the teacher restates the same concern with new evidence, the student must address it (no second defense on the same point). This bounded-defense structure forces real engagement instead of either side caving.

### Rule 3: Disagreement is a feature, not a problem

If the student and teacher are agreeing on every round, something is wrong — usually the student is being too deferential. Force at least one round per stage to involve substantive pushback (either a `[major]` flag from the teacher, or a defense from the student, or a redesign). If a stage closes in one round with no pushback, the decider should re-open it with a critique pass that specifically looks for what the first pass missed — and there's a concrete tool for that pass: `references/mined_review_checks.md`, the pool of checks mined from real reviewer comments. Pick the 3-6 items for that stage most likely to bite this specific paper and run them cold against the draft. This turns "look harder" from an intention into a procedure.

A useful self-prompt before accepting any draft: *"If a critic who hadn't seen this draft yet read it cold against the rubric, what's the first thing they'd flag?"* If you have a real answer, that's an unfired flag and the loop isn't done.

---

## How the loop differs in autoclaude mode

Same stages, same rubric (`references/stages.md`), same stop conditions (`references/discussion_loop.md`). The differences:

1. **No mid-stage user input.** The user is hands-off. If you would normally ask the user a question, instead document it as an open question in the confirmed output's notes and proceed with your best inference.
2. **Citation gaps in stage 3.** The repo probably won't tell you the related work for a research project — codebases rarely cite papers. Use whatever's in the docs (often a "References" section, or a `## Background` paragraph). For everything else, mark `citation: "[citation needed — not present in repo]"` and continue. Don't invent citations. Stage 3 will probably be the weakest stage in autoclaude output, and that's expected — the user can fill citations in afterward or run stage 3 again with a literature search tool if available.
3. **Round display defaults to "compact + final."** The user isn't watching every round. Keep per-round summaries to one line each so the full transcript stays browsable. Final outputs render in full.
4. **Output the seed brief alongside the confirmed outputs.** The user should be able to see what you started from. This makes it easy for them to spot where you misread the repo.
5. **No `ignore_and_submit` override.** The prime stop rule (a stage does not close over an open `[major]`) is strict here: Claude is the student, and a student who waves through their own majors defeats the self-play. Every `[major]` gets resolution rounds until resolved or the cap is hit.
6. **Round cap escalation goes to the user, not auto-decided.** If a stage hits the round cap (default 5, max 50) with `[major]` issues remaining, stop and surface to the user with: "Stage N hit the round cap with these issues unresolved: …. The repo doesn't seem to give clear guidance on this. How would you like to proceed?"

---

## Failure modes specific to autoclaude

These come up in repo-driven runs and are worth flagging early:

- **Repo doesn't describe a research project.** The codebase might be a CRUD app, a CLI tool, a game — something with no research framing. The student should attempt the workflow anyway (every project has *some* problem it solves), but the teacher should flag if the resulting framing feels strained. If three rounds in stage 1 still can't produce a non-strained problem statement, the project probably isn't research and the user should be told.
- **Multiple unrelated subprojects.** A monorepo with five different things in it. Pick the one the README is about, or ask the user which subproject to focus on.
- **Docs and code disagree.** The README describes one thing; the code does another. The student should go with the code (it's the ground truth) but explicitly note the discrepancy.
- **Empty or stub repo.** README is "TODO," code is mostly placeholders. Stop and tell the user — there's nothing to extract.

---

## Final deliverables

The three-artifact set from SKILL.md "Final deliverables" — **paper draft, standalone experiment design spec, and the full discussion trace** — plus one autoclaude extra: the **seed brief**, so the user can audit what you started from. The trace matters *more* here than in interactive mode: the user watched none of the rounds, so the trace is their only window into how the self-play actually went (including every defense, every re-opened stage, and every `[citation needed]`). With file tools available, write four files (`seed_brief.md`, `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`). Hand off to `research-paper-writing` for prose polish or `docx` for Word output, same as before.
