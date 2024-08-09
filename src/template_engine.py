from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class TemplateEngine:
    def __init__(self, templates_dir):
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def render(self, template_name, context):
        template = self.env.get_or_select_template(template_name)
        return template.render(context)

    def render_string(self, template_string, context):
        template = self.env.from_string(template_string)
        return template.render(context)
