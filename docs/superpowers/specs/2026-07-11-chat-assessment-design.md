# Chat-Style Assessment — Design

Date: 2026-07-11
Status: Approved

## Goal

Replace the 3-step wizard assessment with a chat-like interface, delivered two ways:

1. **Homepage (index.html):** floating chat bubble, bottom-right, opens a popup chat panel.
2. **Assessment page (assessment.html):** same chat rendered inline full-width where the wizard was. SEO head/schema, hero, CTA, and footer stay untouched.

## Architecture

One new file, `assessment-chat.js`, self-contained (injects its own CSS via a `<style>` tag; markup built in JS). It relies on the CSS custom properties (`--teal`, `--cream`, etc.) already defined inline on both pages.

Public API:

- `CognitaChat.mount(container)` — renders the chat inline into `container` (assessment.html).
- `CognitaChat.mountBubble()` — appends the floating bubble + popup panel to `<body>` (index.html).

Both call the same internal renderer; only the shell differs.

### Page changes

- **index.html:** add `<script src="assessment-chat.js"></script>` + one line calling `CognitaChat.mountBubble()`.
- **assessment.html:** remove wizard markup (steps 1–3), wizard CSS, and inline assessment script. Keep head, hero, bottom CTA, footer, nav script. Add `<div id="chat-root"></div>` + script tag + `CognitaChat.mount(...)`.

## Chat flow (forward-only, no editing)

1. Bot greets, asks **name** — text input with a "Skip" affordance.
2. Asks **email** — required; invalid input gets a bot reply asking to re-check (regex same as current: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`).
3. Asks **phone** — text input, skippable.
4. Bot explains the 0–4 scale once.
5. Asks the 15 questions (same array as today) one at a time. Answers via 5 tap-pills (Not at all → Almost always). Selected pill becomes a user bubble; typing indicator (~600 ms) precedes each bot message.
6. **Result in-chat:** bot closing message (personalised with name if given), then a result card bubble — band badge, score / 60, "We can help you with" text. Band thresholds unchanged (≤15 well, ≤30 strain, ≤45 elevated, else support).
7. Action buttons as chat actions: **Submit & book a free session** and **WhatsApp** link (same wa.me URL).
8. Submit POSTs to the existing Apps Script `SCRIPT_URL` with the same params (`form_type=assessment`, name, email, phone, score, band, band_desc), `mode: 'no-cors'`. Success and error render as bot messages (success includes WhatsApp link; error offers retry).

## Popup behaviour (homepage)

- Floating teal bubble, fixed bottom-right, chat icon.
- Tap → panel opens above the bubble: ~380 px wide, ~70 vh tall; full-screen (100 % × 100 dvh) under ~480 px viewports.
- Panel header: green status dot, "Cognita Check-In", thin progress bar (fills across intake + questions), × close.
- × collapses the panel; chat state kept in memory — reopening resumes. Reload resets (no localStorage).

## Accessibility

- Message list `role="log"` / `aria-live="polite"`.
- Pills and buttons are real `<button>`s; text input Enter-submits.
- Focus moves into panel on open, back to bubble on close.

## Out of scope (deliberate)

- localStorage persistence, auto-open, bubble on pages other than the homepage, editing past answers, backend changes.

## Testing

Manual run-through on both pages: skip name/phone, bad-then-good email, all 15 answers, each band boundary (0, 15, 16, 30, 31, 45, 46), submit success path, mobile viewport, popup open/close/resume.
