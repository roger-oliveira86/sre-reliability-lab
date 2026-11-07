# GHCR publication — controlled, manual release

**Status:** Proposed workflow; it only becomes available after this change is merged into `main`. A green PR CI run does **not** mean an image has been published.

## Why manual publishing?

Image publication is separate from PR validation. This workflow is started deliberately from the protected `main`, never from a feature branch. The release tag identifies a Git commit (`sha-<12 chars>`), avoiding a mutable `latest` tag.

## Release procedure

1. Review the PR, check the required `checks` job and squash-merge into protected `main`.
2. Run `gh workflow run publish-ghcr.yml --repo roger-oliveira86/sre-reliability-lab --ref main`.
3. Run `gh run list --repo roger-oliveira86/sre-reliability-lab --workflow publish-ghcr.yml --limit 3` and inspect the successful run summary for the published digest.
4. Confirm the package is associated with the correct GitHub repository. GHCR packages may initially be **private**; review visibility and package access under GitHub Packages. Do not assume public access.
5. Use `ghcr.io/roger-oliveira86/sre-reliability-lab@sha256:<verified-digest>` when updating `k8s/deployment.yaml` **in a separate PR**. The placeholder in the current manifest is intentionally left unchanged.
6. Test the image in a disposable cluster, capture the rollout, and record cleanup. Do not use a production cluster.

## Security and scope

- The publisher uses `GITHUB_TOKEN`, not a stored personal access token, and grants `packages: write` **only to the publish job**.
- Checkout is pinned to a full commit SHA. The workflow cannot publish from a PR ref.
- Image release does not currently include a vulnerability scan, signed provenance, SBOM, or a runtime Kubernetes smoke test. These remain follow-up controls rather than implied guarantees.
- The existing PR validation runs on all PRs and is required by the `main` ruleset.
