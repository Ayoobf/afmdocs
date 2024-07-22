import yaml
from pathlib import Path


class Config:
    def __init__(self, config_file="mkdocs.yml") -> None:
        self.config_file = Path(config_file)
        self.config = self.load_config()

    def load_config(self):
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        with open(self.config_file, "r") as f:
            return yaml.safe_load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config


if __name__ == "__main__":
    config = Config()
    print(config.get("site_name"))
    print(config["docs_dir"])
