from infra.db.sqlite_db import SQLiteDB
from core.execution.models.asset import Asset


class AssetRepository:
    def __init__(self, db: SQLiteDB):
        self.db = db


    def create(self):
        query = """
            CREATE TABLE IF NOT EXISTS tb_asset (
                id_asset INTEGER PRIMARY KEY AUTOINCREMENT,
                id_layer INTEGER NOT NULL,
                name TEXT NOT NULL,
                path TEXT,
                status TEXT NOT NULL,
                FOREIGN KEY (id_layer)
                    REFERENCES tb_layer(id_layer)
                    ON DELETE CASCADE
            );
        """

        self.db.execute(query)
        self.db.commit()


    def get_by_id(self, id_asset):
        query = """
            SELECT *
            FROM tb_asset
            WHERE id_asset = ?
        """

        row = self.db.fetchone(query, (id_asset,))
        if row is None:
            raise ValueError(f"Asset not found: {id_asset}")

        return row


    def get_by_id_layer(self, id_layer):
        query = """
            SELECT *
            FROM tb_asset
            WHERE id_layer = ?
        """

        rows = self.db.fetchall(query, (id_layer,))
        if not rows:
            raise ValueError(f"No assets found for layer: {id_layer}")

        return rows


    def get_by_name(self, name):
        query = """
            SELECT *
            FROM tb_asset
            WHERE name = ?
        """

        row = self.db.fetchone(query, (name,))
        if row is None:
            raise ValueError(f"Asset not found: {name}")

        return row


    def get_by_status(self, status):
        query = """
            SELECT *
            FROM tb_asset
            WHERE status = ?
        """

        rows = self.db.fetchall(query, (status,))
        if not rows:
            raise ValueError(f"No assets found with status: {status}")

        return rows


    def find_by_status(self, status):
        query = """
            SELECT *
            FROM tb_asset
            WHERE status = ?
        """

        rows = self.db.fetchall(query, (status,))
        return rows if rows else None


    def get_all(self):
        query = """
            SELECT *
            FROM tb_asset
        """

        rows = self.db.fetchall(query)
        if not rows:
            raise ValueError("No assets found")

        return rows


    def create_asset(self, asset: Asset):
        query = """
            INSERT INTO tb_asset
                (id_layer, name, path, status)
            VALUES
                (?, ?, ?, ?)
        """

        params = (
            asset.id_layer,
            asset.name,
            asset.path,
            asset.status
        )

        cursor = self.db.execute(query, params)
        self.db.commit()

        return cursor.lastrowid


    def update(self, asset: Asset):
        query = """
            UPDATE tb_asset
            SET id_layer = ?,
                name = ?,
                path = ?,
                status = ?
            WHERE id_asset = ?
        """

        params = (
            asset.id_layer,
            asset.name,
            asset.path,
            asset.status,
            asset.id_asset
        )

        self.db.execute(query, params)
        self.db.commit()