class SQLiteDB:

    def __init__(self, conn):
        self.__conn = conn

    def __cursor(self):
        return self.__conn.cursor()

    def execute(self, query, params=()):
        self.__cursor.execute(query, params)

    def fetchone(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor
    
    def commit(self):
        self.__conn.commit()
    
    def rollback(self):
        self.__conn.rollback()

    def close(self):
        self.__conn.close()