# Research skills and commands

The source portfolio supplies project-local skills in `.claude/skills/`:

| Skill | Purpose |
|---|---|
| auto-research-discussion | Six-stage research discussion and refinement |
| research-taste-auditor | Idea framing and mechanism specificity |
| pengsida-stage-reviewer | Stage-aware paper critique |
| paper-digest | Structured paper decomposition |
| pengsida-paper-writer | Research framing and paper writing |
| research-paper-writing | Section, narrative, and submission guidance |
| se-paper-reviewer | Software-engineering paper review |
| deep-research | Source-grounded literature investigation |
| academic-paper-review | Structured academic review |

Claude Code discovers these project-local skills. Other clients can read each
`SKILL.md` or install the desired package explicitly. These are instruction packages;
ARA does not automatically convert them into executable agents or include every
skill in each prompt. Real agent packages select their instructions and adapters through
the [agent contract](AGENT_PACKAGE_SPEC.md).

`.claude/commands/goal.md` describes the topic-to-draft process under
`research/topics/`. `.claude/commands/deerflow_review.md` describes draft review.
Choose a topic explicitly; the archive includes retired and superseded proposals.

The merge retains writing/review instructions, templates, digest helpers, and evidence
catalogs. It removes the redundant packaged `paper_digest.skill` and four one-off
calibration scripts tied to `/home/claude`. References to those scripts now point to
their pinned source revision. Their archived calibration scores were not rerun.

The Peng Sida writing bundle credits
[learning_research](https://github.com/pengsida/learning_research) and
[Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills).
The draft-review command attributes its research/review methods to
[deer-flow](https://github.com/bytedance/deer-flow). Original package credits are retained.
