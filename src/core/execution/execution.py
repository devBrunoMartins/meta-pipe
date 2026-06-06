from infra.repositories.version_repository import VersionRepository
from infra.repositories.layer_repository import LayerRepository
from infra.repositories.asset_repository import AssetRepository

from core.execution.models.version import Version
from core.execution.models.layer import Layer
from core.execution.models.asset import Asset

from typing import Optional

from datetime import datetime
from zoneinfo import ZoneInfo


class Execution:
    SUCCESS = 'success'
    PENDING = 'pending'
    FAILED = 'failed'

    def __init__(
        self,
        version_repository: VersionRepository,
        layer_repository: LayerRepository,
        asset_repository: AssetRepository
    ):
        self.version_repo = version_repository
        self.layer_repo = layer_repository
        self.asset_repo = asset_repository

        self.version: Optional[Version] = None


        self.status_pending = [self.PENDING, self.FAILED]


    def init_db(self) -> None:
        self.version_repo.create()
        self.layer_repo.create()
        self.asset_repo.create()


    def init_version(
            self,
            name,
            description
    ):
        
        if self.version:
            return 

        start_at = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%Y-%m-%d %H:%M:%S")
        
        self.version = Version(
            id_version = None,
            name = name,
            description = description,
            start_at = start_at,
            finished_at = None,
            status = self.PENDING
        )

        id_version = self.version_repo.create_version(self.version)
        self.version.id_version = id_version


    def init_layer(self, name: str) -> int:
        layer = Layer(
            id_layer = None,
            id_version = self.version.id_version,
            name = name,
            status = self.PENDING
        )

        self.version.layers.append(layer)

        id_layer = self.layer_repo.create_layer(layer)

        layer.id_layer = id_layer

        return id_layer



    def init_assets(self, id_layer: int, name: str) -> None:
        asset = Asset(
            id_asset = None,
            id_layer = id_layer,
            name = name,
            path = None,
            status = self.PENDING
        )
        for layer in self.version.layers:
            if layer.id_layer == id_layer:
                layer.assets.append(asset)

        id_asset = self.asset_repo.create_asset(asset)

        asset.id_asset = id_asset


    def get_layers(self):
        return self.version.layers

    def get_layer_by_name(self, layer_name):
        for layer in self.get_layers():
            if layer.name == layer_name:
                return layer

    def pending_assets(self, layer: Layer|None = None):
        if layer:
            return [asset for asset in layer.assets
                    if asset.status in self.status_pending]
        else:
            return layer.assets


    def success_assets(self, layer: Layer|None = None):
        if layer:
            return [asset for asset in layer.assets
                    if asset.status not in self.status_pending]
        else:
            return layer.assets


    def asset_finish(self, asset):
        asset.status = self.SUCCESS
        self.asset_repo.update(asset)
        

    def layer_finish(self, layer: Layer):
        layer.status = self.SUCCESS
        self.layer_repo.update(layer)


    def find_pending_versions(self) -> list:
        interruptions = ['failed', 'pending']
        tb_version = self.version_repo.get_all()
        versions = []

        for row in tb_version:
            if row[3] in interruptions:
                version = Layer(
                id_version = row[0],
                name = row[1],
                start_at = row[3],
                status = row[5]
                )

                versions.append(version)
        
        return versions


    def finish(self,
            finished_at,
            status
    ):
        
        if not self.version:
            return 
        
        self.version.finished_at = finished_at
        self.version.status = status
        
        self.version_repo.update_version(self.version)
