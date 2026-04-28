# Tracker Spreadsheet Schema

The training tracker is an 18-column Google Sheet that captures every completion. The Apps Script writes columns A-N and Q-R; columns O and P are calculated by formulas.

## Header row (row 1)

| Col | Header               | Source       | Notes                                           |
|-----|----------------------|--------------|-------------------------------------------------|
| A   | Timestamp            | Apps Script  | When `submitTraining()` was called              |
| B   | Email                | Apps Script  | From `Session.getActiveUser().getEmail()`       |
| C   | First Name           | Form         | User-entered                                    |
| D   | Last Name            | Form         | User-entered                                    |
| E   | Role                 | Form         | Free text (e.g. "Caseworker", "DBA")            |
| F   | Handles Sensitive    | Form         | Yes / No / Unsure                               |
| G   | FTI Access           | Form         | Yes / No / Unsure                               |
| H   | Supervisor Email     | Form         | User-entered, validated as email format         |
| I   | Training Date        | Apps Script  | Same as Timestamp; separate for analytics       |
| J   | Version              | Apps Script  | From `CONFIG.TRAINING_VERSION`                  |
| K   | Confirmation         | Apps Script  | Always "Acknowledged" (placeholder for future)  |
| L   | PRS Text             | Apps Script  | Full PRS text user signed, joined by " &#124; " |
| M   | Signature            | Apps Script  | Typed name from form                            |
| N   | Rating               | Form         | 1-5 (optional)                                  |
| O   | Next Due             | **Formula**  | `=IF(I="","",I+365)` — recertification deadline |
| P   | Status               | **Formula**  | "Current" / "Due Soon" / "Overdue"              |
| Q   | Notes                | Form         | User-entered (optional)                         |
| R   | Certificate URL      | Apps Script  | Drive link to PDF certificate                   |

## Formula column setup

Two columns use `ARRAYFORMULA` so they auto-populate as new rows are added. Paste these into the formula bar of cells **O2** and **P2** respectively.

### Column O — Next Due

```
=ARRAYFORMULA(IF(I2:I="","",I2:I+365))
```

Replace `365` with your `RECERTIFICATION_DAYS` value if different.

### Column P — Status

```
=ARRAYFORMULA(IF(O2:O="","",IF(REGEXMATCH(LOWER(Q2:Q&""),"manual"),P2:P,IF(TODAY()>O2:O,"Overdue",IF(O2:O-TODAY()<=30,"Due Soon","Current")))))
```

Status logic:
- If `Notes` contains "manual" (case-insensitive), preserve any manually-set status
- Else if today is past the Next Due date → "Overdue"
- Else if Next Due is within 30 days → "Due Soon"
- Else → "Current"

**Important:** use unbounded ranges (`I2:I` not `I2:I1000`). Bounded ranges create phantom rows that break the appendRow flow.

## Setup steps

1. Create a new Google Sheet
2. Name the first sheet tab "Training Tracker"
3. In row 1, paste the headers from the table above (or any equivalent labels — the Apps Script writes by column position, not header name)
4. In cell **O2**, paste the Next Due formula
5. In cell **P2**, paste the Status formula
6. Optional: format column A as datetime, column I as date, column O as date, column R as a clickable link

## Conditional formatting (recommended)

Apply to column P:

- "Overdue" — red background, bold text
- "Due Soon" — yellow background
- "Current" — green background

Makes the dashboard instantly scannable for the security team.

## Why these columns?

The schema is designed for what auditors actually ask for:

- **Who completed it** (B, C, D)
- **What role they hold** (E, F, G) — relevant for AT-3 privileged-user controls
- **When they completed it** (A, I) and **what version** (J) — for audit-period queries
- **What they acknowledged** (K, L, M) — the PRS itself, the signature, and the literal text they signed
- **When they need to recertify** (O) and **whether they're current** (P) — for compliance dashboards
- **Where the certificate lives** (R) — so an auditor can verify the artifact exists
- **Supervisor escalation path** (H) — for automated reminders to supervisors
- **User satisfaction signal** (N) — for continuous improvement

## Querying the tracker for audits

Common audit queries:

**"Show me all employees with FTI access who completed training in the last 12 months."**
```
=QUERY(A:R, "SELECT B, C, D, E, I WHERE G='Yes' AND I > date '"&TEXT(TODAY()-365,"yyyy-mm-dd")&"' ORDER BY I DESC", 1)
```

**"Show me everyone currently overdue."**
```
=QUERY(A:R, "SELECT B, C, D, E, O, H WHERE P='Overdue' ORDER BY O ASC", 1)
```

**"Completion rate this calendar year."**
```
=COUNTIFS(I:I,">="&DATE(YEAR(TODAY()),1,1)) / [your headcount]
```

These can be turned into a separate "Dashboard" tab for at-a-glance reporting.
