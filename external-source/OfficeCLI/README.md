# OfficeCLI

## Source

- Repository: https://github.com/iOfficeAI/OfficeCLI/
- Clone URL: https://github.com/iOfficeAI/OfficeCLI/
- Local upstream clone: `upstream/clone/OfficeCLI/`
- Imported commit: `8e5bd2f0df201ddf77fa2c545bb28f78826c024a`
- License: Apache License 2.0, detected from upstream `LICENSE`

## What This Source Is

OfficeCLI is an external source about agent-operated Office document workflows. It provides a CLI-oriented interface for creating, reading, modifying, and rendering Word, Excel, and PowerPoint files.

## Why It Is Collected

This source may be useful for future work on:

- agent-friendly document automation patterns
- command-line Office document inspection and editing workflows
- render-review-revise loops for generated documents
- reusable skill or playbook patterns for document production
- cross-platform installer and binary distribution conventions

## Expected Extraction Direction

- Review the upstream `SKILL.md`, CLI command model, schema documentation, and rendering workflow.
- Extract reusable patterns for safe agent document editing and validation.
- Keep upstream code, examples, and media inside `upstream/clone/OfficeCLI/`.
- Put project-local reading notes under `notes/` and structured takeaways under `extracted/`.
- Include attribution if concepts, structure, or wording are adapted into playbooks, skills, prompts, or knowledge files.

## Status

- [x] Collected
- [ ] Reading
- [ ] Notes created
- [ ] Extracted
- [ ] Converted to knowledge
- [ ] Converted to playbook
- [ ] Converted to skill

## Local Structure

```text
external-source/OfficeCLI/
├─ README.md
├─ source-links.md
├─ LICENSE-OfficeCLI.md
├─ notes/
├─ extracted/
└─ upstream/
   └─ clone/
      └─ OfficeCLI/
```

## Notes

- The local upstream clone was imported from `main` at commit `8e5bd2f0df201ddf77fa2c545bb28f78826c024a`.
- Treat `upstream/clone/OfficeCLI/` as original source material. Keep project-local interpretation in `notes/` and structured output in `extracted/`.
