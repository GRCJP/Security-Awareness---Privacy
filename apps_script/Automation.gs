/**
 * Automation.gs - Optional time-based triggers that complete the recertification flywheel.
 *
 * Add this file to your Apps Script project alongside Code.gs, then schedule the
 * trigger functions via Apps Script's Triggers panel:
 *
 *   sendReminderEmails       → Daily, 6am
 *   escalateOverdueStaff     → Daily, 7am
 *   sendQuarterlyReport      → Monthly trigger; the function self-checks for first Monday of quarter
 *   backupTracker            → Weekly, Sunday 1am
 *
 * Each function is idempotent and safe to run repeatedly.
 */

const AUTOMATION_CONFIG = {
  REMINDER_DAYS: [30, 14, 7, 1],          // days before Next Due to send a reminder
  SUPERVISOR_ESCALATION_DAYS: 7,           // days overdue before notifying supervisor
  BACKUP_FOLDER_ID: 'PASTE_BACKUP_FOLDER_ID_HERE',  // Drive folder for tracker backups
  REPORT_RECIPIENTS: ['security-leadership@your-agency.gov']  // quarterly report recipients
};


// ============================================================================
// REMINDER EMAILS (daily trigger at 6am)
// ============================================================================

/**
 * Scans the tracker for users approaching their Next Due date.
 * Emails users at 30, 14, 7, and 1 days before recertification.
 */
function sendReminderEmails() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = sheet.getDataRange().getValues();
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let sent = 0;
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const email = row[1];
    const firstName = row[2];
    const nextDue = row[14];  // column O
    const status = row[15];   // column P

    if (!nextDue || !email || status === 'Overdue') continue;

    const due = new Date(nextDue);
    due.setHours(0, 0, 0, 0);
    const daysUntilDue = Math.round((due - today) / 86400000);

    if (AUTOMATION_CONFIG.REMINDER_DAYS.indexOf(daysUntilDue) === -1) continue;

    sendReminderEmail(email, firstName, due, daysUntilDue);
    sent++;
  }

  Logger.log('Reminder emails sent: ' + sent);
}

function sendReminderEmail(email, firstName, dueDate, daysUntilDue) {
  const dueStr = Utilities.formatDate(dueDate, Session.getScriptTimeZone(), 'MMMM d, yyyy');
  const subject = 'Reminder: Annual Sensitive Data Training due in ' + daysUntilDue + ' day' + (daysUntilDue === 1 ? '' : 's');

  let body = 'Hello ' + firstName + ',\n\n';
  body += 'Your annual sensitive data training expires on ' + dueStr + '. ';
  body += 'You have ' + daysUntilDue + ' day' + (daysUntilDue === 1 ? '' : 's') + ' remaining to recertify.\n\n';
  body += 'The training takes about 20 minutes. Recertify here:\n';
  body += getTrainingUrl() + '\n\n';
  body += 'Failure to recertify by your due date will result in your status changing to Overdue, ';
  body += 'and your supervisor will be notified after 7 days.\n\n';
  body += 'Questions? Contact ' + CONFIG.SECURITY_CONTACT + '\n\n';
  body += 'Thank you,\n' + CONFIG.ISSUING_AUTHORITY;

  MailApp.sendEmail(email, subject, body, {
    name: CONFIG.AGENCY_NAME + ' Information Security'
  });
}


// ============================================================================
// SUPERVISOR ESCALATION (daily trigger at 7am)
// ============================================================================

/**
 * Notifies supervisors of staff who are more than 7 days overdue.
 * Re-sends weekly to the same supervisor while the staff member remains overdue.
 */
function escalateOverdueStaff() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = sheet.getDataRange().getValues();
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let escalated = 0;
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const email = row[1];
    const firstName = row[2];
    const lastName = row[3];
    const role = row[4];
    const supervisorEmail = row[7];
    const nextDue = row[14];
    const status = row[15];

    if (status !== 'Overdue' || !supervisorEmail) continue;

    const due = new Date(nextDue);
    due.setHours(0, 0, 0, 0);
    const daysOverdue = Math.round((today - due) / 86400000);

    // Escalate at 7 days overdue, then re-escalate every 7 days
    if (daysOverdue < AUTOMATION_CONFIG.SUPERVISOR_ESCALATION_DAYS) continue;
    if (daysOverdue % 7 !== 0) continue;

    sendSupervisorEscalation(supervisorEmail, firstName, lastName, email, role, daysOverdue);
    escalated++;
  }

  Logger.log('Supervisor escalations sent: ' + escalated);
}

function sendSupervisorEscalation(supervisorEmail, firstName, lastName, userEmail, role, daysOverdue) {
  const subject = 'Action Required: ' + firstName + ' ' + lastName + ' is ' + daysOverdue + ' days overdue on annual training';

  let body = 'Hello,\n\n';
  body += firstName + ' ' + lastName + ' (' + userEmail + ', ' + role + ') is ' + daysOverdue;
  body += ' days overdue on the annual sensitive data training.\n\n';
  body += 'Continued non-compliance may require suspension of access to systems containing sensitive data.\n\n';
  body += 'Please ensure they complete the training as soon as possible:\n';
  body += getTrainingUrl() + '\n\n';
  body += 'You are receiving this notice because you are listed as their supervisor in our records. ';
  body += 'If this is incorrect, contact ' + CONFIG.SECURITY_CONTACT + '\n\n';
  body += 'Thank you,\n' + CONFIG.ISSUING_AUTHORITY;

  MailApp.sendEmail(supervisorEmail, subject, body, {
    name: CONFIG.AGENCY_NAME + ' Information Security',
    cc: CONFIG.SECURITY_CONTACT
  });
}


// ============================================================================
// QUARTERLY STATUS REPORT (monthly trigger; self-checks for first Monday of quarter)
// ============================================================================

/**
 * On the first Monday of each quarter, emails leadership a compliance summary.
 */
function sendQuarterlyReport() {
  const today = new Date();
  const isQuarterStart = (today.getMonth() % 3 === 0) &&
                          (today.getDate() <= 7) &&
                          (today.getDay() === 1);
  if (!isQuarterStart) return;

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = sheet.getDataRange().getValues();

  let total = 0, current = 0, dueSoon = 0, overdue = 0;
  const overdueList = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row[1]) continue;  // skip empty rows

    total++;
    const status = row[15];
    if (status === 'Current') current++;
    else if (status === 'Due Soon') dueSoon++;
    else if (status === 'Overdue') {
      overdue++;
      overdueList.push(row[2] + ' ' + row[3] + ' (' + row[1] + ')');
    }
  }

  const completionRate = total > 0 ? Math.round((current / total) * 100) : 0;
  const subject = 'Quarterly Training Compliance Report — ' + Utilities.formatDate(today, Session.getScriptTimeZone(), 'MMMM yyyy');

  let body = 'Quarterly compliance summary for the annual sensitive data training.\n\n';
  body += '=== SUMMARY ===\n';
  body += 'Total tracked staff: ' + total + '\n';
  body += 'Current: ' + current + ' (' + completionRate + '%)\n';
  body += 'Due Soon (within 30 days): ' + dueSoon + '\n';
  body += 'Overdue: ' + overdue + '\n\n';

  if (overdueList.length > 0) {
    body += '=== OVERDUE STAFF ===\n';
    body += overdueList.join('\n') + '\n\n';
  }

  body += 'Live tracker: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl() + '\n\n';
  body += 'Generated by ' + CONFIG.AGENCY_NAME + ' training automation\n';

  MailApp.sendEmail({
    to: AUTOMATION_CONFIG.REPORT_RECIPIENTS.join(','),
    subject: subject,
    body: body,
    name: CONFIG.AGENCY_NAME + ' Information Security'
  });

  Logger.log('Quarterly report sent. Completion rate: ' + completionRate + '%');
}


// ============================================================================
// WEEKLY TRACKER BACKUP (Sunday 1am)
// ============================================================================

/**
 * Copies the entire tracker spreadsheet to a date-stamped folder in Drive.
 * Audit insurance against accidental deletion or corruption.
 */
function backupTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const file = DriveApp.getFileById(ss.getId());
  const backupFolder = DriveApp.getFolderById(AUTOMATION_CONFIG.BACKUP_FOLDER_ID);
  const dateStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
  const backupName = ss.getName() + ' - Backup ' + dateStr;

  file.makeCopy(backupName, backupFolder);
  Logger.log('Tracker backed up: ' + backupName);
}


// ============================================================================
// HELPERS
// ============================================================================

function getTrainingUrl() {
  // Replace with your deployed web app URL or your Site URL
  return 'https://sites.google.com/your-domain/sensitive-data-training';
}
