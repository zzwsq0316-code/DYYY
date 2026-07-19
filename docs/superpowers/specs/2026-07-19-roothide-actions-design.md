# RootHide GitHub Actions Build Design

## Goal

Replace the existing multi-scheme workflow with a RootHide-only workflow that reliably builds one installable DYYY DEB and exposes it as a downloadable GitHub Actions artifact.

## Scope

- Repository: `zzwsq0316-code/DYYY`
- Workflow: `.github/workflows/build.yml`
- Package scheme: `roothide` only
- Runner: GitHub-hosted macOS
- Distribution: workflow artifact only
- Out of scope: GitHub Releases, device installation, rootful packages, rootless packages, IPA injection

## Triggers

The workflow supports:

1. Manual execution through `workflow_dispatch`.
2. Pushes to `main` when build-relevant source, resource, package metadata, Makefile, or workflow files change.

Documentation-only changes do not start a build.

## Toolchain

The job runs on a GitHub-hosted macOS runner. It installs the RootHide Theos fork and Theos SDKs through the existing Theos setup action. The action revision will be pinned to an immutable commit during implementation to reduce supply-chain risk.

The project already declares:

- iOS deployment target 14.0
- architectures `arm64 arm64e`
- support for `SCHEME=roothide`
- CI behavior when `GITHUB_ACTIONS=true`

## Build Flow

1. Check out the repository with submodules.
2. Restore the cached RootHide Theos toolchain and SDKs.
3. Install or prepare Theos when the cache is incomplete.
4. Remove stale `.theos` and `packages` output.
5. Run:

   ```bash
   GITHUB_ACTIONS=true make clean package SCHEME=roothide FINALPACKAGE=1
   ```

6. Locate the generated DEB in `packages/`.
7. Require exactly one DEB.
8. Validate its Debian metadata:
   - package: `com.huami.dyyy`
   - architecture: `iphoneos-arm64e`
9. Rename the artifact with the package version and `roothide` suffix when needed.
10. Upload the DEB as a GitHub Actions artifact.

## Failure Handling

The shell runs with strict error handling. Missing toolchains, compilation errors, zero or multiple DEBs, invalid package metadata, and artifact upload failures all fail the job. Diagnostic output includes the detected package files and Debian metadata without printing secrets.

## Permissions and Security

The workflow uses read-only repository contents permission. It does not require repository secrets and does not write releases, tags, commits, or packages. Third-party actions are pinned to immutable commit revisions during implementation.

## Acceptance Criteria

- Manual execution is available in the Actions tab.
- A successful run produces exactly one downloadable RootHide DEB.
- The DEB reports package `com.huami.dyyy` and architecture `iphoneos-arm64e`.
- Source or packaging changes on `main` trigger the workflow.
- Documentation-only changes do not trigger it.
- Any build or validation error produces a failed job instead of uploading ambiguous output.
