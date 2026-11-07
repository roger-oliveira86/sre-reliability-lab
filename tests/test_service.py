import unittest
from src.service import BUCKETS, Metrics

class MetricsTests(unittest.TestCase):
    def test_counter_and_histogram(self):
        m = Metrics()
        m.observe('GET', '/', 200, 0.012)
        m.observe('GET', '/', 500, 0.300)
        data = m.render()
        self.assertIn('status="200"} 1', data)
        self.assertIn('status="500"} 1', data)
        self.assertIn('le="0.025"} 1', data)
        self.assertIn('le="+Inf"} 2', data)
        self.assertIn('demo_http_duration_seconds_count{method="GET",route="/"} 2', data)

    def test_empty_registry(self):
        self.assertIn('demo_http_requests_total', Metrics().render())

    def test_bucket_order(self):
        self.assertEqual(tuple(sorted(BUCKETS)), BUCKETS)

if __name__ == '__main__':
    unittest.main()
