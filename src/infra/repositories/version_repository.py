from infra.db.sqlite_db import SQLiteDB
from core.execution.models.version import Version


class VersionRepository:
    def __init__(self, db: SQLiteDB):
        self.db = db


    def create(self):
        query = """
            CREATE TABLE IF NOT EXISTS tb_version (
                id_version INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                start_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL
            );
        """

        self.db.execute(query)
        self.db.commit()


    def get_by_status(self, status):
        query = """
            SELECT *
            FROM tb_version
            WHERE status = ?
        """

        return self.db.fetchall(query, (status,))


    def find_by_status(self, status):
        query = """
            SELECT *
            FROM tb_version
            WHERE status = ?
        """

        return self.db.fetchall(query, (status,))


    def get_by_id(self, id_version):
        query = """
            SELECT *
            FROM tb_version
            WHERE id_version = ?
        """

        return self.db.fetchone(query, (id_version,))


    def get_all(self):
        query = """
            SELECT *
            FROM tb_version
        """

        return self.db.fetchall(query)

    def update_version(self, version: Version):
        query = """
            UPDATE 
                tb_version
            SET
                name = ?,
                description = ?,
                start_at = ?,
                finished_at = ?,
                status = ?
            WHERE
                id_version = ?
        """
        params = (
            version.name,
            version.description,
            version.start_at,
            version.finished_at,
            version.status,
            version.id_version
        )

        self.db.execute(query, params)
        self.db.commit()


    def create_version(self, version: Version):
        query = """
            INSERT INTO tb_version
                (name, description, start_at, finished_at, status)
            VALUES
                (?, ?, ?, ?, ?)
        """

        params = (
            version.name,
            version.description,
            version.start_at,
            version.finished_at,
            version.status
        )

        cursor = self.db.execute(query, params)
        self.db.commit()

        return cursor.lastrowid