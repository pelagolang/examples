# Contributing

Part of the [Pelago](https://github.com/pelagolang/pelago) project. The full guide to commits and pull requests is
[`docs/contributing/commits.md`](https://github.com/pelagolang/pelago/blob/main/docs/contributing/commits.md) in the main repository; the short version follows.

## Before you push

```
pelago fmt .          # format every .pel file (use --check to only look)
pelago check .
pelago run . | diff - expected.txt
```

If you change what the program prints on purpose, update `expected.txt` in the same commit. CI runs the same three commands, plus a native build.

## Commits and pull request titles

Every commit subject and every pull request title uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
type(scope): summary
```

- Types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `chore`, `ci`, `build`, `revert`.
- `scope` is optional (for example `rpn`, `ci`).
- The summary is imperative, starts with a lowercase letter, has no trailing period, and keeps the first line under 72 characters.
- A breaking change gets `!` after the type or scope or a `BREAKING CHANGE:` footer.
- Pull requests are squash-merged, so the PR title becomes the commit on `main`.

CI (`.github/workflows/conventional-commits.yml`) lints the PR title and every non-merge commit subject.

## Branches

`<author>/<type>/<short-name>`, for example `dennis/feat/more-operators` or `claude/docs/readme-setup`.

## Licence

By contributing you agree that your work is licensed under MIT OR Apache-2.0, like the rest of the project.
