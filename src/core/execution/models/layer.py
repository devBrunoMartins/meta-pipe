from core.execution.models.asset import Asset


class Layer:
    def __init__(
        self,
        id_layer: int|None,
        id_version: int,
        name: str,
        status: str
    ):
        self.id_layer = id_layer
        self.id_version = id_version
        self.name = name
        self.status = status
        self.assets = []

    @property
    def id_layer(self):
        return self._id_layer

    @id_layer.setter
    def id_layer(self, value):
        self._id_layer = value

    @property
    def id_version(self):
        return self._id_version

    @id_version.setter
    def id_version(self, value):
        self._id_version = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def assets(self):
        return self._assets

    @assets.setter
    def assets(self, value: list[Asset]):
        self._assets = value

    def add_asset(self, asset: Asset):
        if asset not in self.assets:
            self.assets.append(asset)

    def remove_asset(self, asset: Asset):
        if asset in self.assets:
            self.assets.remove(asset)