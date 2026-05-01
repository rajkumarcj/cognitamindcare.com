# Self-Assessment Page Design

**Date:** 2026-05-01
**Status:** Approved

## Context

Cognita Mindcare needs a self-assessment tool on the website so potential clients can gauge their mental/emotional state before booking a session. The page collects basic contact details, walks the user through 15 rated questions, computes a live score, and shows a personalized result explaining what coaching can help with. Data is submitted to Google Sheets via the existing Google Apps Script webhook.

## File

`/Users/veroraj/Website/assessment.html` — static HTML, same pattern as all other pages.

Add `<a href="assessment.html">Assessment</a>` to the nav in all 7 existing HTML files (between Workshops and Internships links).

## Wizard Structure (3 Steps)

### Step 1 — Basic Details

Fields:
- Name (text, optional)
- Email (email, required)
- Phone (tel, optional)

Button: "Start Assessment →" — validates email present, then transitions to Step 2.

### Step 2 — 15 Questions

UI:
- Progress bar: `Question X of 15`
- Live score label: `Score so far: X` (updates on each answer)
- One question at a time (JS shows/hides)
- 5 pill buttons per question: Not at all (0) / Rarely (1) / Sometimes (2) / Often (3) / Almost always (4)
- Selecting a pill highlights it (teal), auto-advances after 400ms delay
- Back button returns to previous question, score adjusts
- Score accumulates in a JS array of 15 values

Questions (in order):
1. I feel overwhelmed by my thoughts or responsibilities
2. I find it difficult to relax or switch off
3. I feel anxious without a clear reason
4. I overthink situations or conversations frequently
5. I feel mentally or emotionally exhausted
6. I struggle to stay focused on tasks
7. I feel low on motivation or interest in daily activities
8. I feel confused or stuck about my career or life direction
9. I struggle to make decisions about important areas of my life
10. I find it difficult to communicate my thoughts or feelings
11. I experience frequent misunderstandings or conflicts in relationships
12. I feel unheard or unsupported by people around me
13. I often feel self-doubt or lack confidence
14. I feel disconnected from myself or unsure about what I want
15. I feel like I need support but I'm unsure where to start

### Step 3 — Results + Submit

Scoring bands (total 0–60):

| Score | Band | "This session can help with..." |
|-------|------|--------------------------------|
| 0–15 | Doing Well | Building resilience, sharpening clarity, preventive mental fitness |
| 16–30 | Some Strain | Managing stress, improving focus, navigating relationship patterns |
| 31–45 | Elevated | Regaining balance, finding direction, rebuilding confidence |
| 46–60 | Needs Support | Structured support across emotional well-being, clarity, and relationships |

Display:
- Band label card (teal for Doing Well/Some Strain, rose for Elevated/Needs Support)
- "This session can help with..." paragraph
- Total score shown (e.g., "Your score: 24/60")
- "Submit & Book a Free Session" button

On submit — POST to Google Apps Script (same URL as contact.html):
- Fields: name, email, phone, score (integer), band (string)
- Success: show confirmation message (see below)
- Error: show fallback with WhatsApp link (`wa.me/918496979197`)

Confirmation message (on success):
> Thank you for completing this.
> Based on your responses, I'll personally review and share insights with you shortly.
> If you'd like to speak directly, you can also reach out via DM or WhatsApp.

## Styling

Follow existing site conventions:
- CSS variables: `--teal: #3AABA0`, `--rose: #C4A8B0`, `--bg-cream`, `--text-dark: #3A3A3A`
- Fonts: Playfair Display (headings) + DM Sans (body)
- All CSS embedded in `<style>` tag
- Mobile responsive at 900px breakpoint
- Pill buttons: `border-radius: 24px`, selected state = teal fill + white text
- Wizard step transitions: CSS opacity + transform fade

## Data Flow

```
User fills Step 1 → JS stores {name, email, phone}
User answers Step 2 → JS array[15] tracks scores, sums total
Step 3 renders band → User clicks Submit
→ fetch POST (no-cors) to Google Apps Script webhook
→ Success: show confirmation div
→ Error: show error div with WhatsApp fallback
```

## Google Apps Script

Reuse existing webhook URL from `contact.html`:
`https://script.google.com/macros/s/AKfycbyFs8UBshFo8zt7YoQZsLeKjmkTpED07-NCscYRLBIpgqGBLGpbyYeH-YvO6IYYdMvk/exec`

POST payload includes `form_type=assessment` so the Apps Script can route to a dedicated "Assessments" sheet tab. The existing Apps Script needs one update: check `form_type` and append to the correct tab. Fields logged: name, email, phone, score, band, timestamp.

**Note:** This Apps Script update is out of scope for this HTML implementation. The HTML page will POST correctly regardless — data will land in whatever sheet the script routes it to. User must update the Apps Script separately.

## SEO

- `<title>Mental Wellness Self-Assessment | Cognita Mindcare</title>`
- Meta description: "Take our free 15-question self-assessment to understand your mental and emotional well-being. Get personalized insights from Cognita Mindcare."
- Add `assessment.html` to `sitemap.xml`
- BreadcrumbList schema: Home → Assessment

## Verification

1. Open `assessment.html` in browser
2. Step 1: leave email blank → "Start" should not advance
3. Step 2: answer all 15 questions, verify score increments, back button adjusts score
4. Step 3: verify correct band shows for score ranges (test 0, 20, 35, 55)
5. Submit → check Google Sheet for new row with name/email/phone/score/band
6. Test on mobile (375px) — pills should wrap cleanly
7. Verify nav link appears on all 7 pages
