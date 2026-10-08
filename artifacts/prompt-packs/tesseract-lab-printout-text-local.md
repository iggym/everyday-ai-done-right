# Read Lab Printouts Locally: Extract the Text, Then Prepare Better Questions

- **Tool:** Tesseract OCR (Apache-2.0)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/tesseract-ocr/tesseract
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/tesseract-lab-printout-text-local.html

## Steps

1. **Scan or photograph the report.** Flatten it, avoid glare, and save as PNG.
2. **Extract the text.** Run tesseract report.png stdout -l eng and save the output to report.txt.
3. **Check every number.** Compare numbers and units with the paper. OCR often misreads decimals and minus signs.
4. **Write questions, not conclusions.** Use the prompt below to list the tests, the reference ranges printed on the report, and questions to ask.
5. **Bring the list to your appointment.** Ask the clinician what each result means for you specifically.

## Prompt

```text
From this lab report text, list each test name, its result, its units, and the reference range printed on the report. Mark any result the report itself flags as high or low. Then write up to five neutral questions a patient could ask a clinician. Do not interpret the results or give advice.

REPORT TEXT:
<paste>
```

## Check your result

- [ ] Each value and unit matches the paper report
- [ ] No interpretation or advice was added
- [ ] Questions are written in your own words before the visit

## Pitfalls

- Never change a medication or treatment based on a model's reading of your results.
- Urgent symptoms need immediate medical care, not a spreadsheet.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
