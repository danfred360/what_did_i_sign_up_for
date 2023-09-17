import os
import psycopg2
from psycopg2 import OperationalError
import logging

class VectorDBProvider:
    def __init__(self):
        self.dbname = "vectordb"
        self.user = "postgres"
        self.password = os.environ.get('VECTORDB_PASSWORD')
        self.host = os.environ.get('VECTORDB_HOST')
        self.port = os.environ.get('VECTORDB_PORT')
        self.conn = None

    def set_dbname(self, dbname):
        self.dbname = dbname

    def set_user(self, user):
        self.user = user

    def set_password(self, password):
        self.password = password

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port

    def set_conn(self, conn):
        self.conn = conn

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
        except OperationalError as e:
            logging.error(f"Unable to connect to database: {e}")
            raise e


    def disconnect(self):
        self.conn.close()

    def create_user(self, username, hashed_password, salt):
        sql_query = "INSERT INTO person (username, hashed_password, salt) VALUES (%s, %s, %s)"
        self.cursor.execute(sql_query, (username, hashed_password, salt))
        self.conn.commit()

    def get_user(self, username):
        sql_query = "SELECT username, hashed_password, salt FROM person WHERE username=%s"
        self.cursor.execute(sql_query, (username,))
        user = self.cursor.fetchone()
        if user:
            return {"username": user[0], "hashed_password": user[1], "salt": user[2]}
        else:
            return None
