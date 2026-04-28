# Training Content Draft: (anonymous)

**Source:** `sample_pub1075_excerpt.pdf` (PDF, 3 pages/slides)
**Sections extracted:** 18

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

## Module: Foundations

### 1.0 INTRODUCTION
*Source: page/slide 1*

---

## Module: Handling

### PUBLICATION 1075 EXCERPT — TAX INFORMATION SECURITY
*Source: page/slide 1*

GUIDELINES This is a representative excerpt for testing content extraction. The actual IRS Publication 1075 is freely available at irs.gov/pub/irs-pdf/p1075.pdf.

  ### 1.1 General
  *Source: page/slide 1*

  Federal, state, and local agencies that receive Federal Tax Information (FTI) are required to safeguard that information in accordance with Internal Revenue Code section 6103. This publication describes the safeguards required of agencies receiving FTI.

  Agencies must implement administrative, physical, and technical safeguards designed to protect the confidentiality of FTI. Failure to maintain adequate safeguards may result in suspension or termination of FTI access.

  ### 1.2 Overview of Publication 1075
  *Source: page/slide 1*

  Publication 1075 establishes the safeguarding requirements for agencies that receive FTI. The publication addresses requirements in the following areas:

   Recordkeeping requirements  Secure storage of FTI  Restricting access to authorized personnel  Reporting safeguard activities to the IRS  Disposing of FTI when no longer needed  Computer system security requirements

  ### 2.1 Federal Tax Information Logs
  *Source: page/slide 1*

  Agencies must maintain logs documenting the receipt, use, and disposition of all FTI received. Logs must capture: the date FTI was requested and received; the taxpayer identifier; tax year(s) covered;

  type of information; reason for the request; the exact location where the FTI is stored; who has access to the FTI; the disposition date; and the disposition method.

### 3.0 RESTRICTING ACCESS TO FTI
*Source: page/slide 1*

  ### 3.1 Need to Know
  *Source: page/slide 1*

  Access to FTI must be restricted to those agency employees and contractors who require access to perform their official duties. The principle of least privilege must be applied — employees should have access only to the specific FTI required for their assigned tasks.

  ### 3.2 Background Investigations
  *Source: page/slide 2*

  All agency personnel with access to FTI must undergo background investigations consistent with the sensitivity of the information they will access. Contractors granted access to FTI are subject to the same background investigation requirements as agency employees.

### 5.0 DISPOSAL OF FTI
*Source: page/slide 2*

  ### 5.1 Approved Methods
  *Source: page/slide 2*

  FTI must be disposed of in a manner that prevents reconstruction. Approved methods for paper FTI include: shredding using crosscut or microcut shredders; pulping; burning to white ash; or chemical decomposition. Approved methods for digital FTI follow NIST Special Publication 800-88 guidelines for media sanitization.

---

## Module: Consequences

  ### 4.1 Annual Training Requirement
  *Source: page/slide 2*

  Each agency must provide annual security awareness training to all employees and contractors with access to FTI. Training must address: the requirements of IRC section 6103; civil and criminal penalties for unauthorized disclosure under IRC sections 7213, 7213A, and 7431; agency-specific procedures for safeguarding FTI; and the requirement to report any suspected unauthorized access or disclosure.

### 6.0 PENALTIES FOR UNAUTHORIZED DISCLOSURE
*Source: page/slide 2*

  ### 6.1 IRC Section 7213
  *Source: page/slide 2*

  Unauthorized disclosure of FTI by federal employees, state employees, or contractors is a felony punishable by a fine of up to five thousand dollars, imprisonment of up to five years, or both, plus the costs of prosecution. Conviction also results in dismissal from federal employment.

  ### 6.2 IRC Section 7213A
  *Source: page/slide 2*

  Unauthorized inspection of returns or return information is a misdemeanor punishable by a fine of up to one thousand dollars, imprisonment of up to one year, or both, plus the costs of prosecution.

  ### 6.3 IRC Section 7431
  *Source: page/slide 3*

  Taxpayers may bring a civil action against any person who knowingly or by reason of negligence inspects or discloses any return or return information. The minimum civil damages are one thousand dollars per act of unauthorized inspection or disclosure, or actual damages plus punitive damages if the violation was willful.

---

## Module: Acknowledgment

  ### 4.2 Personal Responsibility Statement
  *Source: page/slide 2*

  Each employee and contractor with access to FTI must sign a Personal Responsibility Statement (PRS) annually. The PRS must affirm that the individual has completed the required training and understands their obligations regarding the safeguarding of FTI.

---

## Module: Unmapped

*These sections didn't strongly match any module. Review manually.*

### 2.0 RECORDKEEPING REQUIREMENTS
*Source: page/slide 1*

### 4.0 EMPLOYEE AWARENESS AND TRAINING
*Source: page/slide 2*

---

## Detected Legal References

The source document references the following frameworks. Make sure your
Personal Responsibility Statement (PRS) in `Code.gs` references the same:

- IRC § 6103 (confidentiality of returns)
- IRC § 7213 (unauthorized disclosure)
- IRC § 7213A (unauthorized inspection)
- IRC § 7431 (civil damages)
- IRS Publication 1075

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
