from core.execution.models.layer import Layer


class Version:
    def __init__(
        self,
        id_version: int | None,
        name: str,
        description: str | None,
        start_at: str,
        finished_at: str | None,
        status: str
    ):
        self.id_version = id_version
        self.name = name
        self.description = description
        self.start_at = start_at
        self.finished_at = finished_at
        self.status = status
        self.layers = []

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
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def start_at(self):
        return self._start_at

    @start_at.setter
    def start_at(self, value):
        self._start_at = value

    @property
    def finished_at(self):
        return self._finished_at

    @finished_at.setter
    def finished_at(self, value):
        self._finished_at = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, value: list[Layer]):
        self._layers = value

    def add_layer(self, layer: Layer):
        if layer not in self.layers:
            self.layers.append(layer)

    def remove_layer(self, layer: Layer):
        if layer in self.layers:
            self.layers.remove(layer)