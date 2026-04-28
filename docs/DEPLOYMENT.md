# Deployment Guide

End-to-end deployment from clone to live URL. Plan for ~30 minutes.

## Prerequisites

- A Google Workspace account (personal Gmail works for testing; production deployments should use an organizational account)
- Permission to create Apps Script projects, Drive folders, and Sites in the target domain
- Basic familiarity with the Apps Script editor

## Step 1 — Drive folder structure (5 min)

In Google Drive, create:

```
Training Platform/
├── 01_Current_Materials/
├── 02_Tracker/
│   └── Certificates/
├── 03_Archive/
├── 06_Audit_Evidence/
└── 07_Governance/
```

Note the URL of the `Certificates` folder. You'll need its ID for `CONFIG.CERTIFICATES_FOLDER_ID`.

The folder ID is the last segment of the URL after `/folders/`:
```
https://drive.google.com/drive/folders/[THIS_PART_IS_THE_ID]
```

## Step 2 — Tracker spreadsheet (5 min)

Create a new Google Sheet inside `02_Tracker/`. Name it something like "Annual Training Tracker."

Set up the schema per `docs/SHEET_SCHEMA.md`:
- Row 1: 18 column headers
- Cell **O2**: Next Due formula (`ARRAYFORMULA` for unbounded autofill)
- Cell **P2**: Status formula (`ARRAYFORMULA` for unbounded autofill)
- Optional: conditional formatting on column P, freeze row 1, format dates

## Step 3 — Apps Script project (10 min)

From the open tracker spreadsheet:

**Extensions → Apps Script**

This creates a sheet-bound Apps Script project. The advantage: the script can use `SpreadsheetApp.getActiveSpreadsheet()` to find the tracker, no hardcoded ID needed.

Rename the project something descriptive (top-left of the editor): "Annual Training Web App."

Paste the four files:

1. **Code.gs** — replace the default `Code.gs` with the contents of `apps_script/Code.gs`. **Edit the CONFIG block** at the top with your agency's values (see `docs/CONFIG.md`).
2. **Index.html** — File → New → HTML file → name it `Index`. Paste contents.
3. **Stylesheet.html** — File → New → HTML file → name it `Stylesheet`. Paste contents.
4. **JavaScript.html** — File → New → HTML file → name it `JavaScript`. Paste contents.

Save the project (`Ctrl+S` or `Cmd+S`).

## Step 4 — Test certificate generation (3 min)

In the Apps Script editor, with `Code.gs` open:

1. From the function dropdown at the top of the editor, select `testCertificateGeneration`
2. Click **Run**
3. First time: Apps Script will ask for permissions. Approve them (the script needs access to Drive, Gmail, and Sheets).
4. Check `Logger` (View → Logs) for output: should see "Certificate generated at: [Drive URL]" and "Test email sent to: [your email]"
5. Open the test certificate in Drive and verify it looks right
6. Check your inbox for the test email

If the certificate looks wrong or the email doesn't arrive, fix issues here before going live.

## Step 5 — Deploy as web app (3 min)

In Apps Script editor:

**Deploy → New deployment**

- Click the gear icon next to "Select type" → **Web app**
- **Description:** "v1.0 initial deployment" (or your version number)
- **Execute as:** **User accessing the web app** ← important; uses the visitor's identity, not yours
- **Who has access:** **Anyone within [your organization]** ← restricts to your Workspace domain

Click **Deploy**.

You'll get a deployment URL ending in `/exec`. Copy it.

## Step 6 — Test the deployment (3 min)

Open the `/exec` URL in an **incognito/private window**. You'll be asked to sign in with your Workspace account. After signing in:

- The Welcome screen should load
- Walk through a few steps
- Submit the training with test data
- Verify a row was added to the tracker
- Verify a PDF was created in the Certificates folder
- Verify you got a confirmation email

If any of those fail, check the Apps Script execution log (View → Executions) for errors.

## Step 7 — Distribute (varies)

Three options for getting the deployment URL in front of users:

### Option A — Direct URL distribution
Email the `/exec` URL to staff. Simplest but the URL is ugly.

### Option B — Behind a Google Site
1. Go to **sites.google.com** → **+ Create**
2. Add a header banner with your agency logo
3. Add an intro section explaining the training (~2-3 sentences)
4. Add a button or link pointing to the `/exec` URL — recommend opening in a new tab
5. **Publish** with a slug like `agency-training`. You'll get a URL like `sites.google.com/your-domain/agency-training`

The Site is the friendly URL you give people; clicking through opens the training itself.

**Note on iframe embedding:** Google Sites *can* iframe-embed an Apps Script web app, but the iframe height is constrained and the training will get cut off. Strongly recommend the link/button approach instead.

### Option C — Behind a custom landing page
For a polished landing page with full design control, build a separate HTML page (a self-contained landing page template) and host it on:
- Your agency's intranet
- A static web host (GitHub Pages, Netlify, etc. — only viable for non-sensitive landing pages)
- Google Drive web hosting if your IT allows it

The landing page links to the deployed `/exec` URL.

## Step 8 — Ownership & sustainability (10 min — do this within a week of going live)

Critical: by default, the Apps Script project, the tracker sheet, and the Drive folder are owned by **whoever set them up**. If that person leaves, the entire system goes with them.

For each asset (Apps Script, Tracker Sheet, Certificates folder, Site):

1. Open the asset in Drive (for Apps Script: in the Apps Script editor, **File → Move**)
2. Right-click → **Share**
3. Add a **shared mailbox** (e.g., `infosec@your-agency.gov`) as an Editor first
4. Once added, change their role to **Owner**
5. The original creator becomes an Editor automatically

Now the system survives staff transitions.

## Versioning & updates

When you make content changes:

1. Edit `_build_index.py` and re-run `python3 _build_index.py` to regenerate `Index.html`
2. Bump `CONFIG.TRAINING_VERSION` in both `Code.gs` and `_build_index.py`
3. Paste the updated files into the Apps Script editor
4. **Deploy → Manage deployments → (your deployment) → Edit → Version: New version → Deploy**

Users will get the new version on their next page load. The old version is still queryable in the deployment history.

## Step 9 — (Optional) Set up automation triggers

The repo includes `Automation.gs` with four functions that complete the recertification flywheel. Each is a time-based Apps Script trigger you schedule via the Triggers panel.

### Add Automation.gs to your project

1. In the Apps Script editor: **File → New → Script file → name it `Automation`**
2. Paste the contents of `apps_script/Automation.gs`
3. Edit `AUTOMATION_CONFIG` at the top:
   - `BACKUP_FOLDER_ID`: a Drive folder where weekly tracker backups will be saved
   - `REPORT_RECIPIENTS`: email addresses for the quarterly compliance report
4. Edit `getTrainingUrl()` at the bottom to return your deployed Sites URL or web app URL

### Schedule the triggers

In the Apps Script editor sidebar, click the **clock icon** (Triggers) → **+ Add Trigger** for each:

| Function                | Event source | Time-based type | Schedule                |
|-------------------------|--------------|-----------------|-------------------------|
| `sendReminderEmails`    | Time-driven  | Day timer       | 6am to 7am              |
| `escalateOverdueStaff`  | Time-driven  | Day timer       | 7am to 8am              |
| `sendQuarterlyReport`   | Time-driven  | Month timer     | 1st of month, 8am to 9am (function self-checks for first Monday of quarter) |
| `backupTracker`         | Time-driven  | Week timer      | Sundays, 1am to 2am     |

### Test before activating

Run each function manually first (select from the function dropdown, click Run) to verify:
- `sendReminderEmails` — should log how many emails would be sent (zero is normal if no one's approaching their due date)
- `escalateOverdueStaff` — should log zero unless you have actually overdue staff
- `sendQuarterlyReport` — will return immediately if today isn't the first Monday of a quarter; comment out the `if (!isQuarterStart) return;` line temporarily to test
- `backupTracker` — should create a date-stamped copy of the tracker in your backup folder

Once each runs cleanly, set up the triggers and let them run.

### Email quota considerations

Apps Script limits `MailApp.sendEmail` to:
- **100 recipients/day** for consumer Gmail accounts
- **1,500 recipients/day** for Workspace accounts

For an agency of a few hundred staff, the daily reminder + escalation volume is well within limits. For larger deployments (5,000+ staff), consider batching reminders (e.g., send only on M/W/F instead of daily) or move to `GmailApp.sendEmail` which has higher quotas in some Workspace tiers.

---

## Troubleshooting

**"Sorry, the file you have requested does not exist."**
The deployment URL is wrong, or the deployment has been deleted. Check Deploy → Manage deployments.

**"Authorization required" loop**
The script's permissions changed. Re-run any function in the editor to re-trigger the permissions prompt.

**Certificate is blank or malformed**
Check that `CONFIG.CERTIFICATES_FOLDER_ID` is set to a valid Drive folder ID and that the Apps Script account has Editor access to that folder.

**Email doesn't arrive**
Check the Apps Script quota for `MailApp.sendEmail` (default is 100/day for consumer Gmail, 1500/day for Workspace). Check spam folder.

**Tracker shows phantom rows**
The Status formula might be using bounded ranges (`I2:I1000`) instead of unbounded (`I2:I`). Use unbounded.

**Sheet writes fail intermittently**
Apps Script has a 6-minute execution timeout. If certificate generation is slow (large folder, slow Drive), consider moving cert generation to a separate trigger called from a queue.
