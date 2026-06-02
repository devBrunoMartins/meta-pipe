from infra.db.sqlite_db import SQLiteDB


class RepositoryPipeline:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def create_version_table(self):

        query = """
            CREATE TABLE IF NOT EXISTS tb_version (
                id_version INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                description TEXT,
                start_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL
            );
            """
        
        self.db.execute(query)
        self.db.commit()


    def create_layer_table(self):

        query = """
            CREATE TABLE IF NOT EXISTS tb_layer (
                id_layer INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        
        self.db.execute(query)
        self.db.commit()


    def create_asset_table(self):

        query = """
            CREATE TABLE IF NOT EXISTS tb_asset (
                id_asset INTEGER PRIMARY KEY AUTOINCREMENT,
                id_layer INTEGER NOT NULL,
                id_version INTEGER NOT NULL,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                FOREIGN KEY (id_layer) REFERENCES tb_layer(id_layer),
                FOREIGN KEY (id_version) REFERENCES tb_version(id_version)
            );
            """
    
        self.db.execute(query)
        self.db.commit()


    def create_layers_categories(self):

        query = """
            INSERT OR IGNORE INTO tb_layer (name) 
            values
            (?)
        """

        values = [
            ('bronze',),
            ('silver',),
            ('gold',)
        ]

        self.db.execute_many(query, values)
        self.db.commit()
        

    def get_current_version(self):

        query = """
            SELECT * FROM tb_version WHERE status = 'current'
        """

        row = self.db.fetchone(query)
        if row is None:
            raise

        return row


    def find_current_version(self):

        query = """
            SELECT * FROM tb_version WHERE status = 'current'
        """

        return self.db.fetchone(query)


    def get_versions(self):
        query = """
            SELECT * FROM tb_version
        """

        return self.db.fetchall(query)
        
    
    def get_version(self, id):
        query = """
            SELECT * FROM tb_version WHERE id_version = ?
        """
       
        return self.db.fetchone(query, id)


    def create_version(self,
                       project_name: str,
                       description: str | None,
                       start_at: str,
                       status: str
                       ):
        
        query = """
            INSERT INTO tb_version
                (project_name, description, start_at, status)
            values
                (?, ?, ?, ?)
        """

        if project_name and start_at and status:
            params = (
                project_name,
                description,
                start_at,
                status
            )
            self.db.execute(query, params)
            self.db.commit()
        else:
            raise


    def create_assets(self,
                      id_layer: int, 
                      id_version: int,
                      name: str,
                      path: str,
                      ) -> None:
        
        query = """
        INSERT INTO tb_asset
        (id_layer, id_version, name, path)
        values
        (?, ?, ?, ?)
        """

        params = (
            id_layer,
            id_version,
            name,
            path
        )

        self.db.execute(query, params)
        self.db.commit()


    def get_layer_by_name(self, layer_name: str) -> tuple | None:
        query = """
            SELECT 
                id_layer, name from tb_layer
            WHERE
                name = ?
        """
        params = (layer_name,)

        return self.db.fetchone(query, params)