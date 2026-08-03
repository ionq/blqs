# Changelog

All notable changes to `blqs` and `blqs-cirq` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and both
packages follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). They
version independently; releases are tagged `blqs-vX.Y.Z` and `blqs-cirq-vX.Y.Z`.

## [Unreleased]

### Added

- Type information now ships with both packages (PEP 561 `py.typed` markers), so
  downstream code type-checks against `blqs` and `blqs-cirq`.
- `blqs-cirq` wraps the gates added in cirq 1.6: `UniformSuperpositionGate`, and
  the Google gates `WillowGate`, `AnalogDetuneQubit`, and `AnalogDetuneCouplerOnly`.

### Changed

- **Minimum Python is now 3.11** (previously 3.7). Tested on 3.11 - 3.13.
- `blqs-cirq` now supports `cirq` and `cirq-google` `>=1.6,<2` (previously pinned
  to 1.2.0).
- Packaging moved from `setup.py`/`requirements.txt` to `pyproject.toml` in a
  uv workspace; development tooling is now `ruff` (lint + format) and `ty`
  (type check), with a coverage gate. See `CONTRIBUTING.md`.

### Removed

- Unused runtime dependencies `astor` and `pytype`.

## [0.1.0]

- Initial release of `blqs` and `blqs-cirq`.
