import os
from string import Template


class TemplateEngine:
    def __init__(self, config) -> None:
        self.config = config
        self.base_template = self.load_base_template()

    def load_base_template(self):
        template_path = os.path.join(self.config["theme_dir"], "base.html")
        with open(template_path, "r") as file:
            return Template(file.read())

    def render_page(self, content, title=""):
        return self.base_template.safe_substitute(
            title=title,
            content=content,
            site_name=self.config.get("site_name", ""),
        )


if __name__ == "__main__":
    from config import Config

    config = Config()
    engine = TemplateEngine(config)

    # Simulate rendering a page
    content = "<h1>Test Page</h1><p>This is a test.</p>"
    rendered = engine.render_page(content, title="Test Page")
    print(rendered)
