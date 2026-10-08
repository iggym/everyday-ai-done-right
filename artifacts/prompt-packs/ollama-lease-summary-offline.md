# Summarise a Lease Offline with Ollama — Nothing Leaves Your Laptop

- **Tool:** Ollama (local, MIT-licensed)
- **Cost:** $0 — open-source (MIT licence)
- **Limits:** Your own hardware is the only limit; no quota or account
- **Source:** https://ollama.com
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/ollama-lease-summary-offline.html

## Steps

1. **Install Ollama.** Download the installer from ollama.com for macOS, Windows, or Linux and open a terminal. Check the install with ollama --version.
2. **Download one small model.** Run ollama pull llama3.2 (or another instruct model from the Ollama library that fits your RAM). The download happens once; afterwards the model runs offline.
3. **Turn the lease into text.** Export the lease to a text file. If it is a scan, run it through the OCR guide in this directory first, then save the output as lease.txt.
4. **Ask for a structured summary.** Use the prompt below, paste the lease text after it, and keep the answer in a file next to the lease.
5. **Check every number against the source.** Open the original clause for each rent amount, date, and deadline. A small model can misread a clause; the page reference is what counts.

## Prompt

```text
You are helping a tenant read a lease. Using only the text below, list: (1) monthly rent and due date, (2) deposit amount and conditions for return, (3) notice period for ending the tenancy, (4) who is responsible for repairs and by when, (5) any clause about fees, late payments, or entry. For each item give the section number or quote. If something is not stated, write 'not stated'. Do not give legal advice.

LEASE TEXT:
<paste here>
```

## Check your result

- [ ] Every figure has a quoted clause or section number next to it
- [ ] Anything marked 'not stated' is double-checked in the original
- [ ] The lease file never left your computer

## Pitfalls

- Long leases can exceed a small model's context window; split the document by section and summarise each part.
- A summary is not legal advice. For disputes, use the civic guides linked below.

_Checked on 8 Oct 2026._
