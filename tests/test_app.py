import json
import os
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.request


class ApplicationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(
            [sys.executable, "app/app.py"],
            env={**os.environ, "APP_VERSION": "test-version"},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        for _ in range(50):
            try:
                with urllib.request.urlopen(
                    "http://127.0.0.1:8080/healthz",
                    timeout=1,
                ):
                    break
            except Exception:
                time.sleep(0.1)
        else:
            cls.process.terminate()
            cls.process.wait(timeout=5)
            raise RuntimeError("Application did not start")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=5)

    def get_json(self, path):
        with urllib.request.urlopen(
            "http://127.0.0.1:8080" + path,
            timeout=2,
        ) as response:
            return response.status, json.loads(
                response.read().decode("utf-8")
            )

    def test_homepage(self):
        status, body = self.get_json("/")

        self.assertEqual(status, 200)
        self.assertEqual(
            body["service"],
            "friendly-neighborhood-watch",
        )
        self.assertEqual(body["hero"], "Spider-Man")
        self.assertEqual(body["version"], "test-version")

    def test_health(self):
        status, body = self.get_json("/healthz")

        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "alive")

    def test_readiness(self):
        status, body = self.get_json("/readyz")

        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ready")

    def test_missing_page(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.get_json("/does-not-exist")

        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()

