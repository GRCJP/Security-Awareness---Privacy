# LinkedIn Post Drafts

Two variants below. Both work as standalone posts; pick the tone that matches your voice. Neither references a specific client.

---

## Variant A — Problem-led (recommended for broader reach)

Most agencies handle annual security awareness training the same way: a slide deck attached to an email, a sign-in sheet (or worse, a Google Sheet where people add their own name), and a stack of reply-all confirmations.

This satisfies nobody. Auditors can't verify who actually read it. Security teams have no central record of who's current and who's overdue. Employees forget the content within a week. And under NIST 800-53 Awareness and Training (AT) controls — the baseline virtually all federal compliance frameworks derive from — "everyone got the email" doesn't satisfy the evidence requirements.

So I built a working alternative — entirely in Google Workspace, no new infrastructure, no third-party SaaS. Just Apps Script, Sites, Sheets, Drive, and Gmail wired together to do something the slide deck can't:

→ Capture identity automatically via Workspace SSO
→ Walk users through 5 modules of structured content covering all major sensitive data categories — PII, regulated tax data, healthcare records, controlled unclassified information — with role-based content for privileged users
→ Generate a PDF certificate at completion, archived to Drive
→ Email a confirmation with the certificate attached
→ Log every completion to a tracker sheet with auto-calculated next-due dates and Current/Due Soon/Overdue status
→ Distribute behind a clean Google Sites URL with a branded landing page — the friendly front door staff actually click on
→ Automate the full recertification flywheel — reminder emails at 30/14/7/1 days, supervisor escalation past 7 days overdue, quarterly status reports — so the security team isn't manually chasing people
→ Adapt your existing training material — feed it your old PPT/PDF/DOCX and the included pipeline extracts structured content and maps it to the new training format, compressing weeks of copy-paste into hours of review

Total infrastructure cost: $0. Total stack: Google Workspace.

The deeper point: when "satisfying compliance" is the requirement, the lowest-friction solution that meets the actual control language usually wins. You don't need a six-figure LMS and a vendor relationship. You need a system that produces the evidence an auditor will accept, that runs itself once deployed, and that staff will actually complete.

I open-sourced the template so other agencies can adapt it. Repo + setup guide in comments. MIT-licensed. Brand it for your org, swap the data categories for whatever you handle (FTI, CJIS, FERPA, CUI, etc.), and you're 30 minutes from a deployable training.

How is your org handling annual security awareness today?

#GovTech #SecurityAwareness #ComplianceTraining #GoogleWorkspace #InfoSec #NIST

---

## Variant B — Build-led (recommended for technical audience)

I built a complete annual security awareness training platform in Google Workspace — Apps Script + Sheets + Drive + Sites + Gmail — and just open-sourced the template.

What it does:

• 5 modules, 29 interactive steps covering PII and other regulated data categories, with role-based content for privileged users (DBAs, system administrators, developers)
• Captures identity via Workspace SSO (no separate signup, no email validation)
• Generates a PDF certificate at completion, archived to a Drive folder, emailed to the user
• Writes to an 18-column tracker sheet with formula-driven next-due dates and Current/Due Soon/Overdue status
• Distributes via a branded Google Sites landing page — clean internal URL, restricted to the org's Workspace domain, friendly enough to put in onboarding emails
• Automates the recertification flywheel via time-based Apps Script triggers — reminder emails at 30/14/7/1 days before due, supervisor escalation when staff go more than 7 days overdue, quarterly compliance reports to security leadership
• Includes a content-extraction pipeline (Python) — feed it your existing training as PDF/DOCX/PPTX, it produces a structured JSON tree and a categorized Markdown draft mapped to the 5-module format, with auto-detected legal references for PRS verification
• Implements NIST 800-53 Awareness and Training (AT) family controls — AT-1 through AT-4 — making it portable across federal frameworks (HIPAA, CJIS, FERPA, CUI / DFARS / FedRAMP / StateRAMP, IRS, CMS) and state privacy laws

Why Google Workspace and not the obvious "build it on AWS" path?

→ Identity is solved. SSO inherits the org's existing access controls.
→ Auditors already trust it. Workspace logs are admissible.
→ Zero new infrastructure. Sheets is the database. Drive is the file store. MailApp is SMTP. Sites is the CDN.
→ Survives staff transitions cleanly when ownership is transferred to a shared mailbox.

Methodology note: source materials (IRS publications, agency policy docs, recorded webinars) were processed with Readwise Reader for transcription and highlight extraction, then LLM-assisted synthesis was used to map specific compliance points to module sections. This turned what would normally be weeks of manual content development into a few days.

The repo includes the full Apps Script source, a config-driven build script for the UI, deployment guide, sheet schema with the exact formulas, content adaptation guide for swapping data categories (FTI / CJIS / FERPA / CUI / etc.), and a brandable landing page template.

MIT-licensed. Adapt it for your agency. Link in the first comment.

#GoogleWorkspace #AppsScript #GovTech #ComplianceAutomation #InfoSec #NIST

---

## First comment (for either variant)

Repo: github.com/[YOUR_USERNAME]/sensitive-data-training

Read the README first — it walks through the architecture decisions, what's included, what's not, and how to brand it. CONFIG.md walks through the ~7 fields you edit to make it your own. Setup is ~30 minutes.

If you adapt this for your org, I'd love to hear how it goes — especially what compliance frameworks you're mapping it to and what content you ended up swapping in.

---

## Suggested cover image

For maximum engagement, post a screenshot of the Welcome screen alongside the post (LinkedIn images get 2x the engagement of text-only posts). Use a clean shot showing:
- The agency-branded header bar
- The hero with city/scenic backdrop
- The big "Begin Training" call to action

Crop to roughly 1200x627 (LinkedIn's preferred aspect ratio).

If you want to show the technical depth, include a second image: a screenshot of the tracker spreadsheet with the formulas visible and conditional formatting on the Status column showing a mix of Current/Due Soon/Overdue.

---

## Posting tips

- **Post on a Tuesday or Wednesday morning** (8-10am in your timezone) — highest LinkedIn engagement windows
- **Don't include the URL in the post body** — LinkedIn's algorithm deprioritizes posts with external links. Put the link in the first comment, mention "link in the first comment" at the end of the post
- **Engage with every comment** in the first 2 hours — the algorithm uses early engagement to decide whether to show your post to a wider audience
- **Tag 1-2 people** who would genuinely care about this (not random influencers — real connections in your network who work in GovTech, compliance, or InfoSec). They'll likely engage, which boosts initial reach.
- **Keep your hashtags to 5-7** — more than that signals spam to the algorithm
