from pathlib import Path
from markdown_parser import MarkdownProcessor
from template_engine import TemplateEngine


class SiteBuilder:
    def __init__(self, config):
        """
        Initialize the SiteBuilder with configuration.

        :param config: Configuration object containing site settings
        """
        self.config = config
        # Initialize the Markdown processor for converting Markdown to HTML
        self.markdown_processor = MarkdownProcessor()
        # Initialize the template engine with the theme directory from config
        self.template_engine = TemplateEngine(self.config["theme_dir"])

    def build(self):
        """
        Build the entire site by processing all Markdown files in the docs directory.
        """
        # Iterate through all .md files in the docs directory and its subdirectories
        for md_file in Path(self.config["docs_dir"]).glob("**/*.md"):
            self.process_file(md_file)

    def process_file(self, md_file):
        """
        Process a single Markdown file and generate the corresponding HTML file.

        :param md_file: Path object pointing to the Markdown file
        """
        # Read the content of the Markdown file
        with open(md_file, "r") as f:
            md_content = f.read()

        # Convert Markdown content to HTML
        html_content = self.markdown_processor.process(md_content)

        # Prepare the context for the template engine
        context = {"content": html_content, "config": self.config}

        # Render the final HTML using the main template
        final_html = self.template_engine.render("main.html", context=context)

        # Determine the output path for the HTML file
        output_path = Path(self.config["site_dir"]) / md_file.relative_to(
            self.config["docs_dir"]
        ).with_suffix(".html")

        # Create necessary directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the final HTML to the output file
        with open(output_path, "w") as f:
            f.write(final_html)


if __name__ == "__main__":
    # This block is executed when the script is run directly
    from config import Config

    # Load the configuration
    config = Config()
    # Create a SiteBuilder instance
    builder = SiteBuilder(config)
    # Build the site
    builder.build()
