# Changelog

All notable changes to this project will be documented in this file.

Versioning follows [Semantic Versioning](https://semver.org/).
Commit format follows [Conventional Commits](https://www.conventionalcommits.org/).

---

## Unreleased

### Fix

- move contributing.md to contributing/index.md for correct directory URL
- add navigation.indexes to mkdocs
- force clean gh-pages redeploy to fix CONTRIBUTING case sensitivity
- replace all .md links in README with MkDocs site URLs
- force redeploy to clear stale gh-pages artifacts
- add missing index files for directory routing
- enforce directory URLs and remove .md extensions
- manual recovery for landing pages and case-sensitivity
- final 404 resolution with clean URLs and case-sensitivity
- add missing index files and cleanup mkdocs config
- update navigation and file structure for docs
- final path correction for how-to-extend
- correct how-to-extend link path in index.md
- update nav and fix relative links
- change nav home to index.md
- resolve CI failures for v2.0.0

## v2.0.0 (2026-04-05) — Golden Release

### feat
- MIT License added
- Interview Showcase section in README
- Maintainer's closing note acknowledging human-AI collaboration
- Version bumped to v2.0.0 as official golden release

### docs
- README rewritten with interview-oriented navigation guide
- Changelog updated with complete version history

---

## v1.6.0 (2026-04-05)

### feat
- Architecture visualization: Mermaid sequence diagrams in playbook/02
- Commitizen config for interactive conventional commits
- Automated CHANGELOG generation via GitHub Actions release workflow
- Coverage badge and optimized README Quick Start

### fix
- Complete type hint coverage across all Python modules
- mkdocs Mermaid support with pymdownx.superfences custom fence

---

## v1.5.0 (2026-04-05)

### feat
- `.pre-commit-config.yaml` integrating ruff, mypy, pre-commit-hooks, check-secrets
- ADR-001 layered architecture, ADR-002 async database, ADR-003 CI/CD design
- `scripts/dev-setup.sh` one-command environment initialization
- Generic Item CRUD demo replacing url_checker
- `docs/how-to-extend.md` step-by-step guide

---

## v1.4.0 (2026-04-05)

### feat
- Request ID Middleware with `contextvars` propagation
- `RequestIdFilter` auto-injects `request_id` into every log line
- Async database tests with `pytest-asyncio` + SQLite in-memory
- `.devcontainer/` with Ruff, Pylance, Docker VS Code extensions
- `playbook/05-reliability-checklist.md`

---

## v1.3.0 (2026-04-05)

### feat
- `cookiecutter.json` for project scaffolding
- SQLAlchemy 2.x async database layer (connection, models, CRUD)
- `playbook/04-technical-decisions.md` architecture white paper

---

## v1.2.0 (2026-04-05)

### feat
- `url_checker` service demonstrating layered architecture
- Full type hints with `Callable`/`Awaitable`/`Response` on middleware
- mypy strict mode in `pyproject.toml`
- Python/FastAPI/License badges in README

---

## v1.1.0 (2026-04-05)

### feat
- GitHub Issue templates (bug report, feature request)
- Pull Request template with full checklist
- `deploy-docs.yml` GitHub Pages auto-deploy
- `pyproject.toml` with unified ruff and pytest config
- `CONTRIBUTING.md`

---

## v1.0.0 (2026-04-05)

### feat
- Multi-stage Dockerfile with non-root user and HEALTHCHECK
- `docker-compose.yml` one-command API + docs startup
- `playbook/03-observability-and-security.md`
- `scripts/check-secrets.sh` pre-commit scanner

---

## v0.3.0 (2026-04-05)

### feat
- GitHub Actions CI workflow
- Three-layer template architecture (api/services/schemas)
- MkDocs Material documentation site

---

## v0.1.0 (2026-04-05)

### feat
- FastAPI MVP with `/health` endpoint
- `ProcessTimeMiddleware` and global exception handler
- `playbook/01-standard-workflow.md` and `playbook/02-architecture-and-quality.md`
- SSOT project structure
