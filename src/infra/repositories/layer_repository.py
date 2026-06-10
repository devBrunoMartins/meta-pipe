from infra.db.sqlite_db import SQLiteDB
from core.execution.models.layer import Layer

class LayerRepository:
    def __init__(self, db: SQLiteDB) -> None:
        self.db = db


    def create(self):
        query = """
            CREATE TABLE IF NOT EXISTS tb_layer (
                id_layer INTEGER PRIMARY KEY AUTOINCREMENT,
                id_version INTEGER NOT NULL,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (id_version)
                    REFERENCES tb_version(id_version)
                    ON DELETE CASCADE
            );
        """

        self.db.execute(query)
        self.db.commit()


    def get_by_id(self, id_layer: int):
        query = """
            SELECT *
            FROM tb_layer
            WHERE id_layer = ?
        """

        row = self.db.fetchone(query, (id_layer,))
        if row is None:
            raise ValueError(f"Layer not found: {id_layer}")

        return row


    def get_by_name(self, name):
        query = """
            SELECT *
            FROM tb_layer
            WHERE name = ?
        """

        row = self.db.fetchone(query, (name,))
        if row is None:
            raise ValueError(f"Layer not found: {name}")

        return row


    def get_by_id_version(self, id_version):
        query = """
            SELECT *
            FROM tb_layer
            WHERE id_version = ?
        """

        rows = self.db.fetchall(query, (id_version,))
        if not rows:
            raise ValueError(f"No layers found for version: {id_version}")

        return rows


    def get_by_status(self, status):
        query = """
            SELECT *
            FROM tb_layer
            WHERE status = ?
        """

        rows = self.db.fetchall(query, (status,))
        if not rows:
            raise ValueError(f"No layers found with status: {status}")

        return rows


    def get_all(self):
        query = """
            SELECT *
            FROM tb_layer
        """

        return self.db.fetchall(query)


    def create_layer(self, layer: Layer):
        query = """
            INSERT INTO tb_layer
                (id_version, name, status)
            VALUES
                (?, ?, ?)
        """

        params = (
            layer.id_version,
            layer.name,
            layer.status
        )

        cursor = self.db.execute(query, params)
        self.db.commit()

        return cursor.lastrowid



    def update(self, layer: Layer):
        query = """
            UPDATE tb_layer
            SET name = ?,
                status = ?
            WHERE 
                id_layer = ? and
                id_version = ?
        """

        params = (
            layer.name,
            layer.status,
            layer.id_layer,
            layer.id_version
        )

        self.db.execute(query, params)
        self.db.commit()