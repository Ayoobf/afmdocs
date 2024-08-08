import re
import logging


class MarkdownProcessingError(Exception):
    """Custom exception for Markdown processing errors."""

    pass


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
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("MarkdownProcessor")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def process(self, text):
        try:
            self.logger.info("Starting Markdown processing")
            text = self.pre_process_tables(text)
            text = self.pre_process_blockquotes(text)
            text = self.pre_process_ordered_lists(text)
            text = self.pre_process_unordered_lists(text)

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
            self.logger.info("Markdown processing completed successfully")
            return "\n\n".join(processed_blocks)
        except Exception as e:
            self.logger.error(f"An error occurred during Markdown processing: {str(e)}")
            raise MarkdownProcessingError(f"Failed to process Markdown: {str(e)}")

    def apply_rules(self, block):
        try:
            for pattern, handler, flags in self.rules:
                block = re.sub(pattern, handler, block, flags=flags)
            return block
        except Exception as e:
            self.logger.error(f"Error applying rules to block: {str(e)}")
            raise MarkdownProcessingError(f"Failed to apply rules: {str(e)}")

    def process_headers(self, match):
        try:
            level = len(match.group(1))
            content = match.group(2)
            return f"<h{level}>{content}</h{level}>"
        except Exception as e:
            self.logger.error(f"Error processing header: {str(e)}")
            return match.group(0)  # Return original text if processing fails

    def process_paragraphs(self, match):
        content = match.group(1)
        if re.match(r"<\w+[^>]*>", content):
            return content
        return f"<p>{content}</p>"

    def process_bold(self, match):
        content = match.group(2) or match.group(4)
        return f"<strong>{content}</strong>"

    def process_italic(self, match):
        content = match.group(2) or match.group(4)
        return f"<em>{content}</em>"

    def process_bold_italic(self, match):
        content = match.group(2) or match.group(4)
        return f"<strong><em>{content}</em></strong>"

    def process_inline_code(self, match):
        return f"<code>{self.escape_html(match.group(1))}</code>"

    def process_fenced_code_block(self, match):
        language = match.group(1) or ""
        code = match.group(2)
        return f'<pre><code class="language-{language}">{self.escape_html(code)}</code></pre>'

    def process_indented_code_block(self, match):
        code = match.group(1)
        code = re.sub(r"(?:^|\n)(    |\t)", "\n", code)
        return f"<pre><code>{self.escape_html(code.strip())}</code></pre>"

    def process_links(self, match):
        link_text = match.group(1)
        link_url = self.escape_html(match.group(2))
        return f'<a href="{link_url}">{link_text}</a>'

    def process_images(self, match):
        alt_text = self.escape_html(match.group(1))
        image_url = self.escape_html(match.group(2))
        return f'<img src="{image_url}" alt="{alt_text}">'

    def process_horizontal_rules(self, match):
        return "<hr>"

    def pre_process_tables(self, text):
        try:

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
                            "<tr>"
                            + "".join(f"<td>{cell}</td>" for cell in cells)
                            + "</tr>"
                        )
                body_html += "</tbody>"

                return f"<table>\n{header_html}\n{body_html}\n</table>"

            pattern = r"^\|(.+\|)+\n\|(?:[-:| ]+\|)+\n((?:\|(?:.+\|)+\n?)+)"
            return re.sub(pattern, process_table, text, flags=re.MULTILINE)
        except Exception as e:
            self.logger.error(f"Error pre-processing tables: {str(e)}")
            return text  # Return original text if processing fails

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
            if not items:
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

    def escape_html(self, text):
        try:
            return (
                text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;")
            )
        except Exception as e:
            self.logger.error(f"Error escaping HTML: {str(e)}")
            return text  # Return original text if escaping fails

    def process_markdown_file(self, input_path, output_path):
        try:
            with open(input_path, "r", encoding="utf-8") as file:
                markdown_content = file.read()

            html_content = self.process(markdown_content)

            with open(output_path, "w", encoding="utf-8") as file:
                file.write(html_content)

            self.logger.info(
                f"Processed {input_path} and saved result to {output_path}"
            )
        except IOError as e:
            self.logger.error(f"IO error occurred: {str(e)}")
            raise MarkdownProcessingError(f"Failed to process file: {str(e)}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            raise MarkdownProcessingError(
                f"Unexpected error during file processing: {str(e)}"
            )


if __name__ == "__main__":
    mdp = MarkdownProcessor()
    try:
        with open("error_test_cases.md", "r", encoding="utf-8") as file:
            markdown_text = file.read()

        html_output = mdp.process(markdown_text)
        print(html_output)

    except MarkdownProcessingError as e:
        print(f"Error processing Markdown: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
