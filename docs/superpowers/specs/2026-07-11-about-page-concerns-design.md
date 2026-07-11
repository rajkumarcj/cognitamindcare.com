# About Page: Org Removal + Concern List — Design Spec

**Date:** 2026-07-11
**Goal:** Remove organisation-as-client marketing from the About page and expand the hero bio list to the full concern list. Therapy page stays as is (chips section kept).

## Changes (about.html only)

1. **Hero bio** — remove the "And with organizations aiming to: build resilient teams / strengthen leadership / improve performance" block. Intro list becomes:
   - Lead-in: "I work with individuals, couples, and families navigating:"
   - Items: Anxiety and overthinking; Depression; Stress; Career uncertainty; Relationship challenges; Self-esteem; Postpartum support; Parenting support
   - Fix em dash: "The goal is not just insight, but real, lasting change."
2. **Company story** — "…personal fulfilment and organisational success… individuals and organisations across India…" → "…a meaningful, fulfilling life… individuals, couples, and families across India…". Follow-up line: "Sessions are available online across India and in person in Bengaluru."
3. **Growth card** — "Enabling individuals and organizations…" → "Helping you improve performance, build resilience, and grow with confidence in today's fast-changing world."
4. **Titles/meta** — jobTitle, OG/Twitter titles and descriptions: "Life Coach & Corporate Psychologist" → "Psychologist & Therapist". Keywords: replace "corporate psychologist profile" with therapist terms. Photo alt → "Veroanica, Psychologist and Therapist".

## Kept (biography)

- "extensive experience in corporate environments" line in her intro.
- "10+ Years in Corporate — IT and corporate sectors" credential.
- schema.org `"@type": "Organization"` (technical, not marketing).

## Out of scope

- Therapy page untouched (concern chips stay).
- No other pages.

## Success criteria

- About page markets only to individuals, couples, families.
- Hero list shows the 8 merged concerns.
- No em/en dashes in visible text.
