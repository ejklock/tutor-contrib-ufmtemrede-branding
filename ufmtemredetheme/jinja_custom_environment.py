import os

import jinja2
from tutor import env, hooks


class JinjaCustomEnvironment(jinja2.Environment):
    loader: jinja2.FileSystemLoader

    def __init__(self) -> None:
        template_roots = hooks.Filters.ENV_TEMPLATE_ROOTS.apply([env.TEMPLATES_ROOT])
        loader = jinja2.FileSystemLoader(template_roots)
        super().__init__(loader=loader, undefined=jinja2.StrictUndefined, comment_start_string='{=',comment_end_string='=}',)
        self.globals['date'] = ''

    def read_str(self, template_name: str) -> str:
        return self.read_bytes(template_name).decode()

    def read_bytes(self, template_name: str) -> bytes:
        with open(self.find_os_path(template_name), "rb") as f:
            return f.read()

    def find_os_path(self, template_name: str) -> str:
        path = template_name.replace("/", os.sep)
        for templates_root in self.loader.searchpath:
            full_path = os.path.join(templates_root, path)
            if os.path.exists(full_path):
                return full_path
        raise ValueError("Template path does not exist")