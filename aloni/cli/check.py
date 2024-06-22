import os
import subprocess
import sys
from mypy import api
from ruff.__main__ import find_ruff_bin  # type: ignore

from ..application_state import ApplicationState
from ..cli_foundation.command import Command
from ..role.responds_to_cli import responds_to_cli


@responds_to_cli(
    name="check",
    description="Check the project for type errors and linting issues (runs preconfigured ruff and mypy)",
)
class Check(Command):
    def __init__(
        self,
        application_state: ApplicationState,
    ):
        Command.__init__(self)

        self.application_state = application_state

    async def respond(self) -> int:
        exit_code = await self.run_mypy()

        if exit_code != 0:
            return exit_code

        return await self.run_ruff()

    async def run_mypy(self) -> int:
        result = api.run(
            [
                "--disallow-any-generics",
                "--disallow-any-unimported",
                "--disallow-subclassing-any",
                "--disallow-untyped-calls",
                "--disallow-untyped-decorators",
                "--disallow-untyped-defs",
                "--extra-checks",
                "--follow-imports=normal",
                "--pretty",
                "--strict",
                "--strict-equality",
                "--warn-redundant-casts",
                "--warn-return-any",
                "--warn-unreachable",
                "--warn-unused-ignores",
                self.application_state.get_root_module_directory_path(),
            ]
        )

        stdout, stderr, returncode = result

        sys.stdout.write(stdout)
        sys.stderr.write(stderr)

        return returncode

    async def run_ruff(self) -> int:
        ruff_path = os.fsdecode(find_ruff_bin())

        return subprocess.run(
            [
                ruff_path,
                "check",
                self.application_state.get_root_module_directory_path(),
            ]
        ).returncode
