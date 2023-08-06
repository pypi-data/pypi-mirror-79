from koroviev import __project__

DEFAULT_CONFIG_FILENAME = f".{__project__.lower()}.toml"

DEFAULT_CONFIG_PRESET = (
    "[setup]\n"
    "language = '{language}'\n"
    "project_folder = '{project_folder}'\n"
    "templates_folder = '{templates_folder}'\n"
    "template_extension = '{template_extension}'"
)

DEFAULT_TEMPLATES_DIRNAME = f".{__project__.lower()}_templates"
