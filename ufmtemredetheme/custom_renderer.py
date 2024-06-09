import os
import typing as t

import jinja2
from tutor import env, exceptions, fmt


class CustomRenderer(env.Renderer):
    
    IGNORE_TEMPLATE_RENDER_EXTENSIONS=['.json','.po']
    
    def __render(self, template: jinja2.Template) -> str:
        try:
            return template.render(**self.config)
        except jinja2.exceptions.UndefinedError as e:
            raise exceptions.TutorError(f"Missing configuration value: {e.args[0]}")
    def render_template(self, template_name: str) -> t.Union[str, bytes]:
        """
        Render a template file. Return the corresponding string. If it's a binary file
        (as indicated by its path), return bytes.

        The template_name *always* uses "/" separators, and is not os-dependent. Do not pass the result of
        os.path.join(...) to this function.
        """
        file_extension = os.path.splitext(template_name)[1]
        
        
        if env.is_binary_file(template_name) or file_extension in self.IGNORE_TEMPLATE_RENDER_EXTENSIONS:
            return self.environment.read_bytes(template_name)

        try:
            template = self.environment.get_template(template_name)
        except Exception:
            fmt.echo_error("Error loading template " + template_name)
            raise

        try:
            return self.__render(template)
        except (jinja2.exceptions.TemplateError, exceptions.TutorError):
            fmt.echo_error("Error rendering template " + template_name)
            raise
        except Exception:
            fmt.echo_error("Unknown error rendering template " + template_name)
            raise