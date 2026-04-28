#!/usr/bin/env python3
"""
draft_training.py — Extracted content JSON → training content draft (Markdown).

Takes the JSON produced by extract_content.py and produces a Markdown
draft showing how the source content maps to the training structure.
This draft is for human review — you read through it, decide what to
keep, what to rewrite, and what to drop, then transcribe the final
content into _build_index.py.

Usage:
    python3 draft_training.py content.json [-o draft.md]

The draft includes:
- The source content organized by section
- Suggested mapping to training modules (Foundations / Handling /
  In Practice / Consequences / Acknowledgment)
- Inferred PRS statements based on detected legal references
- A "review checklist" showing what needs editorial decisions
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# Keywords that suggest which module a section belongs in
MODULE_KEYWORDS = {
    "Foundations": [
        "introduction", "overview", "general", "what is", "definition",
        "purpose", "background", "principles", "fundamentals", "scope",
    ],
    "Handling": [
        "category", "categories", "type", "types", "pii", "fti", "phi", "ssa",
        "personally identifiable", "tax information", "health information",
        "need to know", "access", "secure", "transmission", "storage",
        "encryption", "logging",
    ],
    "In Practice": [
        "practice", "daily", "do and don't", "guideline", "procedure",
        "email", "communication", "ai tool", "disposal", "destruction",
        "device", "mobile", "transport", "remote",
    ],
    "Consequences": [
        "penalty", "penalties", "violation", "consequence", "fine",
        "imprisonment", "civil", "criminal", "liability", "ircsection",
        "irc 7213", "irc 7431", "mishandling", "breach", "incident",
        "report", "reporting", "disclosure",
    ],
    "Acknowledgment": [
        "acknowledgment", "acknowledgement", "responsibility", "prs",
        "personal responsibility", "training requirement", "annual",
        "recertification", "signature", "certify",
    ],
}

LEGAL_REFERENCES = [
    (r"\b(?:IRC|Internal Revenue Code)\s*(?:Section|Sections|sec\.?|\u00a7|\u00a7\u00a7)?\s*6103\b", "IRC § 6103 (confidentiality of returns)"),
    (r"\b(?:IRC|Internal Revenue Code)\s*(?:Section|Sections|sec\.?|\u00a7|\u00a7\u00a7)?\s*7213(?!A)\b", "IRC § 7213 (unauthorized disclosure)"),
    (r"\b(?:IRC|Internal Revenue Code)\s*(?:Section|Sections|sec\.?|\u00a7|\u00a7\u00a7)?\s*7213A\b", "IRC § 7213A (unauthorized inspection)"),
    (r"\b(?:IRC|Internal Revenue Code)\s*(?:Section|Sections|sec\.?|\u00a7|\u00a7\u00a7)?\s*7431\b", "IRC § 7431 (civil damages)"),
    (r"\bPub(?:lication)?\s*1075\b", "IRS Publication 1075"),
    (r"\bHIPAA\b", "HIPAA"),
    (r"\bPrivacy Act\s*(?:of)?\s*1974\b", "Privacy Act of 1974"),
    (r"\bNIST\s*(?:SP)?\s*800-\d+\b", "NIST SP 800-series"),
    (r"\bCMS\s+ARC[\s-]?AMPE\b", "CMS ARC-AMPE"),
    (r"\bFERPA\b", "FERPA"),
    (r"\bCJIS\b", "CJIS"),
]


def categorize_section(section):
    """Suggest which training module this section maps to."""
    text = (section.get("heading", "") + " " +
            " ".join(section.get("body", [])) + " " +
            " ".join(section.get("bullets", [])) + " " +
            section.get("notes", "")).lower()

    scores = {}
    for module, keywords in MODULE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[module] = score

    if not scores:
        return "Unmapped"
    return max(scores, key=scores.get)


def detect_legal_references(content):
    """Find all legal/regulatory references in the content."""
    found = []
    for pattern, label in LEGAL_REFERENCES:
        if re.search(pattern, content, re.IGNORECASE):
            found.append(label)
    return found


def make_section_md(section):
    """Render a section as Markdown."""
    lines = []
    indent = "  " * max(0, section["level"] - 1)
    lines.append(f"{indent}### {section['heading']}")

    if section.get("page"):
        lines.append(f"{indent}*Source: page/slide {section['page']}*")
    lines.append("")

    for para in section.get("body", []):
        lines.append(f"{indent}{para}")
        lines.append("")

    if section.get("bullets"):
        for b in section["bullets"]:
            lines.append(f"{indent}- {b}")
        lines.append("")

    if section.get("notes"):
        lines.append(f"{indent}**Speaker notes:** {section['notes']}")
        lines.append("")

    return "\n".join(lines)


def build_draft(content):
    """Build a Markdown draft from the extracted JSON."""
    lines = []

    title = content.get("title", "Untitled")
    src = content.get("source", {})
    sections = content.get("sections", [])

    lines.append(f"# Training Content Draft: {title}")
    lines.append("")
    lines.append(f"**Source:** `{src.get('filename', '?')}` ({src.get('type', '?').upper()}, "
                 f"{src.get('pages', '?')} pages/slides)")
    lines.append(f"**Sections extracted:** {len(sections)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How to use this draft")
    lines.append("")
    lines.append("This draft maps source-document sections to the 5-module training structure.")
    lines.append("It is not the final training content — it is a working document for review.")
    lines.append("")
    lines.append("**Workflow:**")
    lines.append("")
    lines.append("1. Read through each module section below.")
    lines.append("2. For each source section, decide: **Keep as-is**, **Rewrite**, **Merge**, or **Drop**.")
    lines.append("3. For sections to keep/rewrite, transcribe to the corresponding module in `_build_index.py`.")
    lines.append("4. Add scenarios, transitions, and module intros that aren't in source material.")
    lines.append("5. Have the security team review the final content before publishing.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group sections by suggested module
    by_module = {}
    for section in sections:
        module = categorize_section(section)
        by_module.setdefault(module, []).append(section)

    module_order = ["Foundations", "Handling", "In Practice", "Consequences", "Acknowledgment", "Unmapped"]

    for module in module_order:
        if module not in by_module:
            continue

        lines.append(f"## Module: {module}")
        lines.append("")
        if module == "Unmapped":
            lines.append("*These sections didn't strongly match any module. Review manually.*")
            lines.append("")

        for section in by_module[module]:
            lines.append(make_section_md(section))

        lines.append("---")
        lines.append("")

    # Detected legal references
    full_text = json.dumps(content)
    legal_refs = detect_legal_references(full_text)
    if legal_refs:
        lines.append("## Detected Legal References")
        lines.append("")
        lines.append("The source document references the following frameworks. Make sure your")
        lines.append("Personal Responsibility Statement (PRS) in `Code.gs` references the same:")
        lines.append("")
        for ref in legal_refs:
            lines.append(f"- {ref}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Review checklist
    lines.append("## Review Checklist")
    lines.append("")
    lines.append("Before transcribing to `_build_index.py`, confirm:")
    lines.append("")
    lines.append("- [ ] Source content is current (check effective date / revision)")
    lines.append("- [ ] Agency-specific procedures are accurate (don't copy generic regulatory text verbatim)")
    lines.append("- [ ] Each module has 3-5 distinct sections (not too sparse, not too dense)")
    lines.append("- [ ] Scenarios are added — extracted source material rarely has them")
    lines.append("- [ ] Module intro 'Picture this' hooks are written")
    lines.append("- [ ] PRS in `Code.gs` references the legal frameworks listed above")
    lines.append("- [ ] Penalty figures match current law (penalties have been adjusted for inflation)")
    lines.append("- [ ] Information security team has reviewed for accuracy and completeness")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Convert extracted content JSON into a training content draft for human review."
    )
    parser.add_argument("input", help="Input content JSON file (output of extract_content.py)")
    parser.add_argument("-o", "--output", default="draft.md", help="Output Markdown path (default: draft.md)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        content = json.load(f)

    draft = build_draft(content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(draft)

    print(f"Wrote draft to {args.output}", file=sys.stderr)
    print(f"  Sections processed: {len(content.get('sections', []))}", file=sys.stderr)
    print(f"  Title: {content.get('title', '?')}", file=sys.stderr)


if __name__ == "__main__":
    main()
