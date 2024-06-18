import mimetypes
from pathlib import Path

from ..asset.asset import Asset
from ..asset.application_asset_registry import ApplicationAssetRegistry
from ..application_state import ApplicationState
from ..role.service_provider import service_provider
from .service_provider import ServiceProvider


@service_provider(provides=ApplicationAssetRegistry)
class ApplicationAssetRegistryProvider(ServiceProvider[ApplicationAssetRegistry]):
    def __init__(
        self,
        application_state: ApplicationState,
    ):
        ServiceProvider.__init__(self)

        self.application_state = application_state

    def guess_mime(self, absolute_path: Path) -> str:
        mime_type = mimetypes.guess_type(absolute_path)[0]

        if mime_type is None:
            return "application/octet-stream"

        return mime_type

    async def provide(self) -> ApplicationAssetRegistry:
        application_asset_registry = ApplicationAssetRegistry()

        base_module_dirname = self.application_state.get_root_module_directory_path()

        base_path = Path(base_module_dirname) / "assets"

        for file_path in base_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(base_path)

                application_asset_registry.register_asset(
                    Asset(
                        absolute_path=file_path,
                        relative_path=str(relative_path),
                        mime_type=self.guess_mime(file_path),
                    )
                )

        return application_asset_registry
