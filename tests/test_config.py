import unittest
from pathlib import Path
from src.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_config_file = Path("test_mkdocs.yml")
        with open(self.test_config_file, "w") as f:
            f.write("""
            site_name: Test Site
            docs_dir: docs
            """)

    def tearDown(self):
        self.test_config_file.unlink()

    def test_config_loading(self):
        config = Config(self.test_config_file)
        self.assertEqual(config.get("site_name"), "Test Site")
        self.assertEqual(config["docs_dir"], "docs")
        self.assertIn("site_name", config)
        self.assertNotIn("non_existent_key", config)

    def test_missing_config_file(self):
        with self.assertRaises(FileNotFoundError):
            Config("non_existent_file.yml")


if __name__ == "__main__":
    unittest.main()
