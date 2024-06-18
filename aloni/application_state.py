import inspect
import os
from types import ModuleType
from typing import Optional

from .application_mode import ApplicationMode


class ApplicationState:
    def __init__(
        self,
        mode: ApplicationMode,
        root_module: ModuleType,
    ):
        self.cached_root_module_directory_path: Optional[str] = None
        self.mode = mode
        self.root_module = root_module

    def get_root_module_directory_path(self) -> str:
        if self.cached_root_module_directory_path is not None:
            return self.cached_root_module_directory_path

        base_module_path = inspect.getfile(self.root_module)
        base_module_dirname = os.path.dirname(base_module_path)

        self.cached_root_module_directory_path = base_module_dirname

        return base_module_dirname
