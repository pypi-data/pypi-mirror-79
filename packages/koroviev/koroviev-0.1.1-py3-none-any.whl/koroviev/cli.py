import os
from typing import Optional

import toml
from fire import Fire
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from termcolor import cprint

from koroviev.const import DEFAULT_CONFIG_FILENAME, StructureAction
from koroviev.models import Config
from koroviev.utils import (
    create_template_structure,
    get_templates,
    init_project,
    remove_template_structure,
)


def main():
    CLI.start_cli()


class CLI:
    def __init__(self, config: str = None) -> None:
        self._cfg_name = DEFAULT_CONFIG_FILENAME if not config else config
        self._cfg_path = os.path.join(os.getcwd(), self._cfg_name)
        self._cfg_exist = os.path.isfile(self._cfg_path)
        self._cfg: Optional[Config] = Config(
            **toml.load(self._cfg_path)
        ) if self._cfg_exist else None

    @classmethod
    def start_cli(cls):
        Fire(CLI)

    @logger.catch
    def setups(self):
        cprint(
            f"Config file name: {self._cfg_name}\n"
            f"Config file path: {self._cfg_path}\n"
            f"Config file exist: {self._cfg_exist}\n"
            f"Configs:\n{self._cfg.json(indent=4)}",
            "blue",
        )

    @logger.catch
    def templates(self):
        if not self._cfg_exist:
            cprint("Error: config file does not exists", "red")

        get_templates(self._cfg.templates)

    @logger.catch
    def gen(self, template_name: str):
        if template_name not in self._cfg.templates:
            cprint("Error: template not found", "red")
            return

        template = self._cfg.templates.get(template_name)

        target_filepath = os.path.join(
            os.getcwd(),
            self._cfg.setup.project_folder,
            template.target_project_dir,
            f"{template_name}.{template.extension if template.extension else self._cfg.setup.template_extension}",
        )

        template_path = os.path.join(
            os.getcwd(), self._cfg.setup.templates_folder, template.type.name,
        )

        env = Environment(
            loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True
        )

        rendered_data = env.get_template(
            f"{template_name}.{template.extension if template.extension else self._cfg.setup.template_extension}",
        ).render(
            **{param: input(f"Input '{param}' value: ") for param in template.params}
        )

        with open(target_filepath, "w") as f:
            f.write(rendered_data)
            cprint(f"Create file by template: {target_filepath}...", "green")

    @logger.catch
    def init(self):
        language = input("Input language for templates: ")
        project_folder = input("Input project folder: ")

        init_project(language, project_folder)

    @logger.catch
    def structure(self, action: str = StructureAction.generate.value):
        if action in StructureAction.__members__:
            if StructureAction(action) == StructureAction.generate:
                create_template_structure(
                    self._cfg.templates,
                    self._cfg.setup.templates_folder,
                    self._cfg.setup.template_extension,
                )

            elif StructureAction(action) == StructureAction.remove:
                remove_template_structure(self._cfg.setup.templates_folder)

        else:
            cprint(
                f"Error: invalid action name\nActions list: {', '.join(StructureAction.__members__)}",
                "red",
            )
