import os
import subprocess
from ruff.__main__ import find_ruff_bin  # type: ignore

from ..application_state import ApplicationState
from ..cli_foundation.command import Command
from ..role.responds_to_cli import responds_to_cli


@responds_to_cli(
    name="format",
    description="Formats the code",
)
class Format(Command):
    def __init__(
        self,
        application_state: ApplicationState,
    ):
        Command.__init__(self)

        self.application_state = application_state

    async def respond(self) -> int:
        ruff_path = os.fsdecode(find_ruff_bin())

        return subprocess.run(
            [
                ruff_path,
                "format",
                self.application_state.get_root_module_directory_path(),
            ]
        ).returncode
