# Content Pipeline

How to feed an existing training document (PDF, DOCX, or PPTX) into the system and produce a structured content draft for review.

## What this pipeline does

Most agencies don't start from scratch — they have an existing PowerPoint or Word doc that's been the "annual training" for years. The pipeline takes that existing document and pulls structured content out of it, organized in a way that maps cleanly to the 5-module training format.

**What it doesn't do:** rewrite or invent content. The pipeline does extraction and organization. Editorial decisions — what to keep, what to rewrite, what scenarios to add, what to drop entirely — stay with you and your information security team. That's by design. Compliance content needs human judgment.

## Two-step workflow

```
┌─────────────────┐    extract_content.py    ┌──────────────┐
│ Source Document │  ────────────────────────►│ content.json │
│ (.pdf .docx     │                           │ (structured) │
│  .pptx)         │                           └──────┬───────┘
└─────────────────┘                                  │
                                                     │ draft_training.py
                                                     ▼
                                           ┌──────────────────┐
                                           │ draft.md         │
                                           │ (review document)│
                                           └──────┬───────────┘
                                                  │
                                                  │ Human review
                                                  ▼
                                       ┌──────────────────────┐
                                       │ Final training       │
                                       │ content in           │
                                       │ _build_index.py      │
                                       └──────────────────────┘
```

## Step 1: Extract structured content

```bash
cd tools
python3 extract_content.py path/to/your/training.pdf -o content.json
```

Or with the `--summary` flag to also print a tree view to your terminal:

```bash
python3 extract_content.py path/to/your/training.pdf -o content.json --summary
```

### What gets extracted by format

**PDF** (via pypdf)
- Text content with heading-level inference (1.0, 2.5, 3.4.1 numbered patterns; ALL CAPS short lines)
- Page numbers preserved
- Wrapped paragraph lines re-merged
- Document metadata title (if present)

**DOCX** (via python-docx)
- Headings with explicit Heading 1/2/3 styles → preserved level
- Title style → document title
- List Bullet style → bullets array
- Table contents → flattened as bullet rows
- Document metadata title

**PPTX** (via python-pptx)
- Slide titles and body text
- Bullet content (any paragraph at level > 0)
- **Speaker notes** — often the richest content in compliance training PPTs
- Slide numbers preserved as `page` field

### Output JSON structure

```json
{
  "source": {
    "filename": "training.pptx",
    "type": "pptx",
    "pages": 24
  },
  "title": "Annual Sensitive Data Training",
  "sections": [
    {
      "level": 1,
      "heading": "What is Sensitive Data?",
      "body": ["Five categories require special protection:"],
      "bullets": [
        "Personally Identifiable Information (PII)",
        "Federal Tax Information (FTI)",
        ...
      ],
      "page": 2,
      "notes": "Emphasize that mishandling creates real harm to real people..."
    },
    ...
  ]
}
```

## Step 2: Generate a review draft

```bash
python3 draft_training.py content.json -o draft.md
```

This produces a Markdown draft that:

- **Maps each source section to a suggested training module** (Foundations / Handling / In Practice / Consequences / Acknowledgment) using keyword matching
- **Lists detected legal references** so you can verify the PRS in `Code.gs` cites the right frameworks
- **Provides a review checklist** of what needs editorial decisions before going live
- **Flags unmapped sections** that need manual placement

### What the draft looks like

```markdown
# Training Content Draft: Annual Sensitive Data Training

**Source:** training.pptx (PPTX, 24 pages/slides)
**Sections extracted:** 22

## Module: Foundations

### What is Sensitive Data?
*Source: page/slide 2*

Five categories require special protection:

- Personally Identifiable Information (PII)
- Federal Tax Information (FTI)
- Protected Health Information (PHI)
...

**Speaker notes:** Emphasize that mishandling creates real harm...

## Module: Handling
...

## Detected Legal References

- IRC § 6103 (confidentiality of returns)
- IRC § 7213 (unauthorized disclosure)
- IRS Publication 1075
- HIPAA

## Review Checklist

- [ ] Source content is current
- [ ] Agency-specific procedures are accurate
- [ ] Each module has 3-5 distinct sections
- [ ] Scenarios are added (extracted material rarely has them)
...
```

## Step 3: Human review

The draft is your working document. Walk through it and decide for each section:

- **Keep as-is** — the source content is good and just needs to be transcribed
- **Rewrite** — the substance is right but the tone/length needs work
- **Merge** — combine with another section
- **Drop** — not needed in the new training

For each section you keep, transcribe the content into the corresponding location in `_build_index.py`. See `docs/CONTENT_GUIDE.md` for the structure of `_build_index.py` and how content is organized within it.

### What the pipeline can't do

- **Generate scenarios.** Source training rarely has the kind of "Picture this" scenarios that make compliance content stick. You'll need to write these yourself based on real or anonymized incidents.
- **Modernize outdated content.** If your source training references penalties, regulations, or thresholds that have changed, the pipeline won't know. Verify currency manually.
- **Adapt for your specific agency.** Generic regulatory text is rarely what staff need to hear. Translate "agencies must implement..." into "at your agency, we do this by..."
- **Catch contradictions.** If your old PPT says one thing and current policy says another, the pipeline doesn't know — it just extracts what's there.

## Why two tools instead of one

The pipeline is split into extraction (`extract_content.py`) and drafting (`draft_training.py`) for two reasons:

1. **Extraction is reusable.** The JSON output is structured enough to feed into other tools — translation services, LLM-assisted rewriting, content management systems, whatever. Don't lock the extracted content into a specific output format.
2. **Drafting opinions can vary.** The default categorization rules (which keywords map to which module) work for typical sensitive-data trainings but won't fit every use case. Forking `draft_training.py` to use different rules is easier than modifying a monolithic pipeline.

If you have a different content structure (8 modules instead of 5, different module names, different categorization rules), edit `MODULE_KEYWORDS` at the top of `draft_training.py`.

## Working example

Run all of these against your own document:

```bash
cd tools

# Extract (this creates content.json)
python3 extract_content.py /path/to/your/training.pdf -o content.json --summary

# Generate draft (this creates draft.md)
python3 draft_training.py content.json -o draft.md

# Open draft.md in your editor of choice and start reviewing
```

For a worked example without your own document, see the test files in `tools/test_samples/` — three sample sources (PDF, DOCX, PPTX) with the corresponding extracted JSON and generated drafts.

## Common issues

**"My PDF extracts as one giant section."**
The PDF probably doesn't use numbered section headers (1.0, 2.1, etc.) and doesn't have a clear visual hierarchy that pypdf can detect. Try:
- Convert the PDF to DOCX first (Word can do this), then run extraction on the DOCX where heading styles are explicit
- Or break the PDF into smaller sub-documents and extract each

**"My DOCX has body text marked as headings."**
Check the actual paragraph styles in the source document. If everything is "Normal" with manual font formatting, the extractor can't tell what's a heading. Reset paragraph styles in Word so headings actually use Heading 1/2/3 styles before extracting.

**"My PPTX speaker notes are empty in the JSON but I can see them in PowerPoint."**
python-pptx requires the notes to be in the actual `notesSlide` element of the file. If the notes were added as a separate text box on the slide (not the dedicated notes pane), they won't be captured. Check your source.

**"The draft put my section in the wrong module."**
Edit `MODULE_KEYWORDS` in `draft_training.py` to add keywords specific to your content. Re-run the draft step (no need to re-extract).
