import os

from jinja2 import Environment, FileSystemLoader
from termcolor import cprint

from koroviev.const import (
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_CONFIG_PRESET,
    DEFAULT_TEMPLATES_DIRNAME,
    SetupLanguage,
    SetupLanguageExtension,
)


def get_templates(templates: dict):
    for template, info in templates.items():
        info = info.dict()
        cprint(f"{template}", "blue")

        for field in info:
            cprint(f" {field}: {info[field]}", "green")


def generate_by_template(
    template_name: str,
    templates: dict,
    project_folder: str,
    default_template_extension: str,
    templates_folder: str,
):
    if template_name not in templates:
        cprint("Error: template not found", "red")
        return

    template = templates.get(template_name)

    target_filepath = os.path.join(
        os.getcwd(),
        project_folder,
        template.target_project_dir,
        f"{template_name}.{template.extension if template.extension else default_template_extension}",
    )

    template_path = os.path.join(os.getcwd(), templates_folder, template.type.name,)

    env = Environment(
        loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True
    )

    rendered_data = env.get_template(
        f"{template_name}.{template.extension if template.extension else default_template_extension}",
    ).render(**{param: input(f"Input '{param}' value: ") for param in template.params})

    with open(target_filepath, "w") as f:
        f.write(rendered_data)
        cprint(f"Create file by template: {target_filepath}...", "green")
