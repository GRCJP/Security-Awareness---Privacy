/**
 * Sensitive Data Training - Server Logic
 *
 * Generic Apps Script template for an annual security awareness training that
 * tracks completion, generates PDF certificates, and emails confirmations.
 *
 * Customize the CONFIG block below for your organization. See CONFIG.md.
 */

const CONFIG = {
  AGENCY_NAME: 'Your Agency',                     // shown throughout the UI and on certificates
  TRAINING_VERSION: '2026.1',                     // bump when content materially changes
  RECERTIFICATION_DAYS: 365,                      // length of the recertification cycle
  SECURITY_CONTACT: 'security@your-agency.gov',   // shown for incident reporting and tech support
  CERTIFICATES_FOLDER_ID: 'PASTE_DRIVE_FOLDER_ID_HERE',  // Drive folder where PDF certificates are archived
  CERTIFICATE_SIGNATURE_LINE: 'Information Security Office',  // appears at the bottom of each certificate
  ISSUING_AUTHORITY: 'Information Security Office'  // shown in the certificate footer "Issuing Authority" card
};

// ============================================================================
// TEST MODE — DEVELOPMENT / DEMO ONLY
// ============================================================================
// Set TEST_MODE.enabled = true to allow form submission on personal Gmail accounts
// or in any context where Session.getActiveUser().getEmail() returns empty.
//
// In production, this MUST be set to false. Workspace SSO is what makes identity
// capture trustworthy for compliance use. Allowing a fake email in production
// breaks the audit trail and defeats the entire point of the system.
//
// When TEST_MODE.enabled is true, the script will use TEST_MODE.fallbackEmail
// for any caller whose Workspace identity cannot be verified.
//
// Use cases for TEST_MODE:
//   - Demo deployments on personal Gmail
//   - Local testing while building out the rest of the system
//   - Recording portfolio screenshots without a Workspace subscription
//
// REMOVE OR DISABLE BEFORE ANY REAL ROLLOUT.
const TEST_MODE = {
  enabled: false,
  fallbackEmail: 'test@your-agency.gov'
};

function resolveUserEmail() {
  let email = '';
  try {
    email = Session.getActiveUser().getEmail() || '';
  } catch (e) {
    // Session unavailable in some contexts; fall through.
  }
  if (!email && TEST_MODE.enabled) {
    return TEST_MODE.fallbackEmail;
  }
  return email;
}

const PRS_STATEMENTS = [
  'I have completed the ' + CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training and reviewed the requirements for safeguarding the categories of regulated data I handle in my role.',
  'I have been advised of the federal and state laws applicable to my access — which may include the Privacy Act of 1974, applicable state privacy laws, HIPAA Security Rule, and any sector-specific frameworks (tax data, healthcare, criminal justice, education records, or controlled unclassified information) governing the data I handle.',
  'I will not access, use, or disclose sensitive data except as authorized by my role and required to perform my official duties.',
  'My access to sensitive systems is conditional on completing annual recertification, and I will report any suspected incident to the Information Security Office promptly.',
  'I understand that this acknowledgment is retained as part of the agency\'s safeguard records and may be reviewed during federal and state audits.'
];

// CUSTOMIZATION NOTE:
// If your agency handles regulated data under a specific framework (IRS Pub 1075,
// CJIS Security Policy, FERPA, HIPAA, FedRAMP, etc.), edit the PRS_STATEMENTS above
// to reference the specific statute or framework that applies. Auditors look for the
// PRS to explicitly cite the framework the user is being held accountable to.


// ============================================================================
// WEB APP ENTRY POINT
// ============================================================================

function doGet(e) {
  const template = HtmlService.createTemplateFromFile('Index');

  // Populate all template scriptlets used in Index.html.
  const userEmail = resolveUserEmail();
  template.userEmail = userEmail;
  template.prsAcknowledgments = PRS_STATEMENTS;

  // Look up most recent completion for this user, if any.
  const priorCompletion = lookupLastCompletion(userEmail);
  template.alreadyCompleted = priorCompletion !== null;
  template.lastCompletion = priorCompletion || { trainingDate: '', version: '', nextDue: '' };

  return template
    .evaluate()
    .setTitle(CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/**
 * Look up the most recent completion record for a given user.
 * Returns { trainingDate, version, nextDue } or null if no record found.
 *
 * Reads from the bound spreadsheet's first sheet. Expects the schema documented
 * in docs/SHEET_SCHEMA.md (B=email, I=training date, J=version, O=next due).
 *
 * If the script isn't bound to a spreadsheet (e.g., during local Apps Script
 * testing without a sheet), returns null silently.
 */
function lookupLastCompletion(userEmail) {
  if (!userEmail) return null;

  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) return null;

    const sheet = ss.getSheetByName('Training Tracker') || ss.getSheets()[0];
    if (!sheet) return null;

    const lastRow = sheet.getLastRow();
    if (lastRow < 2) return null;  // header only, no data

    // Pull columns A through R for all data rows
    const data = sheet.getRange(2, 1, lastRow - 1, 18).getValues();

    // Walk rows latest-first, find the most recent record for this email
    const targetEmail = String(userEmail).toLowerCase().trim();
    for (let i = data.length - 1; i >= 0; i--) {
      const rowEmail = String(data[i][1] || '').toLowerCase().trim();
      if (rowEmail !== targetEmail) continue;

      const trainingDate = data[i][8];   // column I
      const version = data[i][9];        // column J
      const nextDue = data[i][14];       // column O

      return {
        trainingDate: formatDateForDisplay(trainingDate),
        version: String(version || ''),
        nextDue: formatDateForDisplay(nextDue)
      };
    }
    return null;
  } catch (err) {
    // Don't block the page render on lookup failure.
    Logger.log('lookupLastCompletion failed: ' + err.message);
    return null;
  }
}

function formatDateForDisplay(d) {
  if (!d) return '';
  if (d instanceof Date) {
    return Utilities.formatDate(d, Session.getScriptTimeZone(), 'MMMM d, yyyy');
  }
  return String(d);
}

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}


// ============================================================================
// IDENTITY
// ============================================================================

function getUserEmail() {
  try {
    const email = resolveUserEmail();
    if (!email) {
      return { success: false, error: 'Could not verify your Workspace identity. Please sign in with your organization account.' };
    }
    return { success: true, email: email };
  } catch (err) {
    return { success: false, error: 'Identity check failed: ' + err.message };
  }
}


// ============================================================================
// SUBMISSION HANDLER
// ============================================================================

function submitTraining(formData) {
  try {
    const userEmail = resolveUserEmail();
    if (!userEmail) {
      throw new Error('Identity verification failed. Please refresh and sign in again with a Google Workspace account, or enable TEST_MODE in Code.gs for local testing.');
    }

    const required = ['firstName', 'lastName', 'role', 'sensitiveDataAccess', 'ftiAccess', 'supervisorEmail', 'signature'];
    for (let i = 0; i < required.length; i++) {
      if (!formData[required[i]] || String(formData[required[i]]).trim() === '') {
        throw new Error('Missing required field: ' + required[i]);
      }
    }

    const fullName = (formData.firstName + ' ' + formData.lastName).trim().toLowerCase();
    const sig = (formData.signature || '').trim().toLowerCase();
    if (sig !== fullName) {
      throw new Error('Signature must exactly match your typed name (case-insensitive).');
    }

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Training Tracker') ||
                  SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];

    const now = new Date();
    const datePrefix = Utilities.formatDate(now, 'GMT', 'yyyyMMdd');
    const emailPrefix = userEmail.split('@')[0].replace(/[^a-z0-9]/gi, '');
    const certificateId = 'CERT-' + emailPrefix + '-' + datePrefix;

    const certUrl = generateCertificatePdf(formData, userEmail, certificateId, now);

    sheet.appendRow([
      now,                                  // A: Timestamp
      userEmail,                            // B: Email
      formData.firstName,                   // C: First Name
      formData.lastName,                    // D: Last Name
      formData.role,                        // E: Role
      formData.sensitiveDataAccess,         // F: Handles sensitive data?
      formData.ftiAccess,                   // G: FTI access?
      formData.supervisorEmail,             // H: Supervisor email
      now,                                  // I: Training date
      CONFIG.TRAINING_VERSION,              // J: Version
      'Acknowledged',                       // K: Confirmation
      PRS_STATEMENTS.join(' | '),           // L: PRS text
      formData.signature,                   // M: Signature
      formData.qualityRating || '',         // N: Rating (optional)
      '',                                   // O: Next due (formula in sheet)
      '',                                   // P: Status (formula in sheet)
      formData.notes || '',                 // Q: Notes
      certUrl                               // R: Certificate URL
    ]);

    sendCompletionEmail(userEmail, formData, certificateId, certUrl, now);

    return { success: true, certificateId: certificateId, certUrl: certUrl };
  } catch (err) {
    return { success: false, error: err.message };
  }
}


// ============================================================================
// CERTIFICATE GENERATION
// ============================================================================

/**
 * Generic shield SVG used as the certificate header. Replace with your
 * agency's logo for production. Keep dimensions ~80x96.
 */
function buildAgencyShieldSvg() {
  return '<svg viewBox="0 0 80 96" xmlns="http://www.w3.org/2000/svg" width="80" height="96">' +
    '<path d="M40 4 L72 16 L72 48 Q72 80 40 92 Q8 80 8 48 L8 16 Z" fill="#1F2630" stroke="#C9966B" stroke-width="2"/>' +
    '<path d="M28 48 L36 56 L52 36" fill="none" stroke="#C9966B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';
}

function buildCertificateHtml(formData, userEmail, certificateId, completionDate) {
  const fullName = formData.firstName + ' ' + formData.lastName;
  const dateStr = Utilities.formatDate(completionDate, Session.getScriptTimeZone(), 'MMMM d, yyyy');
  const expDate = new Date(completionDate.getTime() + (CONFIG.RECERTIFICATION_DAYS * 86400000));
  const expDateStr = Utilities.formatDate(expDate, Session.getScriptTimeZone(), 'MMMM d, yyyy');

  return '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>' +
    '@page { size: letter; margin: 0.5in; }' +
    'body { font-family: Georgia, "Times New Roman", serif; color: #1F2630; padding: 0; margin: 0; background: #FFFFFF; }' +
    '.cert-frame { border: 4px double #C9966B; padding: 36px 48px; min-height: 9in; position: relative; }' +
    '.cert-shield { text-align: center; margin-bottom: 16px; }' +
    '.cert-eyebrow { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 11px; letter-spacing: 0.3em; text-transform: uppercase; color: #A87A52; font-weight: 700; text-align: center; margin-bottom: 8px; }' +
    '.cert-title { text-align: center; font-size: 36px; font-weight: 700; color: #1F2630; margin: 0 0 16px; letter-spacing: -0.01em; }' +
    '.cert-divider { width: 80px; height: 3px; background: #C9966B; margin: 12px auto 32px; }' +
    '.cert-recipient-label { text-align: center; font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 12px; letter-spacing: 0.2em; text-transform: uppercase; color: #6B6E73; margin-bottom: 8px; }' +
    '.cert-recipient { text-align: center; font-size: 32px; font-weight: 700; color: #1F2630; margin: 0 0 36px; }' +
    '.cert-body-text { font-size: 15px; line-height: 1.7; color: #1F2630; margin: 0 0 16px; text-align: justify; }' +
    '.cert-footer-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 36px; padding-top: 24px; border-top: 1px solid #E8E1D1; }' +
    '.cert-footer-card { background: #F5F0EA; border-radius: 6px; padding: 14px 16px; text-align: center; }' +
    '.cert-footer-label { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase; color: #A87A52; font-weight: 700; margin-bottom: 6px; }' +
    '.cert-footer-value { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 12px; color: #1F2630; font-weight: 600; }' +
    '.cert-signature { margin-top: 36px; text-align: center; font-style: italic; font-size: 13px; color: #6B6E73; }' +
    '</style></head><body>' +
    '<div class="cert-frame">' +
    '<div class="cert-shield">' + buildAgencyShieldSvg() + '</div>' +
    '<div class="cert-eyebrow">Certificate of Completion</div>' +
    '<h1 class="cert-title">Annual Sensitive Data Training</h1>' +
    '<div class="cert-divider"></div>' +
    '<div class="cert-recipient-label">Awarded To</div>' +
    '<h2 class="cert-recipient">' + fullName + '</h2>' +
    '<p class="cert-body-text">has successfully completed the <strong>' + CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training (v' + CONFIG.TRAINING_VERSION + ')</strong>, in accordance with applicable federal and state safeguarding requirements, including NIST 800-53 Awareness and Training (AT) family controls and the sector-specific frameworks governing the data the recipient handles. The recipient has signed the Personal Responsibility Statement and is authorized to handle sensitive information consistent with their assigned role.</p>' +
    '<div class="cert-footer-grid">' +
    '<div class="cert-footer-card"><div class="cert-footer-label">Certificate ID</div><div class="cert-footer-value">' + certificateId + '</div></div>' +
    '<div class="cert-footer-card"><div class="cert-footer-label">Completion Date</div><div class="cert-footer-value">' + dateStr + '</div></div>' +
    '<div class="cert-footer-card"><div class="cert-footer-label">Valid Through</div><div class="cert-footer-value">' + expDateStr + '</div></div>' +
    '</div>' +
    '<div class="cert-signature">Issued by ' + CONFIG.ISSUING_AUTHORITY + '</div>' +
    '</div></body></html>';
}

function generateCertificatePdf(formData, userEmail, certificateId, completionDate) {
  const html = buildCertificateHtml(formData, userEmail, certificateId, completionDate);
  const blob = Utilities.newBlob(html, 'text/html', certificateId + '.html').getAs('application/pdf');
  blob.setName(certificateId + '.pdf');

  const folder = DriveApp.getFolderById(CONFIG.CERTIFICATES_FOLDER_ID);
  const file = folder.createFile(blob);
  file.setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE);
  return file.getUrl();
}


// ============================================================================
// EMAIL
// ============================================================================

function sendCompletionEmail(userEmail, formData, certificateId, certUrl, completionDate) {
  const dateStr = Utilities.formatDate(completionDate, Session.getScriptTimeZone(), 'MMMM d, yyyy');
  const expDate = new Date(completionDate.getTime() + (CONFIG.RECERTIFICATION_DAYS * 86400000));
  const expDateStr = Utilities.formatDate(expDate, Session.getScriptTimeZone(), 'MMMM d, yyyy');

  const subject = 'Training Completion Confirmation — ' + CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training (' + CONFIG.TRAINING_VERSION + ')';

  let body = 'Hello ' + formData.firstName + ',\n\n';
  body += 'This confirms that you have completed the ' + CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training.\n\n';
  body += 'Certificate ID: ' + certificateId + '\n';
  body += 'Completion Date: ' + dateStr + '\n';
  body += 'Recertification Required By: ' + expDateStr + '\n\n';
  body += 'Your certificate is attached to this email and archived for audit purposes at:\n' + certUrl + '\n\n';
  body += 'Your Personal Responsibility Statement is on file as part of the agency\'s safeguard records.\n\n';
  body += 'Questions or concerns about sensitive data handling should be directed to ' + CONFIG.SECURITY_CONTACT + '.\n\n';
  body += 'Thank you,\n' + CONFIG.ISSUING_AUTHORITY;

  let attachment = null;
  try {
    const html = buildCertificateHtml(formData, userEmail, certificateId, completionDate);
    attachment = Utilities.newBlob(html, 'text/html', certificateId + '.html').getAs('application/pdf');
    attachment.setName(certificateId + '.pdf');
  } catch (e) {
    // If attachment fails, still send the email with the link
  }

  const options = { name: CONFIG.AGENCY_NAME + ' Information Security' };
  if (attachment) options.attachments = [attachment];

  MailApp.sendEmail(userEmail, subject, body, options);
}


// ============================================================================
// TEST HARNESS
// ============================================================================

/**
 * Run from the Apps Script editor to verify certificate generation and email
 * delivery before going live. Uses fake data; does not write to the tracker.
 */
function testCertificateGeneration() {
  const fakeFormData = {
    firstName: 'Test',
    lastName: 'User',
    role: 'Developer',
    sensitiveDataAccess: 'Yes',
    ftiAccess: 'No',
    supervisorEmail: 'supervisor@your-agency.gov',
    signature: 'Test User',
    qualityRating: '5',
    notes: 'Test run from script editor'
  };

  const fakeUserEmail = 'test@your-agency.gov';
  const fakeCertId = 'CERT-test-' + Utilities.formatDate(new Date(), 'GMT', 'yyyyMMdd');
  const now = new Date();

  const url = generateCertificatePdf(fakeFormData, fakeUserEmail, fakeCertId, now);
  Logger.log('Certificate generated at: ' + url);

  sendCompletionEmail(Session.getActiveUser().getEmail(), fakeFormData, fakeCertId, url, now);
  Logger.log('Test email sent to: ' + Session.getActiveUser().getEmail());
}
