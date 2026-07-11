# Therapy Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `services.html` into a therapy-only page ("Therapy") and remove corporate psychology as an offered service site-wide.

**Architecture:** Static HTML site, one self-contained file per page (inline CSS). All changes are copy/markup edits — no build step, no JS changes. URL `services.html` is kept; only content and link labels change.

**Tech Stack:** Plain HTML/CSS. Verification via `grep` and opening pages in a browser.

## Global Constraints

- URL stays `services.html`; `sitemap.xml` untouched.
- Nav/footer label becomes exactly `Therapy` (link href unchanged).
- The 4 therapy services, exact names: `Individual Therapy`, `Couples & Relationship Therapy`, `Family Therapy`, `Career Counselling`.
- Keep biography content: "10+ Years in Corporate" (about.html), "Corporate Psychologist" job titles in bios/JSON-LD/hero eyebrow.
- Keep existing layout/CSS structure; edit copy in place.
- Phone/WhatsApp number `918496979197` unchanged.

---

### Task 1: Rewrite `services.html` as therapy page

**Files:**
- Modify: `services.html` (head meta lines 11–54, hero lines 203–211, service sections lines 213–271, nav line 192, footer link line 309)

**Interfaces:**
- Produces: page section with the 4 therapy cards named in Global Constraints; nav label `Therapy` used by Task 2 pattern.

- [ ] **Step 1: Replace head metadata (title, description, keywords, OG, Twitter, JSON-LD)**

Replace lines 11–13 with:

```html
  <title>Therapy | Cognita Mindcare: Online &amp; In-Person Therapy in Bengaluru</title>
  <meta name="description" content="Individual therapy, couples and relationship therapy, family therapy, and career counselling in Bengaluru. Online sessions available across India." />
  <meta name="keywords" content="therapist Bengaluru, online therapy India, individual therapy, couples therapy Bengaluru, family therapy, career counselling, grief counselling, online counselling Bengaluru" />
```

Replace OG/Twitter title+description (lines 20–21 and 27–28) with:

```html
  <meta property="og:title" content="Therapy | Cognita Mindcare: Individual, Couples &amp; Family Therapy" />
  <meta property="og:description" content="Individual therapy, couples and relationship therapy, family therapy, and career counselling. Online and in-person in Bengaluru." />
```

```html
  <meta name="twitter:title" content="Therapy | Cognita Mindcare: Individual, Couples &amp; Family Therapy" />
  <meta name="twitter:description" content="Individual therapy, couples and relationship therapy, family therapy, and career counselling. Online and in-person in Bengaluru." />
```

Replace Service JSON-LD (lines 34–35, 41) values:

```json
    "serviceType": "Therapy & Counselling",
```
```json
    "description": "Individual therapy, couples and relationship therapy, family therapy, and career counselling. Online and in-person sessions.",
```

Replace breadcrumb item (line 51):

```json
      { "@type": "ListItem", "position": 2, "name": "Therapy", "item": "https://cognitamindcare.com/services.html" }
```

- [ ] **Step 2: Update own nav + footer label**

Line 192: `>Services</a>` → `>Therapy</a>` (keep `class="active"`). Line 309 footer: `Services` → `Therapy`.

- [ ] **Step 3: Replace hero copy**

Replace lines 203–211 with:

```html
  <section class="page-hero">
    <p class="page-hero-eyebrow">Online &amp; In-Person</p>
    <h1>Therapy That <span class="accent">Meets You Where You Are</span></h1>
    <p>Whether you're carrying anxiety, working through grief, or navigating a difficult relationship, you don't have to figure it out alone. Confidential, evidence-based therapy — online across India or in person in Bengaluru.</p>
    <div class="page-hero-actions">
      <a href="contact.html" class="btn btn-primary">Book a Free Session &rarr;</a>
      <a href="https://wa.me/918496979197?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20therapy%20sessions." target="_blank" rel="noopener" class="btn btn-outline">Chat on WhatsApp</a>
    </div>
  </section>
```

- [ ] **Step 4: Replace the two service sections with one therapy section**

Replace lines 213–271 (both `<!-- Individual Services -->` and `<!-- Corporate Services -->` sections) with:

```html
  <!-- Therapy Services -->
  <section class="section-wrap bg-blue">
    <div class="container">
      <div class="section-header">
        <h2>How We Can Help</h2>
        <p>Every session is confidential, unhurried, and grounded in evidence-based practice.<br>Start where it hurts — we'll find the way forward together.</p>
      </div>
      <div class="cards-grid">
        <div class="card">
          <div class="card-icon">&#9825;</div>
          <h3>Individual Therapy</h3>
          <p>One-on-one support for anxiety, stress, low mood, grief, and life transitions. A safe space to understand what you're feeling and build lasting ways to cope.</p>
          <a href="contact.html" class="card-link">Book a session &rarr;</a>
        </div>
        <div class="card">
          <div class="card-icon">💞</div>
          <h3>Couples &amp; Relationship Therapy</h3>
          <p>Work through conflict, rebuild trust, and learn to communicate so you feel heard — whether you're strengthening a good relationship or repairing a strained one.</p>
          <a href="contact.html" class="card-link">Book a session &rarr;</a>
        </div>
        <div class="card">
          <div class="card-icon">🏡</div>
          <h3>Family Therapy</h3>
          <p>Untangle family dynamics, ease parent–child tensions, and help your family talk to each other instead of past each other.</p>
          <a href="contact.html" class="card-link">Book a session &rarr;</a>
        </div>
        <div class="card">
          <div class="card-icon">🧭</div>
          <h3>Career Counselling</h3>
          <p>Find direction, navigate career decisions and work stress with confidence, and align your professional path with who you truly are.</p>
          <a href="contact.html" class="card-link">Book a session &rarr;</a>
        </div>
      </div>
    </div>
  </section>
```

Keep the existing `.services-cta` section (lines 274–283) unchanged.

- [ ] **Step 5: Verify**

Run: `grep -ci "corporate" services.html`
Expected: `0`

Run: `grep -c "card-link" services.html`
Expected: `4`

- [ ] **Step 6: Commit**

```bash
git add services.html
git commit -m "Rewrite services page as therapy-only page"
```

---

### Task 2: Rename nav/footer label "Services" → "Therapy" on all other pages

**Files:**
- Modify: `index.html:874,1146`, `about.html:450,605`, `contact.html:212,359`, `blog.html:198,269`, `blog-why-you-need-life-coaching.html:176,326`, `workshops.html:247,454`, `internships.html:265,502`

**Interfaces:**
- Consumes: nothing. Produces: consistent `Therapy` label site-wide.

- [ ] **Step 1: Apply rename**

```bash
cd /Users/veroraj/Website
sed -i '' 's|<a href="services.html">Services</a>|<a href="services.html">Therapy</a>|g' index.html about.html contact.html blog.html blog-why-you-need-life-coaching.html workshops.html internships.html
```

- [ ] **Step 2: Verify**

Run: `grep -rn '>Services</a>' *.html`
Expected: no output.

Run: `grep -rc '>Therapy</a>' index.html about.html contact.html blog.html blog-why-you-need-life-coaching.html workshops.html internships.html`
Expected: `2` per file.

- [ ] **Step 3: Commit**

```bash
git add *.html
git commit -m "Rename Services nav/footer label to Therapy site-wide"
```

---

### Task 3: Remove corporate offering from `index.html`

**Files:**
- Modify: `index.html` (JSON-LD line 54, hero lines 892–901, services grid lines 936–964, corporate audience panel lines 990–1001)

**Interfaces:**
- Consumes: therapy service names from Global Constraints.

- [ ] **Step 1: Update JSON-LD org description (line 54)**

```json
    "description": "Therapy, life coaching, workshops and internship programmes.",
```

(Line 38/40 "Life Coach & Corporate Psychologist" job title stays — biography.)

- [ ] **Step 2: Reword hero sub-description (lines 892–895)**

```html
        <p class="hero-subdesc">
          Whether you're working through anxiety, a difficult relationship, or a career crossroads,
          evidence-based therapy and coaching give you the clarity, confidence, and tools to move forward.
        </p>
```

Also line 901: `Explore Services &rarr;` → `Explore Therapy &rarr;`.

- [ ] **Step 3: Replace the two featured service cards**

Replace the "Individual Services" card (lines 938–943) and "Corporate Psychology" card (lines 945–950) with a single featured therapy card:

```html
        <div class="card card-featured">
          <div class="card-icon">&#9825;</div>
          <h3>Therapy &amp;<br>Counselling</h3>
          <p>Individual, couples, and family therapy, plus career counselling. Confidential, evidence-based support — online or in person.</p>
          <a href="services.html" class="card-link">Learn more &rarr;</a>
        </div>
```

Grid goes from 4 cards to 3 (Therapy, Workshops, Internships) — `cards-grid` auto-fits, no CSS change.

- [ ] **Step 4: Rework corporate audience panel into couples/families panel**

Replace lines 990–1001 (`panel-corporate` div) with:

```html
    <!-- Couples & Families -->
    <div class="audience-panel panel-corporate">
      <p class="panel-eyebrow">For Couples &amp; Families</p>
      <h2>Is home starting to feel heavy?</h2>
      <ul class="panel-questions">
      <li>Are the same arguments repeating without ever getting resolved?</li>
      <li>Do you feel unheard or distant from your partner?</li>
      <li>Is tension between parents and children wearing everyone down?</li>
      <li>Has trust been shaken, and you're unsure how to rebuild it?</li>
      <li>Do you want to communicate without it turning into a fight?</li>
      </ul>
      <a href="contact.html" class="btn btn-panel">Let's Talk &rarr;</a>
    </div>
```

(Keeps the existing `panel-corporate` CSS class for styling — class name is cosmetic; do not rename, YAGNI.)

- [ ] **Step 5: Verify**

Run: `grep -n "Corporate" index.html | grep -v "Psychologist" | grep -v "panel-corporate\|corporate {" `
Expected: no output (only job-title and CSS-class hits remain).

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Remove corporate psychology offering from homepage"
```

---

### Task 4: Update `contact.html` service dropdown + meta

**Files:**
- Modify: `contact.html:25` (JSON-LD description), `contact.html:252–260` (dropdown)

**Interfaces:**
- Consumes: therapy service names from Global Constraints. Note: `Enquiry.js`/form JS reads `#service` value generically — option values can change freely.

- [ ] **Step 1: Replace dropdown options (lines 252–260)**

```html
              <select id="service">
                <option value="">Select a service...</option>
                <option value="Individual Therapy">Individual Therapy</option>
                <option value="Couples &amp; Relationship Therapy">Couples &amp; Relationship Therapy</option>
                <option value="Family Therapy">Family Therapy</option>
                <option value="Career Counselling">Career Counselling</option>
                <option value="Life Coaching">Life Coaching</option>
                <option value="Workshop / Training">Workshop / Training</option>
                <option value="Other">Other</option>
              </select>
```

- [ ] **Step 2: Update JSON-LD description (line 25)**

```json
    "description": "Therapy, counselling and life coaching in Bengaluru. Book a free 30-minute discovery session today.",
```

- [ ] **Step 3: Verify**

Run: `grep -c "<option" contact.html`
Expected: `8`

Run: `grep -ci "corporate" contact.html`
Expected: `0` (check remaining hits are none; if any, they must be biography-only — inspect).

- [ ] **Step 4: Commit**

```bash
git add contact.html
git commit -m "Update contact form services to therapy offerings"
```

---

### Task 5: Sweep remaining offering-language + final verification

**Files:**
- Modify: `blog.html:35` (JSON-LD `about` array), `about.html:26,42` (JSON-LD description/knowsAbout — offering wording only)

**Interfaces:**
- Consumes: nothing.

- [ ] **Step 1: blog.html line 35**

```json
    "about": ["Mental Wellness", "Therapy", "Life Coaching", "Emotional Intelligence", "Leadership", "Resilience"]
```

- [ ] **Step 2: about.html JSON-LD**

Line 26 — reword offering while keeping biography:

```json
    "description": "A psychologist and therapist helping individuals, couples, and families achieve clarity, resilience, and emotional well-being through evidence-based practice.",
```

Line 42:

```json
    "knowsAbout": ["Therapy", "Counselling", "Life Coaching", "Emotional Intelligence", "Stress Management", "Mental Wellness"]
```

Keep line 25 `"jobTitle": "Life Coach & Corporate Psychologist"` and the "10+ Years in Corporate" credential (line 557) — biography per spec.

- [ ] **Step 3: Site-wide verification**

```bash
cd /Users/veroraj/Website
grep -rn -i "corporate" *.html | grep -v -i "psychologist\|10+ years in corporate\|corporate sectors\|corporate environments\|panel-corporate\|\.corporate\|workshops.html\|internships.html"
```
Expected: no output (only biography, CSS classes, and workshop/internship curriculum mentions remain).

```bash
open index.html services.html contact.html
```
Visual check: homepage 3-card grid, both audience panels styled, therapy page 4 cards, contact dropdown.

- [ ] **Step 4: Commit**

```bash
git add blog.html about.html
git commit -m "Reword remaining corporate offering language to therapy"
```
