# Review a Pull Request Locally Before You Merge It

- **Tool:** Continue (open-source IDE assistant, Apache-2.0)
- **Cost:** $0 — open-source licence (Apache-2.0)
- **Limits:** Your hardware is the limit when run with a local model
- **Source:** https://github.com/continuedev/continue
- **Verified:** 2026-10-08
- **Guide:** https://iggym.github.io/everyday-ai-done-right/articles/continue-local-pr-review.html

## Steps

1. **Check out the branch.** Use git to switch to the pull request's branch locally and view the diff.
2. **Select the changed files.** Add only the changed files to the assistant's context so the review stays focused.
3. **Run the review prompt.** Use the prompt below and ask for findings with file and line references.
4. **Verify each finding.** Reproduce or reject every finding. Do not accept a suggestion you do not understand.
5. **Run the tests.** Run the project's test suite and linter yourself; the model is not a test runner.

## Prompt

```text
Review this diff as a careful senior engineer. List only concrete problems: bugs, missing error handling, unclear naming that affects behaviour, and missing tests. For each, give the file, the line, the problem, and a one-sentence fix. Say 'no issues found' if none.

DIFF:
<paste>
```

## Check your result

- [ ] Every finding is reproduced or rejected
- [ ] Tests and linters were run by you
- [ ] No code was merged on the model's word alone

## Pitfalls

- Models produce plausible but wrong findings; treat them as leads.
- Keep private repository code on local models, as the workflow above does.

_Licence and project status were read from the project's GitHub repository on 8 Oct 2026. Install commands and flags change between releases, so follow the project README for the current version._
