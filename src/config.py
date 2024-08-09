import toml
from pathlib import Path


class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            # Look for the config file in the project root
            self.config_file = self.find_config_file()
        else:
            self.config_file = Path(config_file)

        self.config = self.load_config()
        self.set_defaults()

    def find_config_file(self):
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            config_file = current_dir / "afmdocs.toml"
            if config_file.exists():
                return config_file
            current_dir = current_dir.parent
        raise FileNotFoundError(
            "Config file 'afmdocs.toml' not found in any parent directory"
        )

    def load_config(self):
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        with open(self.config_file, "r") as f:
            return toml.load(f)

    def set_defaults(self):
        # Set default values for Jinja2-related settings
        self.config.setdefault("theme_dir", "themes/default")
        self.config.setdefault("jinja_extensions", [])
        self.config.setdefault("jinja_filters", {})
        self.config.setdefault("docs_dir", "docs")
        self.config.setdefault("site_dir", "site")
        self.config.setdefault("site_name", "My AFMDocs Site")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config


if __name__ == "__main__":
    try:
        config = Config()
        print("Config file found:", config.config_file)
        print("Config contents:", config.config)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(
            "Please ensure 'afmdocs.toml' exists in your project root or any parent directory."
        )
