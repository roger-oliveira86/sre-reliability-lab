# Controlled failure experiment

Use only on a disposable environment. Record date, Git commit, image digest, cluster version, and test inputs. Never claim an observation that was not measured.

1. Verify the environment and enable the failure route explicitly with `ENABLE_FAILURE_ENDPOINT=true`.
2. Confirm initial health and scrape `/metrics`.
3. Generate a limited number of requests against `/failure`.
4. Compare the `demo_http_requests_total` counters for statuses 200 and 500.
5. Restore normal behavior by disabling the failure route and restarting the disposable service.
6. Record the observed time of fault, detection, mitigation, and restoration.
7. Clean up resources and attach evidence only if collected from the running lab.

Questions: Which signal detects impact? What is the difference between detection and restoration? What might make a synthetic metric misleading?
