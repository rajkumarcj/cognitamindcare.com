# Therapy Page Redesign — Design Spec

**Date:** 2026-07-11
**Goal:** Convert the Services page into a therapy-only page and remove corporate psychology as an offered service site-wide.

## Scope

### 1. `services.html` → Therapy page (same URL)

- Page title, meta description, keywords, OG/Twitter tags, JSON-LD: reworded for therapy/counselling (online & in-person, Bengaluru, remote across India).
- Hero: therapy-focused headline and copy. Primary CTA "Book a Free Session" → `contact.html`; secondary WhatsApp CTA (existing number, therapy-worded prefill).
- One services section (the Individual/Corporate split is removed) with 4 cards:
  1. **Individual Therapy** — anxiety, stress, depression, grief, life transitions.
  2. **Couples & Relationship Therapy** — communication, conflict, rebuilding connection.
  3. **Family Therapy** — family dynamics, parent–child relationships.
  4. **Career Counselling** — direction, decisions, work stress.
- Keep existing layout, CSS, card grid, and bottom CTA section (free 30-minute session + WhatsApp) unchanged in structure.
- Claude drafts all copy; user reviews in the finished page.

### 2. Site-wide changes

- **Nav link text:** "Services" → "Therapy" on all pages that carry the nav (index, about, services, contact, blog, blog post, workshops, internships). URL stays `services.html`; sitemap unchanged.
- **Footer links:** same rename where "Services" appears.
- **index.html:** remove the "Corporate Psychology" service card, the corporate audience panel, and the corporate CTA section (plus their now-unused CSS). Reword surrounding copy so the page reads coherently without them.
- **contact.html:** service dropdown — remove "Corporate Well-being"; add Individual Therapy, Couples & Relationship Therapy, Family Therapy, Career Counselling.
- **SEO/meta/JSON-LD across pages:** replace "corporate psychology" service wording with therapy wording where it describes offerings.

### 3. Explicitly kept (biography, not service)

- About page: "10+ Years in Corporate" credential and corporate-background narrative.
- "Corporate Psychologist" job title in bios/JSON-LD stays as-is (user did not request a title change).

## Out of scope

- No new pages, no URL changes, no redesign of layout/visual system.
- Workshops and internships pages: corporate mentions there describe curriculum/experience, not services — untouched except nav label.
- Blog content untouched except nav label.

## Success criteria

- `services.html` markets only the 4 therapy services.
- No page markets corporate psychology as an offering.
- All nav/footer links say "Therapy" and still point to `services.html`.
- Contact form options match the 4 therapy services.
