"""Offline behavioral checks: no browser/app access and no real recording."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import unittest

from capture_runtime import Action, Capture


class FakeCapture(Capture):
    def __init__(self, root):
        super().__init__(session="offline-test", output=root,
                         allowed_hosts={"example.test"}, cli="unused")
        self.commands = []

    def check(self):
        return True

    def move(self, *args, **kwargs):
        pass

    def screenshot(self, *args):
        pass

    def call(self, *args, **kwargs):
        self.commands.append(args)
        return {}

    def _verify_clip(self, path, minimum_seconds):
        return {"offline": True}


class CaptureBehavior(unittest.TestCase):
    def test_failure_stops_take_and_logs_abort(self):
        with TemporaryDirectory() as root:
            capture = FakeCapture(root)
            def fail():
                raise RuntimeError("Unexpected panel")
            with patch("capture_runtime.time.sleep"), self.assertRaisesRegex(RuntimeError, "Unexpected panel"):
                capture.take("failed", 1, [Action(0, "open panel", fail)], park=(0, 0))
            self.assertEqual(sum(a[:2] == ("record", "stop") for a in capture.commands), 1)
            log = json.loads((Path(root)/"review/failed-capture.json").read_text())
            self.assertEqual(log["status"], "failed")

    def test_existing_take_never_starts_recording(self):
        with TemporaryDirectory() as root:
            capture = FakeCapture(root)
            (Path(root)/"clips/home.mp4").write_bytes(b"approved")
            with self.assertRaisesRegex(RuntimeError, "Existing take preserved"):
                capture.take("home", 1, [], park=(0, 0))
            self.assertEqual(capture.commands, [])
            self.assertEqual((Path(root)/"clips/home.mp4").read_bytes(), b"approved")

    def test_late_action_is_not_performed(self):
        with TemporaryDirectory() as root:
            capture = FakeCapture(root)
            invoked = []
            with patch("capture_runtime.time.sleep"), patch("capture_runtime.time.monotonic", side_effect=[10, 12]):
                with self.assertRaisesRegex(RuntimeError, "Choreography late"):
                    capture.take("late", 1, [Action(0, "click", lambda: invoked.append(True))], park=(0, 0))
            self.assertEqual(invoked, [])
            self.assertIn(("record", "stop"), capture.commands)

    def test_disallowed_click_has_no_browser_call(self):
        with TemporaryDirectory() as root:
            capture = FakeCapture(root)
            with self.assertRaisesRegex(RuntimeError, "allowlist"):
                capture.click("#dispatch")
            self.assertEqual(capture.commands, [])

    def test_successful_take_records_action_times(self):
        with TemporaryDirectory() as root:
            capture = FakeCapture(root)
            with patch("capture_runtime.time.sleep"):
                log = capture.take("success", 1, [Action(0, "hold", lambda: None)], park=(0, 0))
            self.assertEqual(log["status"], "passed")
            self.assertIn("start", log["actions"][0])
            self.assertIn("end", log["actions"][0])
            self.assertIn(("record", "stop"), capture.commands)


if __name__ == "__main__":
    unittest.main()
