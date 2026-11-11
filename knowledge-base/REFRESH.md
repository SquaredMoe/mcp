# Refresh and validation playbook

## Status and evidence levels

- **Verified:** Repository exists at `SquaredMoe/<name>`; GitHub metadata (public/fork/parent/default branch); top-level files/directories; README opening content viewed on 2026-11-11.
- **Described:** Repository purpose comes from project metadata/README and is not an independent technical evaluation.
- **Hypothesis:** Cross-repository workflows in [RELATIONSHIPS.md](RELATIONSHIPS.md). No integration is asserted.
- **Not done:** Full code audit, commit-by-commit upstream comparison, complete dependency/SBOM inventory, runtime execution, security assessment, license-compatibility review, verification of deployed environments, and reading of every source file.

## Suggested quarterly refresh

1. Re-list all repositories accessible to the GitHub account; identify new, deleted, archived, or newly private projects before publishing a refreshed index.
2. For each repository, read `GET /repos/SquaredMoe/<repo>` metadata (default branch, fork and parent, pushed timestamp), its root contents, and the README.
3. Inspect manifests and lockfiles for actual dependency and language information; record verified versions and source paths.
4. Compare the fork to upstream to find custom code and synchronization gaps.
5. Update repository rows, topic mapping, and any validated architecture diagrams; date each revision.
6. Review changes for confidential information **before** publishing to any public branch. Don't index API tokens, private configuration, proprietary code, or personal data.

## Template for a deep-dive

```markdown
# <repository>
As reviewed: YYYY-MM-DD | Fork: SquaredMoe/<repo> | Upstream: <owner/repo>
Scope: <branch/SHA and files inspected>
Purpose: <brief verified description>
Languages and frameworks: <manifest-backed facts>
Architecture: <components and interactions based on source>
Entrypoints and key files: <links>
Build and test: <documented commands; clearly mark if untested>
Security and privacy considerations: <evidence and unknowns>
Differences from upstream: <verified compare result>
Open questions: <unknowns>
Related repos: <confirmed integrations vs ideas>
```

## Suggested future-chat prompt

> Use the GitHub connector to read `SquaredMoe/mcp` branch `docs/github-knowledge-base-2026-11-11`, starting at `knowledge-base/README.md`. Treat it as a dated directory, not durable model memory. Recheck current repository state for the specific project before making claims or code changes.
