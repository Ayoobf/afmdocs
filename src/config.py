import toml
from pathlib import Path


class Config:
    def __init__(self, config_file="../afmdocs.toml") -> None:
        self.config_file = Path(config_file)
        self.config = self.load_config()

    def load_config(self):
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        with open(self.config_file, "r") as f:
            return toml.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config


if __name__ == "__main__":
    config = Config()
    print(config.get("name"))
    print(config["name"])
