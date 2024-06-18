from typing import Union
from ..asset.application_asset_registry import ApplicationAssetRegistry
from ..http_foundation.file_response import FileResponse
from ..role.intercepts_http_response import intercepts_http_response
from .asset_response import AssetResponse
from .not_found_responder import NotFoundResponder
from .response_interceptor import ResponseInterceptor


@intercepts_http_response(response_class=AssetResponse)
class AssetResponseInterceptor(ResponseInterceptor[AssetResponse]):
    def __init__(
        self,
        application_asset_registry: ApplicationAssetRegistry,
        not_found_responder: NotFoundResponder,
    ):
        ResponseInterceptor.__init__(self)

        self.application_asset_registry = application_asset_registry
        self.not_found_responder = not_found_responder

    async def intercept(
        self, response: AssetResponse
    ) -> Union[FileResponse, NotFoundResponder]:
        asset = self.application_asset_registry.get_asset(response.asset_filename)

        if asset is not None:
            return FileResponse(
                absolute_file_path=asset.absolute_path,
                content_type=asset.mime_type,
            )

        return self.not_found_responder
