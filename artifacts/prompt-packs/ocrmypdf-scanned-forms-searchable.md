# Make Scanned Forms Searchable with OCRmyPDF

- **Tool:** OCRmyPDF + Tesseract (MPL-2.0 / Apache-2.0)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ocrmypdf/OCRmyPDF
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ocrmypdf-scanned-forms-searchable.html

## Steps

1. **Install OCRmyPDF.** Follow the project's install guide for your system. It needs Tesseract and Ghostscript, which the guide lists.
2. **Run it on one form.** Use ocrmypdf --language eng scan.pdf searchable.pdf. Use --skip-text if some pages already have text.
3. **Check the result.** Search for a word you know is on the form. If it is not found, rescan at higher resolution and repeat.
4. **Save the reference numbers.** Copy the reference, case number, or deadline into your calendar or a notes file the same day.
5. **Keep originals.** Store the scan and the searchable copy together, with a date in the filename.

## Prompt

```text
From the text of this official form, list: the issuing office, any reference or case number, every deadline with its date, the documents the form asks me to provide, and the contact details. Quote each item exactly. Do not interpret the legal effect of the form.

FORM TEXT:
<paste>
```

## Check your result

- [ ] The reference number matches the printed form
- [ ] Every deadline is in your calendar
- [ ] The original scan is kept alongside the searchable copy

## Pitfalls

- Poor scans give poor text; use 300 dpi or higher if you can.
- If a deadline matters, confirm it with the issuing office.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
