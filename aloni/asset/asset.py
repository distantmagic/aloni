from pathlib import Path


class Asset:
    def __init__(
        self,
        relative_path: str,
        absolute_path: Path,
        mime_type: str,
    ) -> None:
        self.relative_path = relative_path
        self.absolute_path = absolute_path
        self.mime_type = mime_type
