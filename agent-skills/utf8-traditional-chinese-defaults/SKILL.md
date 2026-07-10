---
name: utf8-traditional-chinese-defaults
description: Use when creating, reading, updating, normalizing, or converting text files where UTF-8 encoding, Traditional Chinese defaults, PowerShell text I/O, or suspected mojibake may affect the result.
---

# UTF-8 Traditional Chinese Defaults

## Script-First Execution

When validating Codex skills or investigating Windows encoding failures, use the bundled UTF-8-safe validator before treating a validation failure as a skill defect.

```sh
python agent-skills/utf8-traditional-chinese-defaults/scripts/validate_skill_utf8.py agent-skills/<skill-name>
```

For structured evidence:

```sh
python agent-skills/utf8-traditional-chinese-defaults/scripts/validate_skill_utf8.py agent-skills/<skill-name> --json
```

The validator reads `SKILL.md` with explicit `encoding="utf-8"` and reports decode errors cleanly. Use LLM judgement after this deterministic check to decide whether the issue is a file encoding problem, terminal display problem, validator limitation, or actual frontmatter defect.

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

## Workflow

1. Before reading or editing text files, check whether the project or nearby files already imply a language or encoding convention.
2. Treat UTF-8 as the default text encoding unless the user, file format, or project contract clearly requires another encoding.
3. Prefer Traditional Chinese for Chinese-language output unless the user or existing document clearly uses another language variant.
4. Follow the existing document language when it is clearly English, Simplified Chinese, or another requested style; do not rewrite language solely to enforce this preference.
5. When using PowerShell to read text files where encoding matters, use `Get-Content -Encoding UTF8`.
6. When using PowerShell commands that write text files, specify UTF-8 explicitly, such as `Set-Content -Encoding UTF8`, `Add-Content -Encoding UTF8`, `Out-File -Encoding UTF8`, or `Export-Csv -Encoding UTF8`.
7. If output looks garbled, first determine whether the issue is terminal display, incorrect read encoding, or damaged file contents before rewriting the file.
8. After document changes, verify the relevant file snippets, README indexes, or rendered text when practical.
9. When skill validation touches Traditional Chinese or mixed-language `SKILL.md` files, prefer the bundled UTF-8-safe validator or another command that explicitly decodes as UTF-8.

## Rules

- Do not rely on shell or OS implicit encoding defaults for text file writes.
- Do not mass-convert unrelated files to apply this convention.
- Do not rewrite existing English, Simplified Chinese, or other language content solely to enforce Traditional Chinese.
- Do not treat binary files, images, archives, or checksum-sensitive files as text.
- Preserve original bytes when the task is audit, forensics, checksum validation, or another workflow where exact bytes matter.
- Prefer dedicated editing tools such as `apply_patch` for repo edits; still assume UTF-8 output and avoid unnecessary encoding churn.
- If deviating from UTF-8 or Traditional Chinese defaults, briefly explain why in the final response.

## Output Notes

When relevant, use this report template:

```md
### Encoding Report

- Files changed:
- Encoding used or verified:
- Language convention followed:
- Validation performed:
- Any reason for deviating from UTF-8 or Traditional Chinese defaults:
```
