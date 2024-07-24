import re
import os
import sys


class MarkdownProcessor:
    def __init__(self):
        self.rules = [
            # Regex rules go here with form (regex, method)
            (r"^(#{1,6})\s(.+)$", self.process_headers)
        ]

    """reads text, splits it up, and applies rules as needed
    """

    def process(self, text):
        lines = text.split("\n")
        processed_lines = [self.apply_rules(line) for line in lines]
        return "\n".join(processed_lines)

    """applies the regex rules as defined above to each line
    """

    def apply_rules(self, line):
        for pattern, handler in self.rules:
            match = re.match(pattern, line)
            if match:
                return handler(match)
        return line  # Return the line unchanged if no rules match

    # Basic Markdown elements
    def process_headers(self, match):
        level = len(match.group(1))  # Number of '#' symbols
        content = match.group(2)  # Header text
        return f"<h{level}>{content}</h{level}>"

    def process_paragraphs(self, text):
        pass

    def process_bold(self, text):
        pass

    def process_italic(self, text):
        pass

    def process_code(self, text):
        pass

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

    # Utility methods
    def escape_html(self, text):
        pass

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
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define input and output file paths
    input_file = os.path.join(current_dir, "test.md")
    output_file = os.path.join(current_dir, "output.html")

    # Process the Markdown file
    mdp.process_markdown_file(input_file, output_file)
