# Roadmap: OpenTelemetry Configuration Documentation Sync

**Project:** OpenTelemetry Configuration Documentation Sync
**Created:** 2026-03-06
**Granularity:** Coarse (3-5 phases)
**Coverage:** 12/12 requirements mapped

## Phases

- [x] **Phase 1: Core Data Pipeline** - YAML parsing, markdown generation, marker-based injection
- [x] **Phase 2: Repository Integration** - Git operations, CLI orchestration, local workflow (3/3 plans)
- [ ] **Phase 3: GitHub Actions Workflow** - Scheduled automation, manual triggers, authentication
- [ ] **Phase 4: PR Automation & Polish** - Automated pull requests, fork testing, validation pipeline

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Data Pipeline | 4/4 | Complete | 2026-03-06 |
| 2. Repository Integration | 3/3 | Complete | 2026-03-06 |
| 3. GitHub Actions Workflow | 0/3 | Ready to execute | - |
| 4. PR Automation & Polish | 0/? | Not started | - |

## Phase Details

### Phase 1: Core Data Pipeline

**Goal**: Developers can parse YAML schemas and generate markdown documentation tables with marker-based injection

**Depends on**: Nothing (first phase)

**Requirements**: CONF-01, CONF-02, CONF-03, CONF-04, CONF-05

**Success Criteria** (what must be TRUE):
1. Script reads YAML schema files from opentelemetry-configuration repository and loads structured data without errors
2. Script generates language implementation status tables in accordion format matching existing Hugo shortcode requirements
3. Script generates type documentation tables with descriptions, properties, and constraints
4. Script updates markdown files between BEGIN/END markers while preserving all manual content outside markers
5. Generated markdown contains properly escaped special characters (pipes, quotes) and passes visual inspection

**Plans**: 4 plans

Plans:
- [x] 01-01-PLAN.md — Project structure and TypedDict foundations
- [x] 01-02-PLAN.md — YAML schema parser with safe_load
- [x] 01-03-PLAN.md — Marker-based content updater
- [x] 01-04-PLAN.md — Markdown table content generator

---

### Phase 2: Repository Integration

**Goal**: Automation runs end-to-end locally, fetching schema files via GitHub API and integrating with npm formatting pipeline

**Depends on**: Phase 1

**Requirements**: CONF-11, CONF-12

**Success Criteria** (what must be TRUE):
1. Script fetches YAML schema files from opentelemetry-configuration repository via GitHub API
2. Script executes end-to-end from any directory (finds repo root dynamically)
3. Generated content passes `npm run fix:format` and `npm run check:format` without errors
4. Script follows collector-sync structure (uv project in scripts/declarative-configuration-sync/, src/ and tests/ directories)
5. Running script twice produces identical output (idempotent generation)

**Plans**: 3 plans

Plans:
- [x] 02-01-PLAN.md — GitHub API fetcher for schema files
- [x] 02-02-PLAN.md — Inventory Manager for schema discovery
- [x] 02-03-PLAN.md — CLI entry point and npm integration

---

### Phase 3: GitHub Actions Workflow

**Goal**: Documentation sync runs automatically on schedule and can be triggered manually with proper authentication

**Depends on**: Phase 2

**Requirements**: CONF-06, CONF-07

**Success Criteria** (what must be TRUE):
1. GitHub Action triggers manually via workflow_dispatch from Actions UI
2. GitHub Action runs daily at 03:00 UTC on schedule
3. GitHub Action triggers when opentelemetry-configuration repository publishes a release (deferred - manual trigger serves as workaround)
4. Workflow authenticates using otelbot GitHub App credentials with proper permissions (contents: write, pull-requests: write)
5. Workflow executes Python script successfully and reports failures with actionable error messages

**Plans**: 3 plans

Plans:
- [ ] 03-01-PLAN.md — Python --mode flag support and latest release fetching
- [ ] 03-02-PLAN.md — Shell script orchestration for workflow execution
- [ ] 03-03-PLAN.md — Main and fork workflow files with otelbot authentication

---

### Phase 4: PR Automation & Polish

**Goal**: Automation creates/updates pull requests automatically and contributors can test in their forks

**Depends on**: Phase 3

**Requirements**: CONF-09, CONF-10

**Success Criteria** (what must be TRUE):
1. GitHub Action creates new PR with generated changes when content differs from current docs
2. GitHub Action updates existing PR when subsequent runs produce different content
3. PR includes descriptive title and body with summary of changes and link to triggering event
4. Fork testing workflow (configuration-sync-fork.yml) allows contributors to test sync in their forks without otelbot access
5. Generated content passes all validation checks (formatting, link checking) or provides advisory warnings

**Plans**: TBD

---

## Coverage Validation

All v1 requirements mapped to phases:

| Requirement | Phase | Description |
|-------------|-------|-------------|
| CONF-01 | Phase 1 | Python script reads YAML schemas |
| CONF-02 | Phase 1 | Python script parses YAML into structured data |
| CONF-03 | Phase 1 | Python script generates language implementation status tables |
| CONF-04 | Phase 1 | Python script generates type documentation tables |
| CONF-05 | Phase 1 | Python script updates markdown files between markers |
| CONF-06 | Phase 3 | GitHub Action runs on manual dispatch |
| CONF-07 | Phase 3 | GitHub Action runs on schedule (daily 03:00 UTC) |
| CONF-08 | Phase 4 | GitHub Action runs on opentelemetry-configuration releases (deferred) |
| CONF-09 | Phase 4 | GitHub Action creates/updates PR with otelbot |
| CONF-10 | Phase 4 | Fork testing workflow for contributors |
| CONF-11 | Phase 2 | Script follows collector-sync structure |
| CONF-12 | Phase 2 | Generated content formatted correctly |

**Coverage:** 12/12 requirements mapped ✓

---

## Notes

**Phase derivation rationale:**
- Phase 1 establishes foundation components (parsing, generation, injection) that can be tested independently with fixtures
- Phase 2 adds git operations and CLI orchestration while keeping them isolated for testability
- Phase 3 establishes CI/CD foundation with scheduling and authentication
- Phase 4 adds final integration layer (PR automation and fork testing)

**Research alignment:**
- Structure directly follows research recommendation (4-phase progression)
- Phase boundaries match dependency layers identified in research
- All critical pitfalls addressed in success criteria (yaml.safe_load, marker specificity, schedule configuration, authentication)

**Granularity calibration:**
- Config setting: "coarse" (3-5 phases)
- Delivered: 4 phases
- Natural delivery boundaries prevented further compression

---

*Last updated: 2026-03-06 after Phase 3 planning*
