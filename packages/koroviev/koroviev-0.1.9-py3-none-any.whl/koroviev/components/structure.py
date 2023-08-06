import os
import shutil

from termcolor import cprint


def remove_template_structure(templates_folder: str):
    templates_folder = os.path.join(os.getcwd(), templates_folder)
    shutil.rmtree(templates_folder, ignore_errors=True)


def create_template_structure(
    templates: dict, templates_folder: str, default_template_extension: str
):
    for template, info in templates.items():
        type_folder = os.path.join(os.getcwd(), templates_folder, info.type.name)

        if not os.path.isdir(type_folder):
            cprint(
                f"Create template type folder '{info.type.name}': '{type_folder}'...",
                "green",
            )
            os.makedirs(type_folder, exist_ok=True)

        template_filepath = os.path.join(
            os.getcwd(),
            templates_folder,
            info.type.name,
            f"{template}.{default_template_extension if not info.extension else info.extension}",
        )

        if os.path.isfile(template_filepath):
            continue

        with open(template_filepath, "w") as f:
            cprint(
                f"Create template file '{template}': '{template_filepath}'...", "green",
            )
            f.write("\n")
