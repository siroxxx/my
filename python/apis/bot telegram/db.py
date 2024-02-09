from pandas import DataFrame, read_sql_query
from pymysql import connect

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.conn = connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def insert_query(self, query, data):
        df = DataFrame(data)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def read_query(self, query):
        result = read_sql_query(query, self.conn)
        return result