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
            (r"`([^`\n]+)`", self.process_inline_code, 0),
            (r"```([\w-]+)?\n([\s\S]+?)\n```", self.process_fenced_code_block, 0),
            (r"((?:(?:^|\n)(?:    |\t).*)+)", self.process_indented_code_block, 0),
            (r"!\[([^\]]+)\]\(([^\)]+)\)", self.process_images, 0),
            (r"\[([^\]]+)\]\(([^\)]+)\)", self.process_links, 0),
            (
                r"^(?:(?:\*{3,})|(?:-{3,})|(?:_{3,}))$",
                self.process_horizontal_rules,
                re.MULTILINE,
            ),
            (
                r"(?<![^\n])\n?(?!#|\s*[-*+]|\s*\d+\.|\s*>)(.+?)(?:\n\n|\n?$)",
                self.process_paragraphs,
                0,
            ),
        ]
        self.list_item_count = 0

    # Horizontal rules
    def process_horizontal_rules(self, match):
        return "<hr>"  # simple lol

    def pre_process_tables(self, text):
        def process_table(match):
            rows = match.group(0).strip().split("\n")
            header = rows[0]
            body = rows[2:]

            header_cells = [cell.strip() for cell in header.strip("|").split("|")]
            header_html = (
                "<thead><tr>"
                + "".join(f"<th>{cell}</th>" for cell in header_cells)
                + "</tr></thead>"
            )

            body_html = "<tbody>"
            for row in body:
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                if len(cells) == len(header_cells):
                    body_html += (
                        "<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>"
                    )
            body_html += "</tbody>"

            return f"<table>\n{header_html}\n{body_html}\n</table>"

        # Pattern to match Markdown tables
        pattern = r"^\|(.+\|)+\n\|(?:[-:| ]+\|)+\n((?:\|(?:.+\|)+\n?)+)"
        return re.sub(pattern, process_table, text, flags=re.MULTILINE)

    def pre_process_ordered_lists(self, text):
        def replace_list(match):
            items = re.findall(
                r"^\d+\.\s(.+(?:\n(?!\d+\.).*)*)", match.group(0), re.MULTILINE
            )
            processed_items = [f"<li>{item.strip()}</li>" for item in items]
            return f"<ol>\n{''.join(processed_items)}\n</ol>"

        pattern = r"(?:^\d+\..*(?:\n(?!\s*\n|\d+\.).*)*\n?)+"
        return re.sub(pattern, replace_list, text, flags=re.MULTILINE)

    def pre_process_unordered_lists(self, text):
        def replace_list(match):
            items = re.findall(
                r"^[-*+]\s(.+(?:\n(?![-*+]\s).*)*)", match.group(0), re.MULTILINE
            )
            if not items:  # If no items found, don't create an empty list
                return match.group(0)
            processed_items = [f"<li>{item.strip()}</li>" for item in items]
            return f"<ul>\n{''.join(processed_items)}\n</ul>"

        pattern = r"(?:^[-*+].*(?:\n(?!\s*\n|[-*+]).*)*\n?)+"
        return re.sub(pattern, replace_list, text, flags=re.MULTILINE)

    def pre_process_blockquotes(self, text):
        def replace_blockquote(match):
            content = match.group(1).replace("\n>", "\n").strip()
            processed_content = self.apply_rules(content)
            return f"<blockquote>\n{processed_content}\n</blockquote>"

        pattern = r"((?:^>.*\n?)+)"
        return re.sub(pattern, replace_blockquote, text, flags=re.MULTILINE)

    # reads text, splits it up, and applies rules as needed
    def process(self, text):
        # Pre-process the text to handle tables, blockquotes, and lists
        text = self.pre_process_tables(text)
        text = self.pre_process_blockquotes(text)
        text = self.pre_process_ordered_lists(text)
        text = self.pre_process_unordered_lists(text)

        # Process the rest of the text
        blocks = re.split(r"\n{2,}", text)
        processed_blocks = []
        for block in blocks:
            if block.strip():
                if block.startswith("<table>") and block.endswith("</table>"):
                    processed_blocks.append(block)
                elif re.match(r"^(?:(?:\*{3,})|(?:-{3,})|(?:_{3,}))$", block):
                    processed_blocks.append(self.process_horizontal_rules(block))
                else:
                    processed_blocks.append(self.apply_rules(block.strip()))
        return "\n\n".join(processed_blocks)

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

    def process_inline_code(self, match):
        return f"<code>{self.escape_html(match.group(1))}</code>"

    # Links and images
    def process_links(self, match):
        link_text = match.group(1)
        link_url = match.group(2)
        return f'<a href="{self.escape_html(link_url)}">{link_text}</a>'

    def process_images(self, match):
        alt_text = match.group(1)
        image_url = match.group(2)

        return f'<img src="{self.escape_html(image_url)}" alt="{self.escape_html(alt_text)}">'

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
# Table Example

Here's a simple table:

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
| Row 3, Col 1 | Row 3, Col 2 | Row 3, Col 3 |

---

And here's some text after a horizontal rule.

"""
    html_output = mdp.process(markdown_text)
    print(html_output)
