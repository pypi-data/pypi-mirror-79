from functools import wraps
from typing import Callable

from termcolor import cprint


def config_file_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> None:
        if not self._cfg_exist:
            cprint(
                "Error: config file does not exists. It looks like the project is not initialized.",
                "red",
            )
        else:
            func(self, *args, **kwargs)

    return wrapper
