---
name: changelog-normalization
description: Normalize, inspect, or clean up CHANGELOG.md files into versioned, categorized, user-readable release history. Use when the user asks to check,整理,標準化,normalize, rewrite, or prepare a changelog; before releases or tags; or when CHANGELOG.md contains loose notes, commit-log residue, AI conversation residue, TODOs, missing dates, ordering issues, or uncategorized entries.
---

# Changelog Normalization

## Purpose

將 `CHANGELOG.md` 整理成版本化、分類化、可讀的 release history，而不是開發流水帳、commit log 或 AI 對話紀錄。

## Workflow

1. Read `CHANGELOG.md` first. Read nearby release/version files only when needed.
2. Identify format, ordering, date, category, and noise issues.
3. Detect loose development notes, commit-log residue, AI conversation residue, TODOs, and uncategorized entries.
4. Decide which entries to keep, merge, move, rewrite, remove, or place under `Unreleased`.
5. If the user asked only to inspect, analyze, or suggest, do not edit files.
6. If the user asked to normalize, clean up, rewrite, or apply changes, edit the changelog when version ownership and deletion scope are clear.
7. If version ownership, dates, deletion scope, or release scope are unclear, report the proposed strategy or ask before making destructive changes.

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
