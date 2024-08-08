import toml
from pathlib import Path


class Config:
    def __init__(self, config_file="../afmdocs.toml"):
        self.config_file = Path(config_file)
        self.config = self.load_config()

    def load_config(self):
        if not self.config_file.exists():
            print(f"Warning: Config file not found: {self.config_file}")
            print("Using default configuration.")
            return self.default_config()

        with open(self.config_file, "r") as f:
            return toml.load(f)

    def default_config(self):
        return {
            "site_name": "My AFMDocs Site",
            "theme_dir": "themes/default",
            "docs_dir": "docs",
            "site_dir": "site",
        }

    def get(self, key, default=None):
        return self.config.get(key, default)

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config


if __name__ == "__main__":
    config = Config()
    print("Configuration:")
    for key, value in config.config.items():
        print(f"{key}: {value}")
