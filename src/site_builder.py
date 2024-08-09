from pathlib import Path
from markdown_parser import MarkdownProcessor
from template_engine import TemplateEngine


class SiteBuilder:
    def __init__(self, config):
        self.config = config
        self.markdown_processor = MarkdownProcessor()
        self.template_engine = TemplateEngine(config=config)

    def build(self):
        docs_dir = Path(self.config["docs_dir"])
        site_dir = Path(self.config["site_dir"])
        site_dir.mkdir(parents=True, exist_ok=True)

        # Process homepage
        homepage = docs_dir / self.config.get("homepage", "homepage.md")
        if homepage.exists():
            self.process_markdown_file(homepage, site_dir / "index.html")
        else:
            print(f"Warning: Homepage not found at {homepage}")

        # Process other pages
        for markdown_file in docs_dir.glob("**/*.md"):
            if markdown_file != homepage:
                self.process_markdown_file(markdown_file, site_dir)

    def process_markdown_file(self, markdown_file, output_dir):
        try:
            with open(markdown_file, "r", encoding="utf-8") as f:
                markdown_content = f.read()
            html_content = self.markdown_processor.process(markdown_content)
            page_content = self.template_engine.render_page(
                html_content, title=markdown_file.stem
            )

            if isinstance(output_dir, Path) and output_dir.suffix == ".html":
                output_file = output_dir
            else:
                relative_path = markdown_file.relative_to(self.config["docs_dir"])
                output_file = output_dir / relative_path.with_suffix(".html")

            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(page_content)
            print(f"Processed: {markdown_file} -> {output_file}")
        except Exception as e:
            print(f"Error processing {markdown_file}: {str(e)}")


if __name__ == "__main__":
    from config import Config

    config = Config()
    builder = SiteBuilder(config)
    builder.build()
