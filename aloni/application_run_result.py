import sys
from typing import Never


class ApplicationRunResult:
    def __init__(
        self,
        exit_code: int,
    ) -> None:
        self.exit_code = exit_code

    def exit_after_finishing(self) -> Never:
        sys.exit(self.exit_code)
