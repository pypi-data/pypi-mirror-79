import os
import shutil

from termcolor import cprint

from koroviev.const import (
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_CONFIG_PRESET,
    DEFAULT_TEMPLATES_DIRNAME,
    SetupLanguage,
    SetupLanguageExtension,
)


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


def init_project(language: str, project_folder: str):
    if language not in SetupLanguage.__members__:
        cprint(f"Error: {language} not supported language.", "red")
        cprint(
            f"Supported languages: {', '.join(list(map(lambda x: x.name, SetupLanguage)))}"
        )
        return

    if os.path.isfile(os.path.join(os.getcwd(), DEFAULT_CONFIG_FILENAME)):
        cprint("Config file already exists", "red")
        return

    try:
        with open(os.path.join(os.getcwd(), DEFAULT_CONFIG_FILENAME), "w") as f:
            f.write(
                DEFAULT_CONFIG_PRESET.format(
                    project_folder=project_folder,
                    language=language,
                    templates_folder=DEFAULT_TEMPLATES_DIRNAME,
                    template_extension=SetupLanguageExtension.get(language).value,
                )
            )

        if os.path.isdir(os.path.join(os.getcwd(), DEFAULT_TEMPLATES_DIRNAME)):
            cprint("Templates folder already exists", "red")
            return

        os.makedirs(os.path.join(os.getcwd(), DEFAULT_TEMPLATES_DIRNAME), exist_ok=True)
    except Exception:
        raise

    cprint("Config file and template folder created", "green")
    cprint(
        f"{os.path.join(os.getcwd(), DEFAULT_CONFIG_FILENAME)}\n"
        f"{os.path.join(os.getcwd(), DEFAULT_TEMPLATES_DIRNAME)}",
        "green",
    )


def get_templates(templates: dict):
    for template, info in templates.items():
        info = info.dict()
        cprint(f"{template}", "blue")

        for field in info:
            cprint(f" {field}: {info[field]}", "green")
