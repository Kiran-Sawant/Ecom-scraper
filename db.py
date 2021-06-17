from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from conf import DB_CONNECTION_STR

connection = create_engine(DB_CONNECTION_STR)

def verify_table(table_name:str):

    return connection.dialect.has_table(connection, table_name)

session1 = Session(connection)