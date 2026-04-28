# Configuration Guide

This guide walks through what to edit to brand the training for your agency.

## Quick reference: the two CONFIG blocks

There are two `CONFIG` blocks you'll edit. Both are at the top of their respective files.

### `apps_script/Code.gs` — runtime config

Controls server-side behavior: what gets written to the sheet, what the email says, what's on the certificate.

```javascript
const CONFIG = {
  AGENCY_NAME: 'Your Agency',                                  // [1]
  TRAINING_VERSION: '2026.1',                                  // [2]
  RECERTIFICATION_DAYS: 365,                                   // [3]
  SECURITY_CONTACT: 'security@your-agency.gov',                // [4]
  CERTIFICATES_FOLDER_ID: 'PASTE_DRIVE_FOLDER_ID_HERE',        // [5]
  CERTIFICATE_SIGNATURE_LINE: 'Information Security Office',   // [6]
  ISSUING_AUTHORITY: 'Information Security Office'             // [7]
};
```

### `apps_script/_build_index.py` — UI config

Controls UI text shown to users. Edit, then run `python3 _build_index.py` to regenerate `Index.html`.

```python
CONFIG = {
    'AGENCY_NAME': 'Your Agency',                           # [1]
    'TRAINING_VERSION': '2026.1',                           # [2]
    'SECURITY_CONTACT': 'security@your-agency.gov',         # [4]
    'RECERTIFICATION_DAYS': 365,                            # [3]
}
```

The two blocks should match — `AGENCY_NAME` should be the same in both places, etc.

---

## Field reference

### [1] AGENCY_NAME
Your agency's full display name. Appears in:
- Page title (browser tab)
- Header bar throughout the training
- Welcome screen subtitle
- Throughout module text wherever the agency is referenced
- Email subject line and body
- Certificate body text

Examples: `Department of Health Services`, `City of Springfield IT Department`, `Acme Insurance`.

### [2] TRAINING_VERSION
The current version of your training content. Bump this whenever you make material changes to the training so completions are tied to a specific version.

Convention: `YYYY.N` where `N` increments per release within a year. Example: `2026.1`, `2026.2`.

Appears in: certificate footer, tracker sheet column J, email subject line, email body.

### [3] RECERTIFICATION_DAYS
How long a completion is valid before the user needs to recertify. Standard is `365` (annual). Some frameworks require shorter cycles (e.g., 180 days for high-risk roles).

Appears in: certificate "Valid Through" date, tracker sheet "Next Due" formula.

### [4] SECURITY_CONTACT
Email address for incident reporting and tech support. Shown to users throughout the training and in confirmation emails.

Use a shared mailbox if possible (e.g., `security@agency.gov` rather than an individual's address). The email shouldn't break when one person leaves.

### [5] CERTIFICATES_FOLDER_ID
Drive folder ID where PDF certificates get archived.

To find: open the folder in Drive and look at the URL. It'll look like:
```
https://drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I0J
```
The ID is the last segment: `1A2B3C4D5E6F7G8H9I0J`.

### [6] CERTIFICATE_SIGNATURE_LINE
Text shown at the bottom of each certificate (e.g., "Issued by [...]"). Usually your information security office or compliance team.

### [7] ISSUING_AUTHORITY
Shown in the certificate footer's "Issuing Authority" card. Often the same as `CERTIFICATE_SIGNATURE_LINE`.

---

## Branding beyond the CONFIG block

A few branding elements live outside the CONFIG dict:

### Agency logo
The header logo is loaded from a base64 data URI in `_build_index.py`:

```python
LOGO_DATA_URI = 'data:image/svg+xml;base64,...'
```

To use your agency's logo:

1. Get your logo as an SVG, PNG, or JPEG (~80x80 pixels, square works best)
2. Convert to base64:
   ```bash
   base64 -i your_logo.svg -o your_logo_b64.txt
   ```
3. Replace the `LOGO_DATA_URI` value with the contents (prefixed with `data:image/svg+xml;base64,` for SVG or `data:image/png;base64,` for PNG)
4. Re-run `python3 _build_index.py`

### Hero photo (Welcome screen)
By default the Welcome screen uses an SVG cityscape silhouette as the hero background. To use a real photo of your agency's location, headquarters, or a relevant scene:

1. Get a wide photo (~2000x800 pixels)
2. Convert to base64:
   ```bash
   base64 -i your_photo.jpg -o your_photo_b64.txt
   ```
3. In `_build_index.py`, replace `BALTIMORE_SKYLINE_DATA_URI = ''` with the contents (prefixed with `data:image/jpeg;base64,`)
4. Re-run `python3 _build_index.py`

### Color palette
The default palette is navy/cream/tan with red/yellow accent colors. To change:

Edit the CSS variables at the top of `apps_script/Stylesheet.html`:

```css
:root {
  --navy: #1F2630;
  --slate: #3D4A5B;
  --cream: #F5F0EA;
  --beige: #EDE5D8;
  --tan: #C9966B;
  --tan-dark: #A87A52;
  --tan-light: #E5C7A3;
  --success: #4A7C59;
  --alert: #A94442;
  /* ... */
}
```

The palette is used consistently throughout. Changing these variables propagates everywhere.

### Typography
The training uses system fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, ...`) for body text and Georgia serif for the certificate. To use your agency's brand fonts, swap the `font-family` in `Stylesheet.html`.

---

## Content customization

For changes beyond branding (different modules, different scenarios, different PRS), see `docs/CONTENT_GUIDE.md`.

---

## Re-deploying after changes

After making any changes to `Code.gs`, `Index.html`, `Stylesheet.html`, or `JavaScript.html`:

1. Paste the updated files into the Apps Script editor
2. **Deploy → Manage deployments → (your deployment) → Edit → New version → Deploy**

Users hitting the deployment URL will get the new version on their next page load.
