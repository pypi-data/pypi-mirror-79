from enum import Enum

from koroviev import __project__


class SetupLanguage(Enum):
    python = "python"

    @classmethod
    def get(cls, name: str) -> "SetupLanguage":
        return getattr(cls, name)


class SetupTemplateType(Enum):
    unary = "unary"


class SetupLanguageExtension(Enum):
    python = "py"

    @classmethod
    def get(cls, name: str) -> "SetupLanguageExtension":
        return getattr(cls, name)


class StructureAction(Enum):
    generate = "generate"
    remove = "remove"
    actions = "actions"

    @classmethod
    def get(cls, name: str) -> "StructureAction":
        return getattr(cls, name)


DEFAULT_CONFIG_FILENAME = f".{__project__.lower()}.toml"

DEFAULT_CONFIG_PRESET = (
    "[setup]\n"
    "language = '{language}'\n"
    "project_folder = '{project_folder}'\n"
    "templates_folder = '{templates_folder}'\n"
    "template_extension = '{template_extension}'"
)

DEFAULT_TEMPLATES_DIRNAME = f".{__project__.lower()}_templates"
