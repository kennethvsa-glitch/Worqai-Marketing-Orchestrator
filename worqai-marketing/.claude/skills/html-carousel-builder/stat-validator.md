# Stat Source Validator Reference — stat_source_validator.py

Scans carousel HTML for fabricated or unverified stat citations. Run after every render.

## Command

```bash
py scripts/stat_source_validator.py production/carousel_topic_s17.html
py scripts/stat_source_validator.py production/   # scans all .html in directory
```

Exit codes: `0` = all clean, `1` = fabricated or unverified sources found.

---

## How It Works

1. Reads each HTML file line by line
2. Skips `<style>` blocks entirely (CSS won't contain stat citations)
3. Skips lines with `data:image`, `base64,`, or `%3C` (encoded URLs)
4. Matches lines against `SOURCE_TAG_RE`: `(fuente|dato|source|data)\s*[:·]\s*([^<\n]{3,120})`
5. For each match:
   - If source matches a FABRICATED pattern → issue type `FABRICATED`
   - If source does NOT match the verified allow-list → issue type `UNVERIFIED`
   - If source matches the allow-list → clean, no issue

Suggested fix for any issue: `"Dato interno WorqAI · base de datos 2025"`

---

## Verified Sources Allow-List (VERIFIED_SOURCES)

Any source text that contains one of these substrings (case-insensitive) passes:

```
jobscan internal analysis
worqai database
worqai · base de datos
dato interno worqai
linkedin economic graph
world economic forum
future of jobs report
análisis interno profile pro latam
```

---

## Explicitly Banned Fabricated Patterns (FABRICATED_PATTERNS)

Regex patterns matched against source text (case-insensitive):

```
linkedin talent report 202X
linkedin talent solutions report 202X
jobscan ats report 202X
jobscan ats optimization report 202X
jobscan · state of the job search 202X
jobscan / linkedin talent report
```

These are known fake report titles that AI models hallucinate. Any match = FABRICATED, regardless of other content.

---

## Recommended Default Citation

When stat data comes from WorqAI's internal database or no external source is available:

```
Dato interno WorqAI · base de datos 2025
```

This matches `worqai · base de datos` in the allow-list and passes validation.

---

## Detection Scope

The validator detects citations rendered in HTML content. It does NOT check:
- The raw spec JSON (only the rendered HTML output is scanned)
- Data inside `<style>` blocks
- Inline images or base64 data

Scan the rendered HTML file, not the spec.
