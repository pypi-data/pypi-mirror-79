import typing

from pydantic import BaseModel, Field

from koroviev.const import SetupLanguage, SetupTemplateType


class TemplateSection(BaseModel):
    comment: str = Field(default="")
    type: SetupTemplateType = Field(default=SetupTemplateType.unary)
    params: typing.List[str] = Field(default=[])
    extension: typing.Optional[str] = Field(default=None)
    target_project_dir: str = Field(...)


class SetupSection(BaseModel):
    language: SetupLanguage = Field(default=SetupLanguage.python)
    project_folder: str = Field(...)
    templates_folder: str = Field(...)
    template_extension: str = Field(...)


class Config(BaseModel):
    setup: SetupSection = Field(...)
    templates: typing.Dict[str, TemplateSection] = Field(default={})
