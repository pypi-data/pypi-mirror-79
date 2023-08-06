import os
from typing import Optional

import toml
from fire import Fire
from loguru import logger
from termcolor import cprint

from koroviev.components import (
    create_template_structure,
    generate_by_template,
    get_templates,
    init_project,
    remove_template_structure,
)
from koroviev.const import DEFAULT_CONFIG_FILENAME, StructureAction
from koroviev.models import Config
from koroviev.utils import config_file_required


@logger.catch
def start_cli():
    Fire(CLI)


class CLI:
    def __init__(self) -> None:
        self._cfg_name = DEFAULT_CONFIG_FILENAME
        self._cfg_path = os.path.join(os.getcwd(), self._cfg_name)
        self._cfg_exist = os.path.isfile(self._cfg_path)
        self._cfg: Optional[Config] = Config(
            **toml.load(self._cfg_path)
        ) if self._cfg_exist else None

    @config_file_required
    def setups(self):
        """View project setups.

        :return: None
        """
        cprint(
            f"Config file name: {self._cfg_name}\n"
            f"Config file path: {self._cfg_path}\n"
            f"Config file exist: {self._cfg_exist}\n"
            f"Configs:\n{self._cfg.json(indent=4)}",
            "blue",
        )

    @config_file_required
    def templates(self):
        """View all defined templates.

        :return: None
        """
        get_templates(self._cfg.templates)

    @config_file_required
    def gen(self, template_name: str):
        """Generate code by defined template.

        :param template_name: defined template name
        :return: None
        """

        generated_filename = input("Input name for generated file: ")

        generate_by_template(
            template_name,
            self._cfg.templates,
            self._cfg.setup.project_folder,
            self._cfg.setup.template_extension,
            self._cfg.setup.templates_folder,
            generated_filename
        )

    def init(self):
        """Initialize project.

        :return: None
        """

        language = input("Input language for templates: ")
        project_folder = input("Input project folder: ")

        init_project(language, project_folder)

    @config_file_required
    def structure(self, action: StructureAction = StructureAction.actions):
        """Structure templates action.

        :param action: supported structure's action
        :type action: StructureAction
        :return: None
        """

        if isinstance(action, StructureAction):
            action = action.value

        if action in StructureAction.__members__:
            if StructureAction(action) == StructureAction.generate:
                create_template_structure(
                    self._cfg.templates,
                    self._cfg.setup.templates_folder,
                    self._cfg.setup.template_extension,
                )

            elif StructureAction(action) == StructureAction.remove:
                remove_template_structure(self._cfg.setup.templates_folder)

            elif StructureAction(action) == StructureAction.actions:
                cprint(f"Supported actions: {', '.join(StructureAction.__members__)}")

        else:
            cprint(
                f"Error: invalid action name\nActions list: {', '.join(StructureAction.__members__)}",
                "red",
            )
