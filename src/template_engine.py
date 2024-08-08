import os
from string import Template
from pathlib import Path


class TemplateEngine:
    def __init__(self, config):
        self.config = config
        self.base_template = self.load_base_template()

    def load_base_template(self):
        template_path = Path(self.config["theme_dir"]) / "base.html"
        if not template_path.exists():
            print(f"Warning: Base template not found: {template_path}")
            return Template(self.default_template())

        with open(template_path, "r") as file:
            return Template(file.read())

    def default_template(self):
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${title} - ${site_name}</title>
        </head>
        <body>
            <header>
                <h1>${site_name}</h1>
            </header>
            <main>
                ${content}
            </main>
            <footer>
                <p>&copy; ${site_name}</p>
            </footer>
        </body>
        </html>
        """

    def render_page(self, content, title=""):
        return self.base_template.safe_substitute(
            title=title,
            content=content,
            site_name=self.config.get("site_name", "My AFMDocs Site"),
        )


if __name__ == "__main__":
    # Test the TemplateEngine
    from config import Config

    config = Config()
    engine = TemplateEngine(config)

    # Simulate rendering a page
    content = "<h1>Test Page</h1><p>This is a test.</p>"
    rendered = engine.render_page(content, title="Test Page")
    print(rendered)
