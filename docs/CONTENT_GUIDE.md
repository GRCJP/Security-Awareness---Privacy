# Content Guide

How the training content is structured, and how to adapt it for your agency's specific compliance frameworks and data types.

## Structure overview

The training is organized into **5 modules** containing **29 steps** total:

| Module | Steps  | Focus                                          |
|--------|--------|------------------------------------------------|
| 1 — Foundations          | 1-6    | What data privacy means, who's affected, why it matters |
| 2 — Handling Sensitive Data | 7-13  | The 5 categories: PII, FTI, FTI Privileged, PHI, SSA |
| 3 — In Practice            | 14-18 | Daily handling, do's and don'ts, disposal, email/AI |
| 4 — Consequences           | 19-23 | Mishandling, penalties, incident reporting          |
| 5 — Acknowledgment         | 24-28 | Five Things to remember, PRS signature, completion  |

Each module has an intro page with a "Picture this" scenario that grounds the content in a real situation.

## Where the content lives

All UI content is in `apps_script/_build_index.py`. The file is structured as a sequence of `sections.append(...)` calls that build up the 29 steps as Python f-strings.

Search for the section title (e.g., `"What is data privacy?"`) to find where it's defined. Edit the surrounding strings.

After editing, run:
```bash
python3 _build_index.py
```
This regenerates `Index.html`. Paste the new `Index.html` into Apps Script, then redeploy.

## Adapting to your agency

The default content references PII, FTI, PHI, and SSA data because those are the most common sensitive data categories in benefits-administering agencies. If your agency handles different data types, you'll want to swap or supplement these.

### Common data category swaps

| Default category | Alternative for your agency could be |
|------------------|--------------------------------------|
| FTI (Federal Tax Information) | CJIS data (Criminal Justice Info), CUI (Controlled Unclassified Info), ITAR-controlled data |
| PHI (Protected Health Information) | Student records (FERPA), substance abuse records (42 CFR Part 2) |
| SSA data | Veteran records (38 USC §5701), military personnel data |
| PII (general) | Same — almost universally relevant |

To swap a category:

1. Find the relevant module 2 section in `_build_index.py` (e.g., the "FTI" section)
2. Edit the section eyebrow, title, subtitle, body text, scenarios, and any data-card content
3. Update the PII feature spread (Module 2 closing slide) so the "5 categories" reflect your actual categories
4. Update the PRS in `Code.gs` to reference the actual frameworks your data falls under

### Common framework swaps

| Default framework | Alternative |
|------------------|-------------|
| IRS Pub 1075 (for FTI) | CJIS Security Policy (for criminal justice) |
| HIPAA (for PHI) | FERPA (for student records) |
| Privacy Act of 1974 (federal PII) | State-specific equivalents |

### Updating the PRS

The Personal Responsibility Statement (PRS) is in `apps_script/Code.gs` at the top:

```javascript
const PRS_STATEMENTS = [
  'I have completed the [agency] Annual Sensitive Data Training...',
  'I have been advised of the federal and state laws applicable to my access — which may include the Privacy Act of 1974, applicable state privacy laws, HIPAA Security Rule, and any sector-specific frameworks (tax data, healthcare, criminal justice, education records, or controlled unclassified information) governing the data I handle.',
  // ... etc
];
```

Edit each statement to reference your specific frameworks. Aim for **5 statements** total — short enough that users will actually read them, long enough to cover the core obligations.

The default PRS deliberately uses inclusive framing ("which may include...") so that an out-of-the-box deployment is safe across multiple regulatory contexts. Replace the inclusive language with explicit citations once you know which frameworks apply to your agency.

## Adding or removing modules

The training is modular by design. To add a 6th module:

1. In `apps_script/JavaScript.html`, edit the `MODULES` array:
   ```javascript
   const MODULES = [
     { name: 'Foundations',     range: [1, 6] },
     { name: 'Handling',        range: [7, 13] },
     { name: 'In Practice',     range: [14, 18] },
     { name: 'Consequences',    range: [19, 23] },
     { name: 'Acknowledgment',  range: [24, 26] },
     { name: 'Your New Module', range: [27, 30] }  // ← new
   ];
   ```
2. In `_build_index.py`, add new `sections.append(...)` blocks for the new step content
3. Adjust the step numbers throughout the sections that follow (eyebrows like "Module X · Section Y of Z")
4. Re-run the build script

To remove a module: do the reverse. Delete the `sections.append(...)` blocks for those steps, remove the entry from the `MODULES` array, and renumber.

## Adding new scenarios

Scenarios are click-to-reveal cards that present a real-world situation and the right answer. They live throughout the training inside specific sections.

The pattern in `_build_index.py`:

```python
<div class="scenario-card">
  <div class="scenario-prompt">
    <div class="scenario-q-label">Scenario</div>
    <p>You're a caseworker. A client asks you to email their case file to their personal Gmail because their work email is acting up. What do you do?</p>
  </div>
  <button class="scenario-reveal-btn">Show answer &darr;</button>
  <div class="scenario-answer">
    <div class="scenario-a-label">Answer</div>
    <div class="scenario-answer-text">
      <strong>Decline.</strong> Sensitive data leaves your control the moment it hits a personal account...
    </div>
  </div>
</div>
```

Best practices for scenarios:

- **Ground them in real situations.** Pull from documented incidents at peer agencies, or hypotheticals your security team has actually encountered.
- **Make the wrong answer plausible.** "Of course you wouldn't do that" scenarios are useless. The wrong answer should be tempting, common, or seemingly harmless.
- **Cite the relevant framework in the answer.** Reinforce that this isn't arbitrary — it ties to a specific control.
- **Keep it short.** Scenario prompt: 2-3 sentences. Answer: 3-4 sentences max.

## Tone & writing style

The default content uses a "direct but neutral" voice:

- **Avoid:** lecturing, hedging, jargon, legalese, fear-mongering
- **Aim for:** practical, plainspoken, respectful of the reader's time and intelligence
- **Examples in tone:**
  - ✓ "Don't email sensitive data through standard channels. The same rule applies to text messages and chat apps."
  - ✗ "Employees are reminded that the unauthorized transmission of sensitive information through unapproved electronic channels is strictly prohibited."

The first reads like a colleague telling you something useful. The second reads like a policy document — which people skim and forget.

## Methodology — using AI for content adaptation

If you have a stack of source materials (PDFs of IRS publications, recorded webinars, agency policy documents) and want to adapt this template to reflect them:

1. **Process source materials with Readwise Reader** (or any tool that handles bulk text/video ingestion). Highlight the key passages.
2. **Bulk-export your highlights** to text or markdown.
3. **Use an LLM** (Claude, GPT, etc.) to extract the specific compliance points from each source — what's the control, what behavior does it require, what's the consequence of non-compliance.
4. **Map extracted points to module sections.** This becomes your content outline.
5. **Draft scenarios** based on documented incidents or anonymized real examples from your agency.
6. **Have your information security team review.** They'll catch nuance that an LLM misses.

This is much faster than starting from scratch, and the resulting content is more accurate and specific than a generic vendor module.

## Versioning content changes

Whenever you make material changes to content:

1. Bump `CONFIG.TRAINING_VERSION` in both `_build_index.py` and `Code.gs` (e.g., `2026.1` → `2026.2`)
2. Re-run the build script
3. Redeploy

The version number is captured per completion in tracker column J, so you can audit-trail "who completed which version."
