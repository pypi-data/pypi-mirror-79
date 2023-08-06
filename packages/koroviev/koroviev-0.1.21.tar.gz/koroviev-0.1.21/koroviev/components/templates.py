import os

from jinja2 import Environment, FileSystemLoader
from termcolor import cprint

from koroviev.enums import SetupTemplateType
from koroviev.models import TemplateSection


class Templates:
    @staticmethod
    def view_all(templates: dict):
        """Print all templates with metainfo.

        :param templates: templates from config file
        :return: None
        """

        for template, info in templates.items():
            info = info.dict()
            cprint(f"{template}", "blue")

            for field in info:
                cprint(f" {field}: {info[field]}", "green")

    @staticmethod
    def get_template_extension(template: TemplateSection, default_template_extension: str):
        return template.extension if template.extension else default_template_extension

    @staticmethod
    def get_template_filename(template: TemplateSection, template_name: str, default_template_extension: str):
        return f"{template_name}.{Templates.get_template_extension(template, default_template_extension)}"

    @staticmethod
    def get_template_filepath(
        template: TemplateSection, template_name: str, default_template_extension: str, templates_folder: str
    ):
        return os.path.join(
            os.getcwd(),
            templates_folder,
            template.type.name,
            Templates.get_template_filename(template, template_name, default_template_extension),
        )

    @staticmethod
    def get_target_filepath(
        template: TemplateSection, project_folder: str, generated_filename: str, default_template_extension: str
    ):
        return os.path.join(
            os.getcwd(),
            project_folder,
            template.target_project_dir,
            Templates.get_template_filename(template, generated_filename, default_template_extension),
        )

    @staticmethod
    def _generate_unary(
        template: TemplateSection,
        template_name: str,
        project_folder: str,
        default_template_extension: str,
        templates_folder: str,
        generated_filename: str,
    ):
        target_filepath = Templates.get_target_filepath(
            template, project_folder, generated_filename, default_template_extension
        )

        template_filepath = Templates.get_template_filepath(
            template, template_name, default_template_extension, templates_folder
        )

        if not os.path.isfile(template_filepath):
            cprint(f"Error: expected '{template_filepath}', because template has type 'unary'")

        env = Environment(
            loader=FileSystemLoader(os.path.dirname(template_filepath)), trim_blocks=True, lstrip_blocks=True
        )

        rendered_data = env.get_template(
            Templates.get_template_filename(template, template_name, default_template_extension),
        ).render(**{param: input(f"Input '{param}' value: ") for param in template.params})

        with open(target_filepath, "w") as f:
            f.write(rendered_data)
            cprint(f"Create file by template: {target_filepath}...", "green")

    @staticmethod
    def generate(
        template_name: str,
        templates: dict,
        project_folder: str,
        default_template_extension: str,
        templates_folder: str,
        generated_filename: str,
    ):
        """Generate project file by template.

        :param template_name: available template name
        :param templates: project's templates
        :param project_folder: templates folder
        :param default_template_extension: default template extension
        :param templates_folder: templates folder
        :param generated_filename: filename for generated file
        :return: None
        """

        if template_name not in templates:
            cprint("Error: template not found", "red")
            return

        template = templates.get(template_name)

        if template.type == SetupTemplateType.unary:
            Templates._generate_unary(
                template,
                template_name,
                project_folder,
                default_template_extension,
                templates_folder,
                generated_filename,
            )

        elif template.type == SetupTemplateType.complex:
            pass
