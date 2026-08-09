#DATABASE CONNECTION FOR LOADING PULLER OUTPUT INTO SQL SERVER
#NOTE: OPEN SOURCE PROJECT @https://github.com/sguri003/Labor_Stats_Dev
import pandas as pd
import sqlalchemy as sq

class Database:
    def __init__(self, server = 'DESKTOP-03RVSDU\\SQLEXPRESS', db_nm = 'Labor_Stats'):
        self.server = server
        self.db_nm = db_nm
        self.conn = self.sql_cnx()

    def sql_cnx(self) -> sq.engine.Connection:
        conn_str = f"mssql+pyodbc://{self.server}/{self.db_nm}?driver=ODBC+Driver+17+for+SQL+Server"
        engine = sq.create_engine(conn_str)
        return engine.connect()

    def close_cnx(self):
        print('Closing Connection to DB')
        self.conn.close()

    #write a dataframe to a dbo table. if_exists: 'replace', 'append', or 'fail'
    def write_df(self, df, table_nm, if_exists = 'replace'):
        df.to_sql(table_nm, con = self.conn, schema = 'dbo', if_exists = if_exists, index = False)
        #SQLAlchemy 2.0 connections don't autocommit - without this, the insert
        #is silently rolled back when the connection closes
        self.conn.commit()
        print(f"Wrote {len(df)} rows to dbo.{table_nm}")

    def read_df(self, table_nm):
        df = pd.read_sql_query(f'select * from dbo.{table_nm}', con = self.conn)
        return pd.DataFrame(data = df)


if __name__ == "__main__":
    db = Database()
    print(db.read_df('CPI_Data').head(5))
    db.close_cnx()
