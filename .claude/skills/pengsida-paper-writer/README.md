# pengsida-paper-writer

A single consolidated skill for the full research-and-writing lifecycle, distilled and
refined from two sources:

- **Prof. Peng Sida (彭思达)** — `learning_research` research-process notes
  (https://github.com/pengsida/learning_research) and the writing template at
  https://pengsida.notion.site/c1a22465a0fa4b15a12985223916048e
- **Research-Paper-Writing-Skills** — the curated Skill packaging of Prof. Peng's
  writing template (https://github.com/Master-cai/Research-Paper-Writing-Skills)

All substantive methodology is Prof. Peng Sida's. This bundle's contribution is
consolidation: one SKILL.md, the section-by-section writing references and example bank,
plus a new `research-process.md` that folds in the idea/experiment/rebuttal/slides
methodology that the writing-only package left out.

## What it covers

- Research process: finding important problems, generating and pressure-testing ideas,
  planning and debugging experiments, rebuttals, slides — `references/research-process.md`
- Section writing: Abstract, Introduction, Related Work, Method, Experiments, Conclusion —
  load the matching the matching `references/SECTION.md`
- Paragraph flow / clarity check — `references/does-my-writing-flow-source.md`
- Adversarial pre-submission review — `references/paper-review.md`
- Concrete reusable templates and worked examples — `references/examples/`

## Install

### Claude Code

```bash
# global
mkdir -p "$HOME/.claude/skills"
cp -R pengsida-paper-writer "$HOME/.claude/skills/"
# or project-level
mkdir -p .claude/skills
cp -R pengsida-paper-writer .claude/skills/
```

Then in a prompt: `Please use the pengsida-paper-writer skill to improve my Introduction.`

### Codex

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R pengsida-paper-writer "$CODEX_HOME/skills/"
```

### Gemini

```bash
mkdir -p "$HOME/.gemini/skills"
cp -R pengsida-paper-writer "$HOME/.gemini/skills/"
```

## Structure

```
pengsida-paper-writer/
├── SKILL.md                  # core workflow + operating rules (routes everything)
├── README.md
├── agents/openai.yaml        # agent metadata
├── scripts/                  # digest helper and historical corpus catalogs
│   ├── corpus.json           # 36-paper catalog across 8 venues
│   └── digest_paper.py       # heuristic digest skeleton
├── assets/corpus-sample/     # 6 representative downloaded abstracts
└── references/
    ├── research-process.md   # idea / experiments / rebuttal / slides
    ├── paper-archetypes.md   # method / efficiency / analysis / resource / theory
    ├── corpus-evidence.md    # measured stats that justify the taxonomy
    ├── abstract.md  introduction.md  related-work.md
    ├── method.md  experiments.md  conclusion.md
    ├── paper-review.md  does-my-writing-flow-source.md
    ├── corpus/               # manifest, analysis, regression notes
    └── examples/             # templates + worked examples
    │                          #   incl. archetype-examples.md (5 annotated award abstracts)
```


## Credits & License

Primary credit to Prof. Peng Sida (彭思达). Original repo:
https://github.com/pengsida/learning_research. Writing-Skills packaging:
https://github.com/Master-cai/Research-Paper-Writing-Skills. MIT License.


Historical corpus-calibration harnesses used machine-specific paths and are available in the [original source](https://github.com/skill-stability/possible_autoresearch/tree/97cdf786bad3141c8883c7639690da867a44ded5/.claude/skills/pengsida-paper-writer/scripts). Archived calibration numbers have not been rerun by this merge.
