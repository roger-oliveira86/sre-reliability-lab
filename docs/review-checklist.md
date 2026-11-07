# GHCR PR review checklist

- [ ] Change contains only the manual GHCR publisher, its instructions and a container-build CI smoke test.
- [ ] GitHub Actions `checks` job passes including the container smoke test.
- [ ] Publisher uses packages:write only on the manually dispatched job, limited to main.
- [ ] Workflow does not push on PRs and does not modify Kubernetes Deployment image references.
- [ ] No credentials, screenshots or production infrastructure information committed.
- [ ] Review after merge: manually publish and verify returned digest/package visibility.
