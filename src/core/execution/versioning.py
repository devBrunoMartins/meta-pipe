from infra.db.repository import RepositoryPipeline
from datetime import datetime
from zoneinfo import ZoneInfo


class Versioning:

    def __init__(self, repository: RepositoryPipeline):
        
        self.repository = repository


    def run(self) -> None:
        
        self.__create_db_if_not_exists()

        start_at = datetime.now(ZoneInfo("America/Sao_Paulo"))

        if self.repository.find_current_version() is None:

            project_name, description = self.define_version()
            status = 'current'

            self.repository.create_version(
                project_name,
                description,
                start_at,
                status
            )


    def define_version(self) -> tuple:

        while True:
            project_name = input('\033[33m*obrigatório\033[0m\nProject name: ')
            if project_name[:1].isalpha():
                break

        description = input('Project description: ')

        return project_name, description

    def __create_db_if_not_exists(self) -> None:

        self.repository.create_version_table()
        self.repository.create_layer_table()
        self.repository.create_asset_table()
        self.repository.create_layers_categories()
    
    
    def registry_asset(self,
                      layer_name: int,
                      name: str,
                      path: str,
                      ) -> None:

        id_layer = self.repository.get_layer_by_name(layer_name)[0]
        id_version = self.repository.get_current_version()[0]

        self.repository.create_assets(
            id_layer,
            id_version,
            name,
            path
        )