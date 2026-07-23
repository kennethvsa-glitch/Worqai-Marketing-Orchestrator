# Changelog Update Prompt

Use this exact prompt after any session that changes the carousel builder system:

---

```
Update the changelog at .claude/rules/changelog.md with what we just did.
TODAY IS 5/18/2026 USE THIS DATE IN THE ENTRY.
Rules:
- READ the file first. Do NOT overwrite it.
- Add a new entry at the VERY TOP (above the newest existing entry).
- Use this format:

## YYYY-MM-DD — Brief headline

### Added / Fixed / Changed / Removed / Decisions made
- Bullet points only. Specific files, specific changes.
- If a production carousel was built: filename, system, slide count, hook type.
- If a script was modified: what changed and why.
- If a skill was updated: what rule was added/removed/changed.

### Problems hit
- What broke, how we fixed it.

### What was rejected / deferred
- What we decided NOT to do and why.

- Keep it under 100 lines if possible. Brevity over completeness.
- Do NOT repeat historical entries. Only this session.
```

---

Copy-paste the block above into any LLM conversation after a build session.
