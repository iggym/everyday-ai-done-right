# Turn Paper Receipts into a CSV with Free Tesseract OCR

- **Tool:** Tesseract OCR (Apache-2.0)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/tesseract-ocr/tesseract
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/tesseract-receipts-to-csv.html

## Steps

1. **Photograph flat and well lit.** Place each receipt on a dark surface, shoot from above, and save as PNG or JPG.
2. **Install Tesseract.** Use your package manager (for example brew install tesseract or your Linux repository) and check with tesseract --version.
3. **Extract the text.** Run tesseract receipt.png stdout -l eng for each photo and save the output to a text file per receipt.
4. **Pull out the fields.** Ask a local model, or a short script, to extract date, merchant, total, and category into CSV columns. Use the prompt below.
5. **Reconcile the total.** Check the extracted total against the printed total for every receipt. Fix the ones that differ.

## Prompt

```text
From this OCR text of one receipt, return one CSV line with the columns: date (YYYY-MM-DD), merchant, total (numbers only, dot as decimal), currency, category (food, transport, household, health, other). If a field is not clear, write UNCLEAR in that cell. Output the header line once, then one data line.

OCR TEXT:
<paste>
```

## Check your result

- [ ] Each total matches the printed receipt
- [ ] Dates are in one format
- [ ] UNCLEAR cells were fixed by hand

## Pitfalls

- Thermal receipts fade over time; scan them soon after you get them.
- OCR confuses 0/O and 1/l. Check any total that looks wrong.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
