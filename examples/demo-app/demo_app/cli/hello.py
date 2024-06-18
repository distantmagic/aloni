from aloni.cli_foundation import Command
from aloni.role import responds_to_cli


@responds_to_cli(
    name="hello",
    description="Say hello!",
)
class Hello(Command):
    async def respond(self) -> int:
        print("Hello, World!")

        return 0
