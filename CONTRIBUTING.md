# Contributing to blqs

Thanks for your interest in improving blqs. This guide covers the contributor
license agreement, development setup, the local checks, and the conventions that
are easy to trip over.

## Contributor License Agreement

Contributions are accepted under the project's [Apache 2.0 license](LICENSE). To
contribute you must sign a Contributor License Agreement, which confirms you have
the right to contribute the code. To receive IonQ's CLA, email
<opensource@ionq.com>.

## Repository layout

This repo is a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/)
with two published distributions:

- `blqs/` - the base framework (distribution `blqs`, import `blqs`).
- `blqs_cirq/` - the Cirq application (distribution `blqs-cirq`, import `blqs_cirq`),
  which depends on `blqs` as a workspace member.

The root `pyproject.toml` is a virtual project: it is not published and only holds
the workspace definition, the shared dev dependency group, and shared tool config
(ruff, pytest, coverage, ty).

## Development setup

This project uses [`uv`](https://docs.astral.sh/uv/). The `uv.lock` file is
committed and CI runs with `UV_FROZEN=true`; use `uv`, not `pip`, so the lockfile
stays authoritative.

```sh
git clone https://github.com/ionq/blqs
cd blqs
uv sync            # creates .venv, installs both packages editable + dev deps
uvx pre-commit install   # optional: run ruff on commit
```

## Running the checks

```sh
uv run pytest                 # both packages, with the coverage gate
uv run ruff check             # lint
uv run ruff format            # format (drop nothing; add --check to verify only)
uv run ty check               # type check
```

`pyproject.toml` is the source of truth for these commands and their config.

## Conventions worth knowing

- **`blqs/blqs/testing_samples.py` is line-number sensitive.** Several tests
  assert exact line numbers in tracebacks produced by the build rewrite, so the
  file is excluded from ruff (lint and format). If you add sample code, append it
  to the end and do not reformat the file.
- **Bumping cirq can require wrapping new gates.** `blqs_cirq` mirrors every
  `cirq.Gate` subclass; the tests in `gates_test.py` and `google_gates_test.py`
  enforce this. When a cirq upgrade adds gates, either wrap them (public cirq
  gates in `gates.py`, google gates in `google/`) or add them to the test
  exclusion set (private/testing gates).
- **Type checking is advisory for now.** `ty` is wired into CI but non-blocking
  while its diagnostics on the dynamic build core are worked down; new
  hand-written code should still type-check cleanly where practical.

## Pull requests

1. Branch off `main` and make your changes, adding tests for any code you touch.
2. Run the checks above (or rely on `pre-commit`) before pushing.
3. Open a PR against `main`; a reviewer will follow up.
