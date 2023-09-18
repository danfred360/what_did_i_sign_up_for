import os
import psycopg2
from psycopg2 import OperationalError, sql
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

    def create_collection(self, user_id, name, description, parent_collection_id=None, image_url=None):
        table_name = "collection"
        response_fields = ['id', 'user_id', 'parent_collection_id', 'name', 'description', 'image_url']
        if parent_collection_id:
            fields = ['user_id', 'parent_collection_id', 'name', 'description']
            values = [user_id, parent_collection_id, name, description]
        else:
            fields = ['user_id', 'name', 'description']
            values = [user_id, name, description]
        if image_url:
            fields.append('image_url')
            values.append(image_url)
        query = sql.SQL('INSERT INTO {table} ({fields}) VALUES ({values}) RETURNING {response_fields}').format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            values=sql.SQL(',').join(map(sql.Literal, values)),
            response_fields=sql.SQL(',').join(map(sql.Identifier, response_fields))
        )
        self.cursor.execute(query)
        self.conn.commit()
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise Exception(f"Record with name {name} not created")

    def create_user(self, username, hashed_password, salt):
        user_query = "INSERT INTO person (username, hashed_password, salt) VALUES (%s, %s, %s)"
        self.cursor.execute(user_query, (username, hashed_password, salt))
        self.conn.commit()
        self.create_collection(username, 'Default', f'Default collection for {username}')

    def get_user(self, username):
        sql_query = "SELECT username, hashed_password, salt FROM person WHERE username=%s"
        self.cursor.execute(sql_query, (username,))
        user = self.cursor.fetchone()
        if user:
            return {"username": user[0], "hashed_password": user[1], "salt": user[2]}
        else:
            return None
