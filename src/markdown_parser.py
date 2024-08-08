import re
import sys


class MarkdownProcessor:
    def __init__(self):
        self.rules = [
            # Regex rules go here with form (regex, method)
            (r"^(#{1,6})\s(.+)$", self.process_headers),
            (
                r"(\*\*\*([^\*\n]+)\*\*\*)|(\_\_\_([^\*\n]+)\_\_\_)",
                self.process_bold_italic,
            ),
            (r"(\*\*([^\*\n]+)\*\*)|(\_\_([^\*\n]+)\_\_)", self.process_bold),
            (r"(\*([^\*\n]+)\*)|(\_([^\*\n]+)\_)", self.process_italic),
            (r"```([\w-]+)?\n([\s\S]+?)\n```", self.process_fenced_code_block),
            (r"((?:(?:^|\n)(?:    |\t).*)+)", self.process_indented_code_block),
            (
                r"(?<![^\n])\n?(?!#|\s*[-*+]|\s*\d+\.|\s*>)(.+?)(?:\n\n|\n?$)",  # what the fuck is this regex btw
                self.process_paragraphs,
            ),
        ]

    # reads text, splits it up, and applies rules as needed
    def process(self, text):
        return re.sub(
            r"(?:^|\n\n)([\s\S]+?)(?:\n\n|$)",
            lambda m: self.apply_rules(m.group(1)),
            text,
        )

    # applies the regex rules as defined above to each line
    def apply_rules(self, block):
        for pattern, handler in self.rules:
            block = re.sub(pattern, handler, block, flags=re.MULTILINE)
        return block

    # Basic Markdown elements
    def process_headers(self, match):
        level = len(match.group(1))  # Number of '#' symbols
        content = match.group(2)  # Header text
        return f"<h{level}>{content}</h{level}>"

    def process_paragraphs(self, match):
        content = match.group(1)
        return f"<p>{content}</p>"

    def process_bold(self, match):
        content = match.group(2) or match.group(4)  # Get content from either ** or __
        return f"<strong>{content}</strong>"

    def process_italic(self, match):
        content = match.group(2) or match.group(4)  # Get content from either * or _
        return f"<em>{content}</em>"

    def process_bold_italic(self, match):
        content = match.group(2) or match.group(4)  # Get content from either *** or ___
        return f"<strong><em>{content}</em></strong>"

    def process_fenced_code_block(self, match):
        language = match.group(1) or ""
        code = match.group(2)
        return f'<pre><code class="language-{language}">{self.escape_html(code)}</code></pre>'

    def process_indented_code_block(self, match):
        code = match.group(1)
        # Remove the indentation
        code = re.sub(r"(?:^|\n)(    |\t)", "\n", code)
        return f"<pre><code>{self.escape_html(code.strip())}</code></pre>"

    # Lists
    def process_unordered_list(self, text):
        pass

    def process_ordered_list(self, text):
        pass

    # Links and images
    def process_links(self, text):
        pass

    def process_images(self, text):
        pass

    # Block elements
    def process_blockquotes(self, text):
        pass

    def process_code_blocks(self, text):
        pass

    # Tables
    def process_tables(self, text):
        pass

    # Horizontal rules
    def process_horizontal_rules(self, text):
        pass

    # MkDocs-specific elements
    def process_admonitions(self, text):
        pass

    def process_footnotes(self, text):
        pass

    def escape_html(self, text):
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def unescape_html(self, text):
        pass

    """reads the target markdown file and starts processing the output
    """

    # This method might just be an internal helper method for testing
    def process_markdown_file(self, input_path, output_path):
        # Read the input Markdown file
        with open(input_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()

        # Process the Markdown content
        html_content = self.process(markdown_content)

        # Write the processed content to an HTML file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        sys.stdout.write(f"Processed {input_path} and saved result to {output_path}\n")
        sys.stdout.flush()


# Example usage
if __name__ == "__main__":
    mdp = MarkdownProcessor()
    markdown_text = """
# Code Blocks Example

Here's a Python code block:

```python
def hello_world():
    print("Hello, World!")
```

And here's an indented code block:

    This is an
    indented code block
    without language specification
"""
    html_output = mdp.process(markdown_text)
    print(html_output)
