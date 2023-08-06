import os

from termcolor import cprint

from koroviev.const import (
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_CONFIG_PRESET,
    DEFAULT_TEMPLATES_DIRNAME,
    SetupLanguage,
    SetupLanguageExtension,
)


def init_project(language: str, project_folder: str) -> None:
    """Init config file and templates folder.

    :param language: supported language
    :param project_folder: target project source folder in project root folder
    :type language: str
    :type project_folder: str
    :return: None
    """

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
