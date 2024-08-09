from pathlib import Path
from markdown_parser import MarkdownProcessor
from template_engine import TemplateEngine


class SiteBuilder:
    def __init__(self, config):
        self.config = config
        self.markdown_processor = MarkdownProcessor()
        self.template_engine = TemplateEngine(self.config["theme_dir"])

    def build(self):
        for md_file in Path(self.config["docs_dir"]).glob("**/*.md"):
            self.process_file(md_file)

    def process_file(self, md_file):
        with open(md_file, "r") as f:
            md_content = f.read()

        html_content = self.markdown_processor.process(md_content)

        context = {"content": html_content, "config": self.config}

        final_html = self.template_engine.render("main.html", context=context)

        output_path = Path(self.config["site_dir"]) / md_file.relative_to(
            self.config["docs_dir"]
        ).with_suffix(".html")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(final_html)


if __name__ == "__main__":
    from config import Config

    config = Config()
    builder = SiteBuilder(config)
    builder.build()
