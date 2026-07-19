#!/usr/bin/env bash

set -euo pipefail

workflow=${1:-.github/workflows/build.yml}

fail() {
    echo "workflow contract failed: $*" >&2
    exit 1
}

[[ -f "$workflow" ]] || fail "missing $workflow"
grep -Fq 'workflow_dispatch:' "$workflow" || fail "manual trigger missing"
grep -Fq 'contents: read' "$workflow" || fail "read-only contents permission missing"
grep -Eq 'make .*package .*SCHEME=roothide|make .*SCHEME=roothide .*package' "$workflow" || fail "RootHide build command missing"
! grep -Eq 'Build Rootful|Build Rootless|SCHEME=rootless|THEOS_PACKAGE_SCHEME=rootless' "$workflow" || fail "non-RootHide build remains"
grep -Fq 'Expected exactly one RootHide DEB' "$workflow" || fail "single-package validation missing"
grep -Fq 'com.huami.dyyy' "$workflow" || fail "package identity validation missing"
grep -Fq 'iphoneos-arm64e' "$workflow" || fail "architecture validation missing"
grep -Fq 'actions/upload-artifact@' "$workflow" || fail "artifact upload missing"

echo "RootHide workflow contract passed"
