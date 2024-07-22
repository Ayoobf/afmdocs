import unittest
from pathlib import Path
from src.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_config_file = Path("test_afmdocs.toml")
        with open(self.test_config_file, "w") as f:
            f.write("""
            name = "afmdocs"
            version = "0.1.0"
            description = "A test package for pip configuration"
            authors = ["Your Name <your.email@example.com>"]
            """)

    def tearDown(self):
        self.test_config_file.unlink()

    def test_config_loading(self):
        config = Config(self.test_config_file)
        self.assertEqual(config.get("name"), "afmdocs")
        self.assertEqual(config["version"], "0.1.0")
        self.assertIn("name", config)
        self.assertNotIn("non_existent_key", config)

    def test_missing_config_file(self):
        with self.assertRaises(FileNotFoundError):
            Config("non_existent_file.toml")


if __name__ == "__main__":
    unittest.main()
