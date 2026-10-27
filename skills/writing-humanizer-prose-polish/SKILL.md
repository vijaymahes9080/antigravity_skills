---
name: writing-humanizer-prose-polish
description: >-
  Humanize and de-slop AI-sounding prose while preserving meaning, factual accuracy,
  technical terms, and the writer's authentic voice. Remove AI fingerprints (inflated
  significance, stock buzzwords, uniform rhythm, sycophancy, formulaic conclusions)
  and perform conservative text-hygiene checks. Use when asked to humanize, de-slop,
  rewrite naturally, match a voice or sample, or improve writing quality.
metadata:
  version: 2.0.0
  source_repos:
    - https://github.com/RealOrangeKun/humanizer
    - https://github.com/hannsxpeter/humanizer
  license: MIT
---

# Humanizer

Turn AI-flavored, corporate, or machine-smooth prose into writing that reads as the work of an actual person. When a writer's voice is available, make it read as the work of *that specific person*.

The goal is prose that a discerning reader would not flag as synthetic, with its original meaning, technical facts, and human texture intact. The goal is **not** to trick or defeat detectors, and this skill names and optimizes against none.

This unified skill integrates the strongest compatible features from:
- **[hannsxpeter/humanizer](https://github.com/hannsxpeter/humanizer)**: Structural variance, multi-pass workflow, anti-fabrication hard-line, density pre-checks, voice matching, restraint guardrails, and conservative text hygiene.
- **[RealOrangeKun/humanizer](https://github.com/RealOrangeKun/humanizer)**: 24 pattern catalog based on Wikipedia AI cleanup, explicit filler phrase removals, copula avoidance, and slash-command support.

---

## Slash Command & Invocation

Invoke this skill in Antigravity via:
- `/humanizer [paste text]`
- `/humanizer Rewrite the selected paragraph naturally.`
- `/humanizer Improve this assignment without changing its meaning.`
- `/humanizer Make this report clearer and less repetitive.`
- `/humanizer Match the writing style of my supplied sample.`
- `/humanizer Fix this content while preserving all technical terminology.`

### Antigravity Invocation Mechanism
1. **Slash Command**: Typing `/humanizer` triggers this skill directly when registered in the workspace (`.agents/skills/humanizer/`) or globally (`~/.gemini/config/skills/humanizer/`).
2. **Natural Language**: Requests such as *"humanize this draft"*, *"remove AI buzzwords"*, *"make this sound like me"*, or *"de-slop this report"* activate the skill automatically via progressive disclosure.
3. **Gemini CLI / Command Integration**: For CLI environments, a matching command definition is provided in `commands/humanizer.toml`.

---

## Core Principle: Variance Over Substitution

AI prose reads as artificial primarily because of **uniformity**: even sentence lengths, balanced clauses, repetitive hedging, and predictable rhythms. Mechanically replacing buzzwords (e.g., swapping "delve" with "explore") merely shifts the machine signature.

True humanization comes from **structural and rhythmic variance**:
- Alternating very short punchy sentences with longer, winding, subordinated thoughts.
- Occasional natural fragments.
- Asymmetrical development where simple ideas stay brief and complex ideas take time.
- Varying how you vary—avoiding a new repetitive template.

---

## 10-Step Humanization Workflow

When this skill is invoked, execute this sequence:

1. **Understand Purpose & Audience**: Identify the intended audience, target register (formal, conversational, academic, technical), language (e.g., English, Tamil), and desired tone.
2. **Inspect Context & Style Sources**: Check for supplied writing samples, an active `VOICE.md`, `STYLE-GUIDE.md`, or project instructions.
3. **Calibrate Effort (Density Pre-check)**: Skim the text for dead-giveaways (promotional fluff, chatbot artifacts, buzzword clusters) to determine pass intensity:
   - *Low (0–2 tells/100 words)*: **Light edit** (fix only dead-giveaways; leave genuine quirks untouched).
   - *Medium (3–5 tells/100 words)*: **Standard rewrite** (apply catalog with restraint; protect what works).
   - *High (6+ tells/100 words)*: **Full rewrite** (push strong structural variance and clean all formulaic patterns).
4. **Preflight Text Hygiene**: Conservatively check for invisible Unicode (zero-width spaces, anomalous line breaks, stray direction overrides) while strictly preserving language-critical joiners (e.g., Tamil/Indic ZWJ/ZWNJ).
5. **Establish Voice (Pass 1)**: If a writing sample, named author, or voice profile is provided, shape the draft toward that cadence and diction *before* pruning patterns. (Skip in generic mode).
6. **Eliminate AI Tells (Pass 2)**: Walk the prose against the unified 34-pattern catalog in [references/tell-patterns.md](references/tell-patterns.md). Fix the underlying thought rather than swapping surface tokens.
7. **Perform Self-Audit & Restraint Check (Pass 3)**: Review against [references/do-not-flag.md](references/do-not-flag.md). Revert edits that flattened authentic quirks, introduced uniform rhythms, or compromised natural human expression.
8. **Enforce Meaning & Factual Integrity**: Verify that every technical term, equation, citation, number, date, and logical conclusion matches the source exactly. Remove any soft inferences or invented details.
9. **Verify Hygiene & Language Preservations**: Ensure non-Latin scripts, formatting, and mathematical symbols remain intact.
10. **Deliver Output**: Return the copy-ready revised text accompanied by the concise audit report.

---

## Strict Rules

- **Zero Hallucination / Anti-Fabrication Hard-Line**: Never invent facts, statistics, sources, quotes, causes, or lived experiences to make prose "sound concrete." If the original text is vague, say less plainly; do not manufacture details.
- **Preserve Factual Meaning**: Never change or distort the author's meaning to make a sentence sound smoother.
- **No Mechanical Synonym Churn**: Never replace every instance of a word with an arbitrary thesaurus synonym.
- **No Forced Informality**: Never inject slang, intentional grammatical mistakes, or colloquial contractions into formal, legal, or academic writing.
- **Protect Domain Terms & Code**: Preserve all programming code, formulas, academic citations, tables, and domain-specific jargon.
- **Respect Multilingual Contexts**: Honor requested languages (e.g., Tamil, English, bilingual texts). In Indic scripts such as Tamil, preserve Zero-Width Non-Joiners (ZWNJ) and Zero-Width Joiners (ZWJ) required for proper conjunct formation.
- **No Over-Editing**: If a piece of text is already human, direct, and well-written, make minimal or no changes and state so clearly.
- **No AI-Detector Guarantees**: Never claim that text is guaranteed to bypass AI detection or achieve a 0% score. AI detectors are probabilistic and unreliable proof of authorship.

---

## Output Contract

Unless the user explicitly requests **"only the revised text"**, format the output using this structure:

```markdown
## Humanized draft
Voice: [generic | from FILENAME | matched to sample | author: NAME] [append " + stance" if stance mode was requested]
Density: [low -> light pass | medium -> standard pass | high -> full pass]
Text hygiene: [no suspicious characters visible | cleaned: DETAILS | not verifiable in this interface]

[The complete, copy-ready rewritten prose]

## What changed
- [Pattern family / item]: [Concise explanation of what was adjusted and why; max 5-8 bullets]
- [Text hygiene]: [Note if formatting residue was cleaned]

## Deliberately left alone
- [Human trait or technical phrasing preserved, and why it was kept; 1-3 bullets]

## Meaning check
[1-2 sentences confirming that facts, numbers, citations, and intent were preserved without distortion or fabrication.]
```

*Note: If the user prompts "Return only the rewritten text" or passes the text through automated scripts, omit the metadata sections and output the revised prose directly.*

---

## On-Demand Reference Documentation

Consult these reference documents only when needed for the active task:
- [references/tell-patterns.md](references/tell-patterns.md): Complete 34-pattern catalog across 6 families (Inflated Significance, Promotional Language, Formulaic Structure, Lexical Tics, Syntactic Tics, Formatting Artifacts).
- [references/do-not-flag.md](references/do-not-flag.md): Restraint guidelines, false positive protections, and genuine human writing markers to preserve.
- [references/voice-matching.md](references/voice-matching.md): Cadence extraction from raw samples, named author modeling, and `VOICE.md` schema.
- [references/text-hygiene.md](references/text-hygiene.md): Conservative Unicode cleaning rules, load-bearing exceptions (Tamil/Indic joiners, bidi controls), and regex patterns.
- [references/examples.md](references/examples.md): Concise before-and-after runs (Generic de-slop, Voice-matching, Restraint on human text, Technical/Academic prose).

---

## Attribution & License

This skill is open source under the **MIT License**.
- Based on `hannsxpeter/humanizer` (Copyright (c) 2026 aihxp, MIT License).
- Incorporates features and pattern categorizations from `RealOrangeKun/humanizer` (Adapted from blader's humanizer and the Wikipedia AI Cleanup project).
