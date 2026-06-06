class Asset:
    def __init__(
        self,
        id_asset: int|None,
        id_layer: int,
        name: str,
        path: str|None,
        status: str
    ):
        self.id_asset = id_asset
        self.id_layer = id_layer
        self.name = name
        self.path = path
        self.status = status

    @property
    def id_asset(self):
        return self._id_asset

    @id_asset.setter
    def id_asset(self, value):
        self._id_asset = value

    @property
    def id_layer(self):
        return self._id_layer

    @id_layer.setter
    def id_layer(self, value):
        self._id_layer = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str|None):
        self._path = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value