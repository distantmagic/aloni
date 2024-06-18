from typing import Dict, Optional

from .asset import Asset


class ApplicationAssetRegistry:
    def __init__(self) -> None:
        self.assets: Dict[str, Asset] = {}

    def get_asset(self, relative_path: str) -> Optional[Asset]:
        if relative_path in self.assets:
            return self.assets[relative_path]

        return None

    def register_asset(
        self,
        asset: Asset,
    ) -> None:
        self.assets[asset.relative_path] = asset
