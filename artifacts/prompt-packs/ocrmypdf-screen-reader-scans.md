# Make Scanned Documents Work with Screen Readers Using OCRmyPDF

- **Tool:** OCRmyPDF + Tesseract (MPL-2.0 / Apache-2.0)
- **Cost:** $0 — open-source licence, runs on your computer
- **Limits:** Speed depends on your hardware; no quota or account
- **Source:** https://github.com/ocrmypdf/OCRmyPDF
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ocrmypdf-screen-reader-scans.html

## Steps

1. **Scan at 300 dpi.** Greyscale is fine; colour is only needed for diagrams.
2. **Run OCRmyPDF.** Use ocrmypdf --language eng --deskew scan.pdf accessible.pdf. --deskew straightens crooked pages and improves recognition.
3. **Test with a screen reader.** Open the file in your screen reader or the built-in reader and listen to the first page.
4. **Fix the tags if needed.** For complex forms, a tagged PDF editor may be required; note this for later.
5. **Provide an alternative when necessary.** For maps or charts, add a plain-text description next to the document.

## Prompt

```text
Write concise alt text for each figure described in the notes below. Keep each description under 40 words, say what matters for understanding the document, and do not invent details.

NOTES ON FIGURES:
<paste>
```

## Check your result

- [ ] Text can be selected and read aloud
- [ ] Pages are straight and legible
- [ ] Figures have a text description

## Pitfalls

- OCR cannot read handwriting reliably; type it or ask for an alternative format.
- Accessible-format rights for reading materials are set out in your local law; ask your school or library if unsure.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
