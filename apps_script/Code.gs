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

const PRS_STATEMENTS = [
  'I have completed the ' + CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training and reviewed the requirements for safeguarding PII, FTI, PHI, and SSA data.',
  'I have been advised of the Privacy Act of 1974, applicable state privacy laws, HIPAA, IRS Publication 1075, and Internal Revenue Code §§ 6103, 7213, 7213A, and 7431.',
  'I will not access, use, or disclose sensitive data except as authorized by my role and required to perform my official duties.',
  'My access to sensitive systems is conditional on completing annual recertification, and I will report any suspected incident to the Information Security Office promptly.',
  'I understand that this acknowledgment is retained as part of the agency\'s safeguard records and may be reviewed during federal and state audits.'
];


// ============================================================================
// WEB APP ENTRY POINT
// ============================================================================

function doGet(e) {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle(CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}


// ============================================================================
// IDENTITY
// ============================================================================

function getUserEmail() {
  try {
    const email = Session.getActiveUser().getEmail();
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
    const userEmail = Session.getActiveUser().getEmail();
    if (!userEmail) {
      throw new Error('Identity verification failed. Please refresh and sign in again.');
    }

    const required = ['firstName', 'lastName', 'role', 'sensitive', 'fti', 'supervisorEmail', 'signature'];
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
      formData.sensitive,                   // F: Handles sensitive data?
      formData.fti,                         // G: FTI access?
      formData.supervisorEmail,             // H: Supervisor email
      now,                                  // I: Training date
      CONFIG.TRAINING_VERSION,              // J: Version
      'Acknowledged',                       // K: Confirmation
      PRS_STATEMENTS.join(' | '),           // L: PRS text
      formData.signature,                   // M: Signature
      formData.rating || '',                // N: Rating (optional)
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
    '<p class="cert-body-text">has successfully completed the <strong>' + CONFIG.AGENCY_NAME + ' Annual Sensitive Data Training (v' + CONFIG.TRAINING_VERSION + ')</strong>, in accordance with applicable federal and state requirements including the Privacy Act of 1974, applicable state privacy laws, HIPAA, and IRS Publication 1075. The recipient has signed the Personal Responsibility Statement and is authorized to handle sensitive information consistent with their assigned role.</p>' +
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
    sensitive: 'Yes',
    fti: 'No',
    supervisorEmail: 'supervisor@your-agency.gov',
    signature: 'Test User',
    rating: '5',
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
