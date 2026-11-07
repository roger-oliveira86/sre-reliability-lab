# SRE Reliability Lab

An original, minimal reliability lab focused on **measurable service behavior**, safe failure simulation, and evidence-driven operations. Created independently; it does not reproduce the contents of any third-party course or fork.

## What works today

- A dependency-free Python HTTP service with `/healthz`, `/metrics`, `/`, and opt-in `/failure` endpoints.
- Prometheus-compatible request counters and a latency histogram.
- Structured JSON request logs and a generated request ID.
- Unit tests, a non-root container image, and example Kubernetes manifests.
- GitHub Actions validates Python syntax, unit tests, basic Kubernetes YAML syntax, container smoke tests and vulnerabilities (not Kubernetes runtime behavior).

This is a **starting laboratory**, not a complete SRE platform or a production-ready service. No tracing stack, dashboards, alert delivery, or live Kubernetes execution is claimed.

## Platform Engineering roadmap

See [the incremental stack blueprint](docs/platform-engineering-stack.md) and [publication checklist](docs/publication-checklist.md). GitOps, OpenTelemetry and Backstage remain future stages. GHCR publication is implemented and manually triggered.


## Verified container delivery

The Python service runs in a non-root Alpine-based container,
with the base image pinned by digest.

GitHub Actions validates Python tests, Kubernetes YAML syntax,
container builds and HTTP smoke tests.

Trivy scans container images during PR validation and before
manual GHCR publication. CRITICAL findings block the workflow;
HIGH findings are reported.

Verified GHCR release (November 7, 2026):

`ghcr.io/roger-oliveira86/sre-reliability-lab@sha256:4b6013f5ac28b109fbcba868dec2239786c13ce2bfa4f00d20d3bc29d5a60517`

The published image passed a HIGH/CRITICAL vulnerability scan
with zero findings. This does not establish that the image is
free of all security risks.

Kubernetes runtime deployment, GitOps, tracing and dashboards
have not been demonstrated.

## Architecture

```text
HTTP client -> Python service -> JSON logs (stdout)
                              -> /metrics (Prometheus text)
                              -> /healthz (Kubernetes probe)
```

## Run without Docker

```bash
python3 -m unittest discover -s tests -v
python3 -m src.service
# in another terminal
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS http://127.0.0.1:8080/metrics
```

To simulate HTTP 500s, explicitly opt in: `ENABLE_FAILURE_ENDPOINT=true python3 -m src.service`, then call `/failure`. Never enable the failure route on a real service.

## Container and Kubernetes

Build locally with `docker build -t sre-reliability-lab:local .`. The example Deployment uses the placeholder image `ghcr.io/YOUR_USERNAME/sre-reliability-lab:VERSION`; **replace it with a published image under your control** before applying the manifests. Work in an isolated disposable cluster only:

```bash
kubectl config current-context
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl -n sre-reliability-lab rollout status deployment/reliability-demo
kubectl delete namespace sre-reliability-lab
```

Do not use production credentials or clusters. Inspect files and context before applying. Kubernetes resources have not been runtime-tested by this starter's authoring workflow.

## Operational guidance

See [service runbook](docs/runbook.md), [experiment protocol](docs/experiment.md), and [postmortem template](docs/postmortem-template.md). Keep real screenshots and results only when captured during an actual reproducible experiment.

## Scope and provenance

This repository is an independent original project and is not a fork or republication of `alanmosilva/sre-observability-course`. The structure and code here were created anew. Do not add third-party scripts, dashboards or images without checking their licenses and attribution requirements.

## License

Apache-2.0. See [LICENSE](LICENSE).
