"""Comprobaciones sin iniciar ni conectar Discord."""
import json
import tempfile
import unittest
from pathlib import Path

from main import load_config, make_activity


def example():
    return {
        "client_id": "123456789012345678",
        "game": "Grand Theft Auto VI",
        "details": "Jugando en PlayStation 5",
        "state": "PS5 | GTA VI",
        "large_image": "",
        "large_text": "GTA VI",
        "elapsed_hours": 357044,
        "refresh_seconds": 60,
        "retry_seconds": 15,
    }


class TestConfig(unittest.TestCase):
    def load(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return load_config(path)

    def test_valid(self):
        self.assertEqual(self.load(example())["game"], "Grand Theft Auto VI")

    def test_requires_client_id(self):
        data = example()
        data["client_id"] = "PON_AQUI_TU_APPLICATION_ID"
        with self.assertRaises(ValueError):
            self.load(data)

    def test_avoids_excessive_updates(self):
        data = example()
        data["refresh_seconds"] = 1
        with self.assertRaises(ValueError):
            self.load(data)

    def test_no_artwork(self):
        activity = make_activity(example(), 12345)
        self.assertEqual(activity["name"], "Grand Theft Auto VI")
        self.assertEqual(activity["details"], "Jugando en PlayStation 5")
        self.assertEqual(activity["start"], 12345)
        self.assertNotIn("large_image", activity)

    def test_artwork(self):
        data = example()
        data["large_image"] = "gta6"
        activity = make_activity(data, 12345)
        self.assertEqual(activity["large_image"], "gta6")


if __name__ == "__main__":
    unittest.main()
