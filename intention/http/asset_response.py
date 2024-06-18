from ..http_foundation import Response


class AssetResponse(Response):
    def __init__(
        self,
        asset_filename: str,
    ):
        Response.__init__(self)

        self.asset_filename = asset_filename
