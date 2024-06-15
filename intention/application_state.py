from types import ModuleType
from .application_mode import ApplicationMode


class ApplicationState:
    def __init__(
        self,
        mode: ApplicationMode,
        root_module: ModuleType,
    ):
        self.mode = mode
        self.root_module = root_module
