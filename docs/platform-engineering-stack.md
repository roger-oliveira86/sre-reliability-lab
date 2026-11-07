# Platform Engineering Stack — Incremental Blueprint

**Status:** Incremental architecture. The Python service, container runtime, CI, vulnerability scanning and manual GHCR publication have been verified. Kubernetes deployment and the wider platform have not been demonstrated.

## Purpose

Show how a development team can deliver a service safely, observe its behavior, and recover from a controlled failure. The platform's customer is the developer; the product is a repeatable, low-friction path to production-like practices in a **disposable lab**.

## Target architecture (not yet deployed)

```text
Developer -> GitHub PR -> CI checks -> OCI image (GHCR)
                                   |
                                   v
                         GitOps desired state (Git)
                                   |
                                   v
                             Argo CD (future)
                                   |
                                   v
                           Disposable Kubernetes
                                   |
                  +----------------+----------------+
                  |                                 |
             Prometheus (future)               OpenTelemetry (future)
                  |                                 |
                  +--------------> Grafana <--------+
                                     |
                            SLI/SLO + runbooks
```

## Stack and stages

| Layer | Choice | Status | Evidence required to call it complete |
|---|---|---|---|
| Application | Python stdlib HTTP demo | **Implemented** | Unit tests and local endpoints |
| Container | Non-root Alpine image pinned by digest | **Built and tested** | Health, metrics and UID 10001 verified |
| Orchestration | Kubernetes Deployment + Service | **Specified, runtime unverified** | Ready rollout and cleanup in disposable cluster |
| CI | GitHub Actions tests, smoke test and Trivy | **Implemented and verified** | Successful required PR check |
| Container registry | GHCR manual publishing | **Implemented and verified** | Published image digest and successful security scan |
| GitOps | Argo CD | **Planned** | Synced application and documented rollback |
| Telemetry | Prometheus + OTel Collector | **Planned** | Measured metrics/traces with known test load |
| Visualization | Grafana | **Planned** | Redacted dashboard screenshots from a real lab |
| Reliability | SLI/SLO, error budget, alert/runbook | **Design stage** | Recorded incident drill and review |
| Policy | Kyverno or Gatekeeper | **Optional** | Enforced policy with positive/negative tests |
| Developer portal | Backstage | **Optional / later** | One software component registered and documented |
| Infra provisioning | OpenTofu/Terraform | **Optional / later** | Reproducible isolated infra with cost controls |

## Roadmap without deadlines

1. **Foundation:** clean tests, CI, rootless container, read-only token, immutable action references; verify Kubernetes manifest schema as a separate check.
2. **Delivery:** publish image under your GitHub account after reviewing provenance and security; keep manifests on a feature branch and use a PR.
3. **GitOps:** introduce Argo CD only after the application works independently; document sync, drift, and rollback.
4. **Observability:** add Prometheus scrape configuration, then OpenTelemetry Collector and Grafana, proving each signal individually.
5. **Reliability:** choose service-level indicators, induce a controlled failure, capture timeline and postmortem evidence.
6. **Platform product:** document the golden path for a second developer; consider Backstage only if it removes demonstrable friction.

## Guardrails

- No lab commands against production or employer environments; no secrets or customer data in Git.
- Avoid cluster resources and cloud expenses until a disposable runtime and cost cap are defined.
- Keep GitHub workflows least-privileged; no push to main; all changes via PR.
- Do not call a tool part of the implemented stack until its execution has been demonstrated.
- Preserve attribution and licenses for any components adopted later.

## Official references

- [Argo CD](https://argo-cd.readthedocs.io/en/stable/)
- [OpenTelemetry Collector on Kubernetes](https://opentelemetry.io/docs/platforms/kubernetes/helm/collector/)
- [Backstage](https://backstage.io/docs/)
- [Prometheus](https://prometheus.io/docs/introduction/overview/)
- [GitHub Actions security](https://docs.github.com/en/actions/security-for-github-actions)
