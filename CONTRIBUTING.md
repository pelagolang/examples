# Contributing

Part of the [Pelago](https://github.com/pelagolang/pelago) project. The full guide to commits and pull requests is
[`docs/contributing/commits.md`](https://github.com/pelagolang/pelago/blob/main/docs/contributing/commits.md) in the main repository; the short version follows.

## Adding an example

- One small, focused example per feature, in the folder for its topic (`basics`, `types`, `braids`, `collections`,
  `strings`, `errors`, `iterators`, `files`, `time`, `math`, `crypto`, `json`, `concurrency`, `modules`, `programs`).
  A multi-file example is a folder with a `main.pel`.
- Start the file with the header comment: `/// Shows:` (what it demonstrates), `/// Run:` (the command),
  `/// Output:` and then the exact output, one `/// | ` line per line printed. See the [README](README.md#how-an-example-is-written).
- It must type check and print the same text natively and in the interpreter. Do not print anything that changes from run to run.
- Add a row to the table in `README.md` (CI fails if an example is missing from it).
- Link to documentation pages that exist on the live docs site, and never to private repositories.

## Before you push

```
pelago fmt .                          # format every .pel file (use --check to only look)
python3 tools/run-examples.py         # check and run every example; add --bless to rewrite the Output lines of a new one
```

`--bless` writes the `/// |` lines from what the program prints: read the diff, because it will bless a wrong answer as readily as a right one.
CI runs the same commands, builds native executables, and runs the RPN project in `projects/rpn`.

## Commits and pull request titles

Every commit subject and every pull request title uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
type(scope): summary
```

- Types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `chore`, `ci`, `build`, `revert`.
- `scope` is optional (for example `types`, `ci`).
- The summary is imperative, starts with a lowercase letter, has no trailing period, and keeps the first line under 72 characters.
- A breaking change gets `!` after the type or scope or a `BREAKING CHANGE:` footer.
- Pull requests are squash-merged, so the PR title becomes the commit on `main`.

CI (`.github/workflows/conventional-commits.yml`) lints the PR title and every non-merge commit subject.

## Branches

`<author>/<type>/<short-name>`, for example `dennis/feat/more-operators` or `claude/docs/readme-setup`.

## Licence

By contributing you agree that your work is licensed under MIT OR Apache-2.0, like the rest of the project.
