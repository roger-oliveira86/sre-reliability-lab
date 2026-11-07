"""Small observability demonstration using only Python's standard library."""
import json
import os
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5)

class Metrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.counts = {}
        self.durations = {}

    def observe(self, method, route, status, duration):
        key = (method, route, str(status))
        hist_key = (method, route)

        with self.lock:
            self.counts[key] = self.counts.get(key, 0) + 1

            hist = self.durations.setdefault(
                hist_key,
                {
                    "count": 0,
                    "sum": 0.0,
                    "buckets": [0] * len(BUCKETS),
                },
            )

            hist["count"] += 1
            hist["sum"] += duration

            for i, bound in enumerate(BUCKETS):
                if duration <= bound:
                    hist["buckets"][i] += 1

    def render(self):
        with self.lock:
            counts = dict(self.counts)
            durations = {
                key: {
                    "count": value["count"],
                    "sum": value["sum"],
                    "buckets": value["buckets"].copy(),
                }
                for key, value in self.durations.items()
            }

        rows = [
            "# HELP demo_http_requests_total Total HTTP requests.",
            "# TYPE demo_http_requests_total counter",
        ]

        for (method, route, status), value in sorted(counts.items()):
            rows.append(
                f'demo_http_requests_total{{method="{method}",'
                f'route="{route}",status="{status}"}} {value}'
            )

        rows += [
            "# HELP demo_http_duration_seconds Request latency in seconds.",
            "# TYPE demo_http_duration_seconds histogram",
        ]

        for (method, route), hist in sorted(durations.items()):
            labels = f'method="{method}",route="{route}"'

            for bound, count in zip(BUCKETS, hist["buckets"]):
                rows.append(
                    f'demo_http_duration_seconds_bucket'
                    f'{{{labels},le="{bound}"}} {count}'
                )

            rows.append(
                f'demo_http_duration_seconds_bucket'
                f'{{{labels},le="+Inf"}} {hist["count"]}'
            )
            rows.append(
                f'demo_http_duration_seconds_sum'
                f'{{{labels}}} {hist["sum"]:.9f}'
            )
            rows.append(
                f'demo_http_duration_seconds_count'
                f'{{{labels}}} {hist["count"]}'
            )

        return "\n".join(rows) + "\n"

METRICS = Metrics()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        start = time.perf_counter()
        route = urlsplit(self.path).path
        request_id = str(uuid.uuid4())
        status = 200
        if route == '/healthz':
            body = b'{"status":"ok"}\n'
            content_type = 'application/json'
        elif route == '/metrics':
            body = METRICS.render().encode('utf-8')
            content_type = 'text/plain; version=0.0.4; charset=utf-8'
        elif route == '/':
            body = b'{"service":"sre-reliability-lab","status":"ok"}\n'
            content_type = 'application/json'
        elif route == '/failure' and os.getenv('ENABLE_FAILURE_ENDPOINT') == 'true':
            status = 500
            body = b'{"error":"controlled_failure"}\n'
            content_type = 'application/json'
        else:
            status = 404
            body = b'{"error":"not_found"}\n'
            content_type = 'application/json'
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Request-ID', request_id)
        self.end_headers()
        self.wfile.write(body)
        duration = max(time.perf_counter() - start, 0)
        if route != '/metrics':
            METRICS.observe('GET', route if route in ('/', '/healthz', '/failure') else 'unmatched', status, duration)
            print(json.dumps({'event':'request','request_id':request_id,'route':route,'status':status,'duration_ms':round(duration*1000,3)}), flush=True)

    def log_message(self, format, *args):
        pass  # avoid duplicating structured request logs


def main():
    port = int(os.getenv('PORT', '8080'))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(json.dumps({'event': 'start', 'port': port}), flush=True)
    server.serve_forever()

if __name__ == '__main__':
    main()
