# Training Content Draft: Annual Sensitive Data Training

**Source:** `sample_training.pptx` (PPTX, 5 pages/slides)
**Sections extracted:** 5

---

## How to use this draft

This draft maps source-document sections to the 5-module training structure.
It is not the final training content — it is a working document for review.

**Workflow:**

1. Read through each module section below.
2. For each source section, decide: **Keep as-is**, **Rewrite**, **Merge**, or **Drop**.
3. For sections to keep/rewrite, transcribe to the corresponding module in `_build_index.py`.
4. Add scenarios, transitions, and module intros that aren't in source material.
5. Have the security team review the final content before publishing.

---

## Module: Handling

### Annual Sensitive Data Training
*Source: page/slide 1*

FY 2026 — Required for all staff with access to sensitive systems

### What is Sensitive Data?
*Source: page/slide 2*

Five categories require special protection:

- Personally Identifiable Information (PII)
- Federal Tax Information (FTI)
- Protected Health Information (PHI)
- Social Security Administration (SSA) data
- Financial / business sensitive records

**Speaker notes:** Emphasize that mishandling any of these creates real harm to real people. The legal consequences for the agency and the individual are severe. This is not a paperwork exercise.

### Need to Know Principle
*Source: page/slide 3*

Access is granted by job function, not seniority.

Even with general clearance, only access specific records your role requires.

Curiosity is not a need-to-know. Past relationships are not a need-to-know.

Every access is logged. Federal auditors review access logs.

**Speaker notes:** Real example: a state worker in 2023 was prosecuted under IRC 7213A for looking up the tax records of a celebrity case. Curiosity was the only motive. The conviction stood.

---

## Module: Consequences

### Reporting Incidents
*Source: page/slide 4*

The 24-hour rule:

When you suspect a problem, the clock starts immediately.

You don't need certainty before reporting. Just report.

False alarms are fine. Silence is not.

Contact the Information Security Office through the agency's incident reporting process.

### Personal Liability Under IRC
*Source: page/slide 5*

Federal law assigns personal liability:

- IRC §7213: up to 5 years federal prison + $5,000 fine
- IRC §7213A: up to 1 year prison + $1,000 fine for unauthorized inspection
- IRC §7431: civil damages, minimum $1,000 per incident
- Plus: termination, loss of clearance, permanent ineligibility for federal work

**Speaker notes:** Make clear: these penalties follow the individual, not the employer. The agency cannot indemnify employees against criminal liability for unauthorized disclosure.

---

## Detected Legal References

The source document references the following frameworks. Make sure your
Personal Responsibility Statement (PRS) in `Code.gs` references the same:

- IRC § 7213A (unauthorized inspection)

---

## Review Checklist

Before transcribing to `_build_index.py`, confirm:

- [ ] Source content is current (check effective date / revision)
- [ ] Agency-specific procedures are accurate (don't copy generic regulatory text verbatim)
- [ ] Each module has 3-5 distinct sections (not too sparse, not too dense)
- [ ] Scenarios are added — extracted source material rarely has them
- [ ] Module intro 'Picture this' hooks are written
- [ ] PRS in `Code.gs` references the legal frameworks listed above
- [ ] Penalty figures match current law (penalties have been adjusted for inflation)
- [ ] Information security team has reviewed for accuracy and completeness
