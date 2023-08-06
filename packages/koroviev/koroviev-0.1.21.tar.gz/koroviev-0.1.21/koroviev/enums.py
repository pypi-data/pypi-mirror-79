from enum import Enum


class SetupLanguage(Enum):
    python = "python"

    @classmethod
    def get(cls, name: str) -> "SetupLanguage":
        return getattr(cls, name)


class SetupTemplateType(Enum):
    unary = "unary"
    complex = "complex"


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
