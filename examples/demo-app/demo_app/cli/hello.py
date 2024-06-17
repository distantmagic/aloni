from intention.cli_foundation import Command
from intention.role import responds_to_cli


@responds_to_cli(
    name="hello",
    description="Say hello!",
)
class Hello(Command):
    def respond(self) -> int:
        print("Hello, World!")

        return 0
