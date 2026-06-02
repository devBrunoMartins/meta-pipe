class SQLiteDB:

    def __init__(self, conn):
        self.__conn = conn

    def execute(self, query, params=()):
        return self.__conn.execute(query, params)

    def execute_many(self, query, rows):
        return self.__conn.executemany(query, rows)

    def fetchone(self, query, params=()):
        cursor = self.__conn.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query, params=()):
        cursor = self.__conn.execute(query, params)
        return cursor.fetchall()

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def close(self):
        self.__conn.close()