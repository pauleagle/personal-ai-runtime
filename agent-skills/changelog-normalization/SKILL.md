---
name: changelog-normalization
description: Normalize, inspect, or clean up CHANGELOG.md files into versioned, categorized, user-readable release history. Use when the user asks to check,整理,標準化,normalize, rewrite, or prepare a changelog; before releases or tags; or when CHANGELOG.md contains loose notes, commit-log residue, AI conversation residue, TODOs, missing dates, ordering issues, or uncategorized entries.
---

# Changelog Normalization

## Purpose

將 `CHANGELOG.md` 整理成版本化、分類化、可讀的 release history，而不是開發流水帳、commit log 或 AI 對話紀錄。

## Script-First Execution

Before semantic cleanup, collect deterministic changelog structure evidence when a local file is available:

```powershell
python agent-skills/changelog-normalization/scripts/analyze_changelog_structure.py --repo-root . --changelog CHANGELOG.md --json
```

Use the same Python command on Linux/macOS shells. The helper checks file existence, UTF-8 readability, Markdown headings, version sections, ISO dates, category headings, newest-first date order, uncategorized entries, and likely TODO / commit-log / AI residue. Use LLM judgement only after this evidence to decide what to keep, merge, move, rewrite, remove, or ask the user about.

## Workflow

1. Run the script-first changelog structure check when `CHANGELOG.md` or another target changelog file is available; if the helper is unavailable or the changelog path is not local, state the fallback.
2. Read `CHANGELOG.md` first. Read nearby release/version files only when needed.
3. Identify format, ordering, date, category, and noise issues.
4. Detect loose development notes, commit-log residue, AI conversation residue, TODOs, and uncategorized entries.
5. Decide which entries to keep, merge, move, rewrite, remove, or place under `Unreleased`.
6. If the user asked only to inspect, analyze, or suggest, do not edit files.
7. If the user asked to normalize, clean up, rewrite, or apply changes, edit the changelog when version ownership and deletion scope are clear.
8. If version ownership, dates, deletion scope, or release scope are unclear, report the proposed strategy or ask before making destructive changes.

## Rules

- Keep latest versions at the top.
- Give each version its own section.
- Prefer dates for released versions.
- Categorize changes by type.
- Do not paste full commit messages verbatim.
- Do not paste AI conversation logs verbatim.
- Do not leave temporary TODOs or loose notes at the bottom.
- Put unclear version ownership under `Unreleased`.
- Do not invent version numbers, dates, features, or fixes.
- Avoid rewriting unrelated historical wording unless the task requires full normalization.

## Categories

Prefer these categories when applicable:

- Added
- Changed
- Fixed
- Removed
- Docs
- Internal
- Deprecated
- Security
- Breaking Changes

## Assessment Output

When reporting before edits, use concise sections:

```md
### Current Issues

### Proposed Structure

### Entries To Keep

### Entries To Merge Or Move

### Entries To Rewrite Or Remove

### Open Questions

### Next Steps
```
