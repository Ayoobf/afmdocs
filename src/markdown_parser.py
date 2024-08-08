import re
import sys


class MarkdownProcessor:

    def __init__(self):
        self.rules = [
            (r"^(#{1,6})\s(.+)$", self.process_headers, re.MULTILINE),
            (
                r"(\*\*\*([^\*\n]+)\*\*\*)|(\_\_\_([^\*\n]+)\_\_\_)",
                self.process_bold_italic,
                0,
            ),
            (r"(\*\*([^\*\n]+)\*\*)|(\_\_([^\*\n]+)\_\_)", self.process_bold, 0),
            (r"(\*([^\*\n]+)\*)|(\_([^\*\n]+)\_)", self.process_italic, 0),
            (r"```([\w-]+)?\n([\s\S]+?)\n```", self.process_fenced_code_block, 0),
            (r"((?:(?:^|\n)(?:    |\t).*)+)", self.process_indented_code_block, 0),
            (
                r"(?<![^\n])\n?(?!#|\s*[-*+]|\s*\d+\.|\s*>)(.+?)(?:\n\n|\n?$)",
                self.process_paragraphs,
                0,
            ),
        ]
        self.list_item_count = 0

    # reads text, splits it up, and applies rules as needed
    def process(self, text):
        # Pre-process the text to handle ordered lists
        text = self.pre_process_ordered_lists(text)

        # Process the rest of the text
        blocks = re.split(r"\n{2,}", text)
        processed_blocks = [
            self.apply_rules(block.strip()) for block in blocks if block.strip()
        ]
        return "\n\n".join(processed_blocks)

    def pre_process_ordered_lists(self, text):
        def replace_list(match):
            items = re.findall(
                r"^\d+\.\s(.+(?:\n(?!\d+\.).*)*)", match.group(0), re.MULTILINE
            )
            processed_items = [f"<li>{item.strip()}</li>" for item in items]
            return f"<ol>\n{''.join(processed_items)}\n</ol>"

        pattern = r"(?:^\d+\..*(?:\n(?!\s*\n|\d+\.).*)*\n?)+"
        return re.sub(pattern, replace_list, text, flags=re.MULTILINE)

    # applies the regex rules as defined above to each line
    def apply_rules(self, block):
        for pattern, handler, flags in self.rules:
            block = re.sub(pattern, handler, block, flags=flags)
        return block

    # Basic Markdown elements
    def process_headers(self, match):
        level = len(match.group(1))  # Number of '#' symbols
        content = match.group(2)  # Header text
        return f"<h{level}>{content}</h{level}>"

    def process_paragraphs(self, match):
        content = match.group(1)
        # Don't wrap content in <p> tags if it's already wrapped in other tags
        if re.match(r"<\w+[^>]*>", content):
            return content
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

    def process_ordered_list_item(self, match):
        self.list_item_count += 1
        indent = match.group(1)
        content = match.group(2)
        # Process the content of the list item
        processed_content = self.apply_rules(content)
        # Remove any trailing newlines and add indentation
        processed_content = processed_content.rstrip().replace(
            "\n", "\n" + " " * len(indent)
        )
        return f"<li>{processed_content}</li>"

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

1. First item
2. Second item
   with a line break
4. Fourth item
"""
    html_output = mdp.process(markdown_text)
    print(html_output)
