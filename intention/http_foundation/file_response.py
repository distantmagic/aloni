from pathlib import Path
from .final_response import FinalResponse


class FileResponse(FinalResponse):
    def __init__(
        self,
        absolute_file_path: Path,
        content_type: str,
    ):
        self.absolute_file_path = absolute_file_path
        self.content_type = content_type

    def get_content_type(self) -> str:
        return self.content_type

    def get_absolute_file_path(self) -> Path:
        return self.absolute_file_path
