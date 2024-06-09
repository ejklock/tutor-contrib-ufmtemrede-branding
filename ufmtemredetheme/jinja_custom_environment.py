import os

import jinja2
from tutor import env, hooks


class JinjaCustomEnvironment(jinja2.Environment):
    loader: jinja2.FileSystemLoader

    def __init__(self):
        template_roots = hooks.Filters.ENV_TEMPLATE_ROOTS.apply([env.TEMPLATES_ROOT])
        loader = jinja2.FileSystemLoader(template_roots)
        super().__init__(loader=loader, undefined=jinja2.StrictUndefined)
        self.globals['date'] = ''