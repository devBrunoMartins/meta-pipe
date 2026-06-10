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


    def get_versions(self):
        versions_list = []
        for row in self.version_repo.get_all():
            versions_list.append(
                Version(
                    id_version = row[0],
                    name = row[1],
                    description = row[2],
                    start_at = row[3],
                    finished_at = row[4],
                    status = row[5]
                )
            )
        return versions_list


    def get_layers(self):
        return self.version.layers

    def get_layer_by_name(self, layer_name):
        for layer in self.get_layers():
            if layer.name == layer_name:
                return layer

    def pending_assets(self, layer: Layer|None = None):
        return [asset for asset in layer.assets
                if asset.status in self.status_pending]
    

    def success_assets(self, layer: Layer|None = None):
        return [asset for asset in layer.assets
                if asset.status not in self.status_pending]


    def asset_finish(self, asset):
        asset.status = self.SUCCESS
        self.asset_repo.update(asset)
        

    def layer_finish(self, layer: Layer):
        layer.status = self.SUCCESS
        self.layer_repo.update(layer)


    def find_pending_versions(self) -> list:
        pendings = ['failed', 'pending']
        tb_version = self.version_repo.get_all()
        versions = []

        for row in tb_version:
            if row[5] in pendings:
                version = Version(
                id_version = row[0],
                name = row[1],
                description = row[2],
                start_at = row[3],
                finished_at = row[4],
                status = row[5]
                )

                versions.append(version)
        
        return versions

    def get_layers_by_version(self, version: Version):
        layer_list = []

        for row in self.layer_repo.get_by_id_version(version.id_version):
            print
            id_layer = row[0]
            id_version = row[1]
            name = row[2]
            status = row[3]

            layer_list.append(
                Layer(
                    id_layer = id_layer,
                    id_version = id_version,
                    name = name,
                    status = status
                ))

        return layer_list


    def get_assets_by_layer(self, layer: Layer):
        asset_list = []

        for row in self.asset_repo.get_by_id_layer(layer.id_layer):
            id_asset = row[0]
            id_layer = row[1]
            name = row[2]
            path = row[3]
            status = row[4]

            asset_list.append(
                Asset(
                    id_asset = id_asset,
                    id_layer = id_layer,
                    name = name,
                    path = path,
                    status = status
                ))
        return asset_list


    def get_assets_by_version(self, version: Version) -> list[Asset]:
        layers = self.get_layers_by_version(version)
        assets_lists = []
        for layer in layers:
            assets_lists.append(self.get_assets_by_layer(layer))

        assets_list = []
        for list_ in assets_lists:
            assets_list += list_

        return assets_list
            

    def load_version_pending(self, version: Version):
        self.version = version
        for layer in self.get_layers_by_version(version):
            for asset in self.get_assets_by_layer(layer):
                layer.assets.append(asset)

            self.version.layers.append(layer) 


    def delete_version(self, id_version):
        self.version_repo.delete_version(id_version)

    def finish(self):
        
        if not self.version:
            return 
        
        self.version.finished_at = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.version.status = self.SUCCESS
        
        self.version_repo.update_version(self.version)

        self.version = None


