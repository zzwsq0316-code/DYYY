# RootHide GitHub Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the existing multi-scheme workflow with a tested RootHide-only macOS build that uploads exactly one validated DEB artifact.

**Architecture:** A shell contract test enforces the workflow's RootHide-only behavior before implementation. The workflow checks out the project, caches and prepares the RootHide Theos toolchain, builds with `SCHEME=roothide`, validates one package, and uploads the DEB without creating a release.

**Tech Stack:** GitHub Actions YAML, Bash, macOS GitHub-hosted runner, RootHide Theos, Theos SDKs

## Global Constraints

- Target repository: `zzwsq0316-code/DYYY`.
- Work only on branch `codex/roothide-actions` until integration is approved.
- Build only `roothide`; do not build `rootful` or `rootless` packages.
- Generate a workflow artifact only; do not create GitHub Releases or tags.
- Use read-only workflow permissions and no repository secrets.
- A build is successful only when exactly one DEB exists and its metadata matches `com.huami.dyyy` and `iphoneos-arm64e`.

---

### Task 1: Add a RootHide Workflow Contract Test

**Files:**
- Create: `.github/scripts/test-roothide-workflow.sh`
- Test: `.github/scripts/test-roothide-workflow.sh`

**Interfaces:**
- Consumes: `.github/workflows/build.yml`
- Produces: exit code 0 only when the workflow is RootHide-only and contains required validation and artifact-upload behavior

- [ ] **Step 1:** Add a strict shell contract test for manual triggering, read-only permissions, the RootHide build command, absence of other schemes, package validation, and artifact upload.
- [ ] **Step 2:** Run it against the existing workflow and require a failure caused by the remaining rootful/rootless steps.
- [ ] **Step 3:** Commit the failing test as `test: define RootHide workflow contract`.

### Task 2: Replace the Workflow with a RootHide-only Build

**Files:**
- Modify: `.github/workflows/build.yml`
- Test: `.github/scripts/test-roothide-workflow.sh`

**Interfaces:**
- Consumes: repository sources, `Makefile`, `control`, RootHide Theos, Theos SDKs
- Produces: one validated RootHide DEB in a GitHub Actions artifact

- [ ] **Step 1:** Replace the workflow with one macOS job using pinned action commits and `GITHUB_ACTIONS=true make clean package SCHEME=roothide FINALPACKAGE=1`.
- [ ] **Step 2:** Run the contract test and require exit 0.
- [ ] **Step 3:** Run YAML syntax validation and require exit 0.
- [ ] **Step 4:** Run `git diff --check` and inspect the workflow diff.
- [ ] **Step 5:** Commit as `ci: build RootHide package only`.

Pinned action revisions:
- checkout: `df4cb1c069e1874edd31b4311f1884172cec0e10`
- cache: `caa296126883cff596d87d8935842f9db880ef25`
- RootHide Theos setup: `c5ddc7728cc1bcac2f07ab65fbc3022d25ce0c10`
- artifact upload: `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`

### Task 3: Publish and Verify the GitHub Actions Run

- [ ] **Step 1:** Publish branch `codex/roothide-actions`.
- [ ] **Step 2:** Trigger `.github/workflows/build.yml` with that branch ref.
- [ ] **Step 3:** Inspect every job step and record the final conclusion.
- [ ] **Step 4:** Confirm the artifact contains exactly one RootHide DEB.
- [ ] **Step 5:** Report the run URL, conclusion, and artifact name; report logs instead of completion if any step fails.
