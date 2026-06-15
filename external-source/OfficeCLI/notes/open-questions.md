# OfficeCLI Open Questions

## Source And License

- [ ] Is Apache License 2.0 sufficient for the intended derived artifact?
- [ ] Are there file-level notices, generated assets, examples, or media with separate attribution requirements?
- [ ] Should `agent-playbooks/external-source-copyright-notice-review.md` be run before any playbook or skill extraction?

## Technical Review

- [ ] Which OfficeCLI commands are stable enough to reference in an internal playbook?
- [ ] Which validation loop should be extracted: structural JSON inspection, HTML/PNG rendering, or both?
- [ ] Which document formats should be in scope for first extraction: Word, Excel, PowerPoint, or all three?
- [ ] Does the binary/install flow fit this workspace's cross-environment CLI bootstrap conventions?

## Integration Boundary

- [ ] Should OfficeCLI be treated as a general external source, a future playbook input, or a candidate tool dependency?
- [ ] Should derived guidance target Codex, Claude Code, or a platform-neutral agent workflow?
