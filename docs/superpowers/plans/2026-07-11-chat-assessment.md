# Chat-Style Assessment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the wizard assessment with a chat-like interface — floating-bubble popup on `index.html`, inline full-width on `assessment.html` — sharing one script.

**Architecture:** One self-contained vanilla-JS file, `assessment-chat.js`, that injects its own CSS and builds all markup. Exposes `window.CognitaChat.mount(container)` (inline) and `window.CognitaChat.mountBubble()` (popup). Flow is a single async function using promise-returning input helpers. Scoring, bands, and the Apps Script POST are copied unchanged from the current wizard.

**Tech Stack:** Plain HTML/CSS/JS static site (GitHub Pages). No build step, no dependencies. Fonts: DM Sans / Playfair Display. Design tokens (`--teal`, `--cream`, `--border`, …) are defined in `:root` inline on every page — the component's CSS uses them with hex fallbacks.

## Global Constraints

- No new dependencies, no build step. One new file only: `assessment-chat.js`.
- Keep unchanged: SEO `<head>`/schema on both pages, page hero, bottom CTA, footer, nav script.
- Endpoint: `SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyKDlssYtpxkktCDXFHAXVd1iT1l2HcL-JaEQOvZAsnb4ZSFb0C5Zhdm9S74d0AO0TVOA/exec'`, POST params exactly `form_type=assessment, name, email, phone, score, band, band_desc`, `mode: 'no-cors'`.
- WhatsApp link: `https://wa.me/918496979197?text=Hi%2C%20I%20just%20completed%20the%20self-assessment%20and%20would%20like%20to%20speak%20directly.`
- Band thresholds: ≤15 Doing Well, ≤30 Some Strain, ≤45 Elevated, else Needs Support. Score 0–4 per question, 15 questions, max 60.
- User-typed text must be rendered with `textContent` or escaped (`esc()`) — never raw innerHTML.
- Forward-only chat: no editing past answers.
- No localStorage; popup close keeps in-memory state, reload resets.

---

### Task 1: Create `assessment-chat.js`

**Files:**
- Create: `assessment-chat.js`

**Interfaces:**
- Produces: `window.CognitaChat.mount(containerElement)` — renders inline chat into container, starts flow immediately. `window.CognitaChat.mountBubble()` — appends floating bubble + popup panel to `<body>`; chat is created and started on first open; × hides panel keeping state.
- Self-check: `node assessment-chat.js` runs band-boundary assertions and prints `band checks pass`.

- [ ] **Step 1: Write the file**

Full content of `assessment-chat.js`:

```js
/* Cognita Mindcare — chat-style self-assessment (inline + popup). No dependencies. */
(function () {
  'use strict';

  var SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyKDlssYtpxkktCDXFHAXVd1iT1l2HcL-JaEQOvZAsnb4ZSFb0C5Zhdm9S74d0AO0TVOA/exec';
  var WA_LINK = 'https://wa.me/918496979197?text=Hi%2C%20I%20just%20completed%20the%20self-assessment%20and%20would%20like%20to%20speak%20directly.';

  var QUESTIONS = [
    'I feel overwhelmed by my thoughts or responsibilities',
    'I find it difficult to relax or switch off',
    'I feel anxious without a clear reason',
    'I overthink situations or conversations frequently',
    'I feel mentally or emotionally exhausted',
    'I struggle to stay focused on tasks',
    'I feel low on motivation or interest in daily activities',
    'I feel confused or stuck about my career or life direction',
    'I struggle to make decisions about important areas of my life',
    'I find it difficult to communicate my thoughts or feelings',
    'I experience frequent misunderstandings or conflicts in relationships',
    'I feel unheard or unsupported by people around me',
    'I often feel self-doubt or lack confidence',
    'I feel disconnected from myself or unsure about what I want',
    'I feel like I need support but I\'m unsure where to start'
  ];
  var PILL_LABELS = ['Not at all', 'Rarely', 'Sometimes', 'Often', 'Almost always'];
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function getBand(score) {
    if (score <= 15) return { cls: 'well', label: 'Doing Well', helps: 'Building resilience, sharpening clarity, preventive mental fitness' };
    if (score <= 30) return { cls: 'strain', label: 'Some Strain', helps: 'Managing stress, improving focus, navigating relationship patterns' };
    if (score <= 45) return { cls: 'elevated', label: 'Elevated', helps: 'Regaining balance, finding direction, rebuilding confidence' };
    return { cls: 'support', label: 'Needs Support', helps: 'Structured support across emotional well-being, clarity, and relationships' };
  }

  var CSS = '\
.cchat-panel{display:flex;flex-direction:column;background:var(--cream,#F5F4F4);border:1px solid var(--border,#D4CCC8);border-radius:16px;overflow:hidden;font-family:"DM Sans",sans-serif;height:100%;}\
.cchat-head{display:flex;align-items:center;gap:.6rem;padding:.85rem 1rem;background:var(--teal,#3AABA0);color:#fff;position:relative;flex:none;}\
.cchat-dot{width:9px;height:9px;border-radius:50%;background:#8FF7A7;flex:none;box-shadow:0 0 0 3px rgba(255,255,255,.25);}\
.cchat-title{font-weight:600;font-size:.92rem;}\
.cchat-close{margin-left:auto;background:none;border:none;color:#fff;font-size:1.35rem;cursor:pointer;line-height:1;padding:.15rem .4rem;}\
.cchat-progress{position:absolute;left:0;bottom:0;height:3px;background:rgba(255,255,255,.9);width:0%;transition:width .3s;}\
.cchat-log{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.55rem;}\
.cchat-msg{max-width:84%;padding:.6rem .85rem;border-radius:14px;font-size:.88rem;line-height:1.5;color:var(--text,#3A3A3A);}\
.cchat-msg a{color:var(--teal,#3AABA0);font-weight:600;}\
.cchat-bot{background:#fff;align-self:flex-start;border-bottom-left-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,.06);}\
.cchat-user{background:var(--teal,#3AABA0);color:#fff;align-self:flex-end;border-bottom-right-radius:4px;}\
.cchat-user.cchat-skipped{background:var(--gray-bg,#EDEAE8);color:var(--muted,#7A7A7A);font-style:italic;}\
.cchat-typing span{display:inline-block;width:6px;height:6px;margin:0 1.5px;border-radius:50%;background:var(--muted,#7A7A7A);opacity:.4;animation:cchat-blink 1s infinite;}\
.cchat-typing span:nth-child(2){animation-delay:.2s;}\
.cchat-typing span:nth-child(3){animation-delay:.4s;}\
@keyframes cchat-blink{0%,80%,100%{opacity:.25;}40%{opacity:1;}}\
.cchat-dock{padding:.75rem;border-top:1px solid var(--border,#D4CCC8);background:#fff;flex:none;min-height:56px;}\
.cchat-form{display:flex;gap:.5rem;}\
.cchat-input{flex:1;min-width:0;padding:.6rem .8rem;border:1.5px solid var(--border,#D4CCC8);border-radius:10px;font-family:inherit;font-size:.88rem;color:var(--text,#3A3A3A);outline:none;}\
.cchat-input:focus{border-color:var(--teal,#3AABA0);}\
.cchat-send{padding:.6rem 1.1rem;border:none;border-radius:10px;background:var(--teal,#3AABA0);color:#fff;font-family:inherit;font-size:.88rem;font-weight:600;cursor:pointer;}\
.cchat-skip{margin-top:.5rem;background:none;border:none;color:var(--muted,#7A7A7A);font-family:inherit;font-size:.8rem;cursor:pointer;text-decoration:underline;}\
.cchat-pills{display:flex;flex-wrap:wrap;gap:.45rem;}\
.cchat-pill{padding:.55rem 1rem;border:2px solid var(--rose,#C4A8B0);border-radius:24px;background:#fff;font-family:inherit;font-size:.85rem;font-weight:500;color:var(--text,#3A3A3A);cursor:pointer;transition:background .18s,border-color .18s,color .18s;}\
.cchat-pill:hover{border-color:var(--teal,#3AABA0);color:var(--teal,#3AABA0);}\
.cchat-actions{display:flex;flex-direction:column;gap:.5rem;}\
.cchat-action{display:flex;align-items:center;justify-content:center;width:100%;padding:.7rem 1rem;border-radius:10px;font-family:inherit;font-size:.88rem;font-weight:600;cursor:pointer;text-decoration:none;}\
.cchat-action-primary{background:var(--teal,#3AABA0);color:#fff;border:none;}\
.cchat-action-primary:disabled{opacity:.6;cursor:default;}\
.cchat-action-wa{background:#fff;color:#128C7E;border:1.5px solid #25D366;}\
.cchat-result{max-width:100%;width:100%;text-align:center;padding:1.25rem;}\
.cchat-band-well{background:#e8f5f4;border:1.5px solid var(--teal-light,#7BCBC5);}\
.cchat-band-strain{background:#f0f8f7;border:1.5px solid var(--teal,#3AABA0);}\
.cchat-band-elevated{background:#fdf5f7;border:1.5px solid var(--rose,#C4A8B0);}\
.cchat-band-support{background:#f9eef1;border:1.5px solid #b08090;}\
.cchat-badge{display:inline-block;padding:.3rem .9rem;border-radius:99px;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.6rem;color:#fff;}\
.cchat-band-well .cchat-badge{background:var(--teal,#3AABA0);}\
.cchat-band-strain .cchat-badge{background:var(--teal-dark,#2A7A76);}\
.cchat-band-elevated .cchat-badge{background:var(--rose,#C4A8B0);}\
.cchat-band-support .cchat-badge{background:#9a6070;}\
.cchat-score{font-size:2.2rem;font-weight:800;color:var(--teal-dark,#2A7A76);line-height:1.1;}\
.cchat-band-elevated .cchat-score,.cchat-band-support .cchat-score{color:#9a6070;}\
.cchat-score span{font-size:.9rem;font-weight:500;color:var(--muted,#7A7A7A);}\
.cchat-helps-label{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted,#7A7A7A);margin:.8rem 0 .3rem;}\
.cchat-helps{font-size:.9rem;font-style:italic;line-height:1.55;}\
.cchat-bubble{position:fixed;right:22px;bottom:22px;width:58px;height:58px;border-radius:50%;background:var(--teal,#3AABA0);color:#fff;border:none;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.22);display:flex;align-items:center;justify-content:center;z-index:1001;transition:transform .15s;}\
.cchat-bubble:hover{transform:scale(1.06);}\
.cchat-popup{position:fixed;right:22px;bottom:92px;width:380px;max-width:calc(100vw - 30px);height:70vh;max-height:640px;z-index:1000;display:none;box-shadow:0 12px 40px rgba(0,0,0,.25);border-radius:16px;}\
.cchat-popup.cchat-open{display:block;}\
.cchat-inline{height:72vh;max-height:700px;}\
@media (max-width:480px){.cchat-popup{left:0;right:0;top:0;bottom:0;width:100%;height:100dvh;max-height:none;border-radius:0;}.cchat-popup .cchat-panel{border-radius:0;}}';

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function injectCSS() {
    if (document.getElementById('cchat-css')) return;
    var s = el('style');
    s.id = 'cchat-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function createChat(root, opts) {
    opts = opts || {};
    var panel = el('div', 'cchat-panel');
    var head = el('div', 'cchat-head');
    head.appendChild(el('span', 'cchat-dot'));
    head.appendChild(el('span', 'cchat-title', 'Cognita Check-In'));
    if (opts.onClose) {
      var x = el('button', 'cchat-close', '&times;');
      x.type = 'button';
      x.setAttribute('aria-label', 'Close chat');
      x.addEventListener('click', opts.onClose);
      head.appendChild(x);
    }
    var progress = el('div', 'cchat-progress');
    head.appendChild(progress);
    var log = el('div', 'cchat-log');
    log.setAttribute('role', 'log');
    log.setAttribute('aria-live', 'polite');
    var dock = el('div', 'cchat-dock');
    panel.appendChild(head);
    panel.appendChild(log);
    panel.appendChild(dock);
    root.appendChild(panel);

    var TOTAL = 3 + QUESTIONS.length;
    var doneSteps = 0;
    function tick() {
      doneSteps++;
      progress.style.width = Math.round(doneSteps / TOTAL * 100) + '%';
    }
    function scrollLog() { log.scrollTop = log.scrollHeight; }
    function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

    function botSay(html) {
      var t = el('div', 'cchat-msg cchat-bot cchat-typing', '<span></span><span></span><span></span>');
      log.appendChild(t);
      scrollLog();
      return sleep(600).then(function () {
        t.classList.remove('cchat-typing');
        t.innerHTML = html;
        scrollLog();
      });
    }

    function userSay(text, skipped) {
      var m = el('div', 'cchat-msg cchat-user' + (skipped ? ' cchat-skipped' : ''));
      m.textContent = text;
      log.appendChild(m);
      scrollLog();
    }

    function askText(o) {
      return new Promise(function (res) {
        dock.innerHTML = '';
        var form = el('form', 'cchat-form');
        var input = el('input', 'cchat-input');
        input.type = o.type || 'text';
        input.placeholder = o.placeholder || '';
        if (o.autocomplete) input.autocomplete = o.autocomplete;
        var send = el('button', 'cchat-send', 'Send');
        send.type = 'submit';
        form.appendChild(input);
        form.appendChild(send);
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          var v = input.value.trim();
          if (!v) return;
          userSay(v, false);
          dock.innerHTML = '';
          res(v);
        });
        dock.appendChild(form);
        if (o.skip) {
          var sk = el('button', 'cchat-skip', 'Skip this');
          sk.type = 'button';
          sk.addEventListener('click', function () {
            userSay('Skipped', true);
            dock.innerHTML = '';
            res('');
          });
          dock.appendChild(sk);
        }
        input.focus();
      });
    }

    function askPills() {
      return new Promise(function (res) {
        dock.innerHTML = '';
        var wrap = el('div', 'cchat-pills');
        PILL_LABELS.forEach(function (lab, i) {
          var b = el('button', 'cchat-pill', lab);
          b.type = 'button';
          b.addEventListener('click', function () {
            userSay(lab, false);
            dock.innerHTML = '';
            res(i);
          });
          wrap.appendChild(b);
        });
        dock.appendChild(wrap);
        scrollLog();
      });
    }

    function askSubmit() {
      return new Promise(function (res) {
        dock.innerHTML = '';
        var wrap = el('div', 'cchat-actions');
        var submit = el('button', 'cchat-action cchat-action-primary', 'Submit &amp; book a free session &rarr;');
        submit.type = 'button';
        submit.addEventListener('click', function () {
          submit.disabled = true;
          submit.textContent = 'Sending…';
          res();
        });
        var wa = el('a', 'cchat-action cchat-action-wa', 'Chat on WhatsApp instead');
        wa.href = WA_LINK;
        wa.target = '_blank';
        wa.rel = 'noopener';
        wrap.appendChild(submit);
        wrap.appendChild(wa);
        dock.appendChild(wrap);
        scrollLog();
      });
    }

    var state = { name: '', email: '', phone: '', answers: [] };

    function submitFlow(total, band) {
      return askSubmit().then(function () {
        var params = new URLSearchParams({
          form_type: 'assessment',
          name: state.name,
          email: state.email,
          phone: state.phone,
          score: total,
          band: band.label,
          band_desc: band.helps
        });
        return fetch(SCRIPT_URL, { method: 'POST', body: params, mode: 'no-cors' }).then(function () {
          dock.innerHTML = '';
          return botSay('<strong>Thank you for completing this.</strong> I’ll personally review your responses and share insights with you shortly. If you’d like to talk sooner, <a href="' + WA_LINK + '" target="_blank" rel="noopener">reach out on WhatsApp</a>.');
        }, function () {
          dock.innerHTML = '';
          return botSay('Something went wrong sending your results. You can try again, or <a href="' + WA_LINK + '" target="_blank" rel="noopener">reach us directly on WhatsApp</a>.').then(function () {
            return submitFlow(total, band);
          });
        });
      });
    }

    async function flow() {
      await botSay('Hi, I’m glad you’re here. This is a free mental wellness check-in — 15 quick questions, about 5 minutes, completely private.');
      await botSay('Before we start, what’s your name? <em>(optional)</em>');
      state.name = await askText({ placeholder: 'Your name', autocomplete: 'name', skip: true });
      tick();
      await botSay((state.name ? 'Nice to meet you, ' + esc(state.name) + '! ' : '') + 'What’s your email address? We’ll use it only to send you your results.');
      for (;;) {
        var v = await askText({ placeholder: 'your@email.com', type: 'email', autocomplete: 'email' });
        if (EMAIL_RE.test(v)) { state.email = v; break; }
        await botSay('Hmm, that doesn’t look like an email address — mind checking it?');
      }
      tick();
      await botSay('And your phone number? <em>(optional)</em>');
      state.phone = await askText({ placeholder: '+91 XXXXX XXXXX', type: 'tel', autocomplete: 'tel', skip: true });
      tick();
      await botSay('Great. I’ll share 15 statements. For each one, tap how often you’ve experienced it recently.');
      for (var i = 0; i < QUESTIONS.length; i++) {
        await botSay('<strong>' + (i + 1) + ' of ' + QUESTIONS.length + '.</strong> ' + QUESTIONS[i]);
        state.answers[i] = await askPills();
        tick();
      }
      var total = state.answers.reduce(function (s, a) { return s + a; }, 0);
      var band = getBand(total);
      await botSay('That’s all 15 — thank you' + (state.name ? ', ' + esc(state.name) : '') + '. Here’s where you stand:');
      var card = el('div', 'cchat-msg cchat-bot cchat-result cchat-band-' + band.cls,
        '<span class="cchat-badge">' + band.label + '</span>' +
        '<div class="cchat-score">' + total + ' <span>/ 60</span></div>' +
        '<div class="cchat-helps-label">We can help you with</div>' +
        '<div class="cchat-helps">' + band.helps + '</div>');
      log.appendChild(card);
      scrollLog();
      await botSay('Want me to send this to Cognita Mindcare? We’ll personally review and share insights with you.');
      await submitFlow(total, band);
    }

    var started = false;
    return {
      panel: panel,
      start: function () {
        if (started) return;
        started = true;
        flow();
      }
    };
  }

  function mount(container) {
    injectCSS();
    container.classList.add('cchat-inline');
    createChat(container, {}).start();
  }

  function mountBubble() {
    injectCSS();
    var popup = el('div', 'cchat-popup');
    var bubble = el('button', 'cchat-bubble');
    bubble.type = 'button';
    bubble.setAttribute('aria-label', 'Open free mental wellness check-in');
    bubble.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3C6.5 3 2 6.9 2 11.7c0 2.7 1.4 5.1 3.6 6.7-.1 1-.6 2.6-1.5 3.6 1.9-.2 3.8-1 5-1.8.9.2 1.9.3 2.9.3 5.5 0 10-3.9 10-8.8S17.5 3 12 3z"/></svg>';
    var chat = null;
    bubble.addEventListener('click', function () {
      var open = popup.classList.toggle('cchat-open');
      if (open) {
        if (!chat) {
          chat = createChat(popup, {
            onClose: function () {
              popup.classList.remove('cchat-open');
              bubble.focus();
            }
          });
          chat.start();
        }
        var f = popup.querySelector('.cchat-input') || popup.querySelector('.cchat-pill') || popup.querySelector('.cchat-close');
        if (f) f.focus();
      }
    });
    document.body.appendChild(popup);
    document.body.appendChild(bubble);
  }

  if (typeof window !== 'undefined') {
    window.CognitaChat = { mount: mount, mountBubble: mountBubble };
  } else {
    /* ponytail: `node assessment-chat.js` = band-boundary self-check, no test framework */
    var assert = require('assert');
    [[0, 'Doing Well'], [15, 'Doing Well'], [16, 'Some Strain'], [30, 'Some Strain'],
     [31, 'Elevated'], [45, 'Elevated'], [46, 'Needs Support'], [60, 'Needs Support']]
      .forEach(function (t) { assert.strictEqual(getBand(t[0]).label, t[1], 'score ' + t[0]); });
    console.log('band checks pass');
  }
})();
```

- [ ] **Step 2: Run self-check**

Run: `node assessment-chat.js`
Expected output: `band checks pass`

- [ ] **Step 3: Commit**

```bash
git add assessment-chat.js
git commit -m "Add shared chat-style assessment component"
```

---

### Task 2: Convert `assessment.html` to inline chat

**Files:**
- Modify: `assessment.html` — remove wizard markup (the three `wizard-step` divs, lines ~253–365), wizard-only CSS (the `/* ── Wizard ── */` block through `.rate-note strong`, lines ~127–196, plus `.wizard-card` rule inside the 900px media query), and the inline assessment script (SCRIPT_URL through `submitAssessment`, keep the Nav script at the bottom).

**Interfaces:**
- Consumes: `window.CognitaChat.mount(container)` from Task 1.

- [ ] **Step 1: Replace wizard markup**

Inside `<section class="section-wrap bg-cream"><div class="container">`, replace the three `<div id="step-N" class="wizard-step">…</div>` blocks with:

```html
      <div id="chat-root"></div>
```

- [ ] **Step 2: Remove wizard CSS**

Delete CSS rules: `.wizard-step`, `.wizard-step.active`, `.wizard-card`, `.wizard-card h2`, `.wizard-card .sub`, `.progress-wrap` through `.progress-fill`, `.question-box`, `.question-num-badge`, `.question-text`, `.question-hint`, `.pills-wrap`, `.pill-btn` (all variants), `.q-nav`, `.back-btn` (all variants), `.result-card` (all variants), `.result-badge` (all variants), `.result-score`, `.result-score-label`, `.result-helps-label`, `.result-helps-text`, `.confirm-msg`, `.error-msg` (and their `p` rules), `.rate-note`, `.rate-note strong`, and `.wizard-card { padding: … }` inside `@media (max-width: 900px)`. The `.form-group` rules are also dead once the wizard is gone — delete them too.

- [ ] **Step 3: Replace inline assessment script**

Delete from `const SCRIPT_URL = …` down to the end of `submitAssessment()` (keep the `// Nav` block). Just before the existing inline `<script>` that holds the nav code, add:

```html
  <script src="assessment-chat.js"></script>
```

and inside the remaining inline script (after the nav wiring), add:

```js
    CognitaChat.mount(document.getElementById('chat-root'));
```

- [ ] **Step 4: Verify in browser**

Run: `python3 -m http.server 8080 --directory /Users/veroraj/Website` (background)
Open `http://localhost:8080/assessment.html`: chat renders inline, greeting types in, name skippable, bad email rejected with bot reply, pills advance through all 15, result card + submit actions appear. No console errors.

- [ ] **Step 5: Commit**

```bash
git add assessment.html
git commit -m "Replace assessment wizard with inline chat interface"
```

---

### Task 3: Add chat bubble popup to `index.html`

**Files:**
- Modify: `index.html` — before closing `</body>`.

**Interfaces:**
- Consumes: `window.CognitaChat.mountBubble()` from Task 1.

- [ ] **Step 1: Add script + mount call**

Just before `</body>` in `index.html`:

```html
  <script src="assessment-chat.js"></script>
  <script>CognitaChat.mountBubble();</script>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8080/index.html`: teal bubble bottom-right; tap opens panel above it; chat starts; × closes; reopen resumes mid-conversation; mobile viewport (devtools, 390px) shows full-screen panel. No console errors, no layout clash with page content.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Add floating chat assessment bubble to homepage"
```

---

### Task 4: Full manual verification pass

**Files:** none new — fixes to the three files above if issues found.

- [ ] **Step 1: Run spec's test checklist on both pages**

- Skip name and phone; give bad email then good email.
- Answer all 15; verify score math (all "Almost always" → 60 / Needs Support; all "Not at all" → 0 / Doing Well).
- Submit → success bot message appears (check Apps Script sheet receives row if account available; otherwise verify request in devtools Network tab).
- WhatsApp links open correct wa.me URL.
- Popup: open/close/reopen keeps thread; Esc-free close via ×; focus returns to bubble.
- Mobile widths 390px and 320px: pills wrap, panel full-screen, inline chat usable.

- [ ] **Step 2: Fix anything found, re-verify, commit**

```bash
git add -A
git commit -m "Fix issues found in chat assessment verification"
```

(Skip commit if nothing found.)
