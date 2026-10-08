# Write Unit Tests for a Small Script with Aider

- **Tool:** Aider (open-source coding agent, Apache-2.0)
- **Cost:** $0 — open-source licence (Apache-2.0)
- **Limits:** Your hardware is the limit when run with a local model
- **Source:** https://github.com/Aider-AI/aider
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/aider-unit-tests-small-script.html

## Steps

1. **Start with a tiny script.** Pick a script under 100 lines, such as a unit converter or a budget calculator, and commit it.
2. **Ask for tests.** Use the prompt below in Aider with the script added to the chat.
3. **Run the tests.** Run pytest (install it first). Read the output even when everything passes.
4. **Break the code on purpose.** Change one line of the script to produce a wrong answer and confirm a test fails.
5. **Explain each test to yourself.** For each test, write one sentence saying what behaviour it protects.

## Prompt

```text
Write pytest unit tests for the functions in this file. Cover normal inputs, edge cases such as zero and negative values, and one error case. Do not change the script. Keep each test short with a descriptive name.

SCRIPT:
<paste>
```

## Check your result

- [ ] Tests run and pass on the correct code
- [ ] At least one test fails when you break the code on purpose
- [ ] You can explain each test

## Pitfalls

- A passing test is not proof of correct behaviour if the test asserts the wrong thing.
- Do not accept generated tests that only call the function without checking the result.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
