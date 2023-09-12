import os
from datetime import datetime
import psycopg2
from psycopg2 import sql, OperationalError
import logging

class RecordNotFound(Exception):
    pass

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

    # collections

    def list_collections(self):
        table_name = "collection"
        fields = ['id', 'parent_collection_id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table}').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        )
        self.cursor.execute(query)

        response =  self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            return response_dict
        else:
            raise RecordNotFound("No records found")

    def get_collection(self, collection_id):
        table_name = "collection"
        column_name = "id"
        fields = ['id', 'parent_collection_id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (collection_id,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with id {collection_id} not found")
        
    def get_collection_by_name(self, name):
        table_name = "collection"
        column_name = "name"
        fields = ['id', 'parent_collection_id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (name,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with name {name} not found")
        

    def get_collections(self, collection_ids):
        if not collection_ids:
            raise ValueError('Collection ids are required')
        if not isinstance(collection_ids, list):
            raise ValueError('Collection ids must be a list')
        if not all(isinstance(collection_id, int) for collection_id in collection_ids):
            raise ValueError('Collection ids must be integers')
        
        table_name = "collection"
        column_name = "id"
        fields = ['id', 'parent_collection_id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} IN %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (tuple(collection_ids),))

        response = self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            return response_dict
        else:
            raise RecordNotFound(f"Records with ids {collection_ids} not found")

    def create_collection(self, name, description, parent_collection_id=None, image_url=None):
        if not name or not description:
            raise ValueError('Name and description are required')
        if not isinstance(name, str) or not isinstance(description, str):
            raise ValueError('Name and description must be strings')
        if parent_collection_id and not isinstance(parent_collection_id, int):
            raise ValueError('Parent collection id must be an integer')
        if image_url and not isinstance(image_url, str):
            raise ValueError('Image url must be a string')
        
        table_name = "collection"
        response_fields = ['id', 'parent_collection_id', 'name', 'description', 'image_url']
        if parent_collection_id:
            fields = ['parent_collection_id', 'name', 'description']
            values = [parent_collection_id, name, description]
        else:
            fields = ['name', 'description']
            values = [name, description]
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
            raise RecordNotFound(f"Record with name {name} not created")
        

    def update_collection(self, collection_id, name=None, description=None, parent_collection_id=None, image_url=None):
        if not collection_id:
            raise ValueError('Collection id is required')
        if not isinstance(collection_id, int):
            raise ValueError('Collection id must be an integer')
        if name and not isinstance(name, str):
            raise ValueError('Name must be a string')
        if description and not isinstance(description, str):
            raise ValueError('Description must be a string')
        if parent_collection_id and not isinstance(parent_collection_id, int):
            raise ValueError('Parent collection id must be an integer')
        if image_url and not isinstance(image_url, str):
            raise ValueError('Image url must be a string')
        
        table_name = "collection"
        column_name = "id"
        response_fields = ['id', 'parent_collection_id', 'name', 'description', 'image_url']
        fields = []
        values = []
        if name:
            fields.append('name')
            values.append(name)
        if description:
            fields.append('description')
            values.append(description)
        if parent_collection_id:
            fields.append('parent_collection_id')
            values.append(parent_collection_id)
        if image_url:
            fields.append('image_url')
            values.append(image_url)
        query = sql.SQL('UPDATE {table} SET ({fields}) = ({values}) WHERE {column} = %s RETURNING {response_fields}').format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            values=sql.SQL(',').join(map(sql.Literal, values)),
            column=sql.Identifier(column_name),
            response_fields=sql.SQL(',').join(map(sql.Identifier, response_fields))
        )
        self.cursor.execute(query, (collection_id,))
        self.conn.commit()
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with id {collection_id} not found")
        
    def delete_collection(self, collection_id):
        if not collection_id:
            raise ValueError('Collection id is required')
        if not isinstance(collection_id, int):
            raise ValueError('Collection id must be an integer')
        
        table_name = "collection"
        column_name = "id"
        query = sql.SQL('DELETE FROM {table} WHERE {column} = %s').format(
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (collection_id,))
        self.conn.commit()
        
        if self.cursor.rowcount == 0:
            raise RecordNotFound(f"Record with id {collection_id} not found")
        else:
            return True
        
    # file_classes
    def list_file_classes(self):
        table_name = "file_class"
        fields = ['id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table}').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        )
        self.cursor.execute(query)

        response =  self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            return response_dict
        else:
            raise RecordNotFound("No records found")
        
    def get_file_class(self, file_class_id):
        table_name = "file_class"
        column_name = "id"
        fields = ['id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (file_class_id,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with id {file_class_id} not found")
        
    def get_file_class_by_name(self, name):
        table_name = "file_class"
        column_name = "name"
        fields = ['id', 'name', 'description', 'image_url']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (name,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with name {name} not found")
        
    def create_file_class(self, name, description, image_url=None):
        table_name = "file_class"
        response_fields = ['id', 'name', 'description', 'image_url']
        fields = ['name', 'description']
        values = [name, description]
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
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with name {name} not created")
        
    def update_file_class(self, file_class_id, name=None, description=None, image_url=None):
        if not file_class_id:
            raise ValueError('file_class id is required')
        if not isinstance(file_class_id, int):
            raise ValueError('file_class id must be an integer')
        if name and not isinstance(name, str):
            raise ValueError('Name must be a string')
        if description and not isinstance(description, str):
            raise ValueError('Description must be a string')
        if image_url and not isinstance(image_url, str):
            raise ValueError('Image url must be a string')
        
        table_name = "file_class"
        column_name = "id"
        response_fields = ['id', 'name', 'description', 'image_url']
        fields = []
        values = []
        if name:
            fields.append('name')
            values.append(name)
        if description:
            fields.append('description')
            values.append(description)
        if image_url:
            fields.append('image_url')
            values.append(image_url)
        query = sql.SQL('UPDATE {table} SET ({fields}) = ({values}) WHERE {column} = %s RETURNING {response_fields}').format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            values=sql.SQL(',').join(map(sql.Literal, values)),
            column=sql.Identifier(column_name),
            response_fields=sql.SQL(',').join(map(sql.Identifier, response_fields))
        )
        self.cursor.execute(query, (file_class_id,))
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Record with id {file_class_id} not found")
        
    def delete_file_class(self, file_class_id):
        if not file_class_id:
            raise ValueError('file_class id is required')
        if not isinstance(file_class_id, int):
            raise ValueError('file_class id must be an integer')
        
        table_name = "file_class"
        column_name = "id"
        query = sql.SQL('DELETE FROM {table} WHERE {column} = %s').format(
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (file_class_id,))
        
        if self.cursor.rowcount == 0:
            raise RecordNotFound(f"Record with id {file_class_id} not found")
        else:
            return True

    # files
        
    def list_files(self):
        table_name = "file"
        fields = ['id', 'collection_id', 'file_class_id', 'name', 'description', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table}').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        )
        self.cursor.execute(query)

        response =  self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            return response_dict
        else:
            raise RecordNotFound("No files found")
        
    def get_file(self, file_id):
        table_name = "file"
        column_name = "id"
        fields = ['id', 'collection_id', 'file_class_id', 'name', 'description', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (file_id,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"File with id {file_id} not found")
        
    def get_file_by_name(self, name):
        table_name = "file"
        column_name = "name"
        fields = ['id', 'collection_id', 'file_class_id', 'name', 'description', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (name,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"File with name {name} not found")
        
    def create_file(self, collection_id: int, file_class_id: int, name: str, description: str, url: str):
        table_name = "file"
        response_fields = ['id', 'collection_id', 'file_class_id', 'name', 'description', 'url', 'created_at', 'updated_at']
        fields = ['collection_id', 'file_class_id', 'name', 'description', 'url']
        values = [collection_id, file_class_id, name, description, url]
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
            raise RecordNotFound(f"File with name {name} not created")
        
    def update_file(self, file_id, name=None, description=None, url=None):
        if not file_id:
            raise ValueError('File id is required')
        if not isinstance(file_id, int):
            raise ValueError('File id must be an integer')
        if name and not isinstance(name, str):
            raise ValueError('Name must be a string')
        if description and not isinstance(description, str):
            raise ValueError('Description must be a string')
        if url and not isinstance(url, str):
            raise ValueError('File url must be a string')
        
        table_name = "file"
        column_name = "id"
        response_fields = ['id', 'collection_id', 'name', 'description', 'url', 'created_at', 'updated_at']
        fields = ['updated_at']
        values = [datetime.now()]
        if name:
            fields.append('name')
            values.append(name)
        if description:
            fields.append('description')
            values.append(description)
        if url:
            fields.append('url')
            values.append(url)
        update_query = """
            UPDATE {table}
            SET ({fields}) = (
                SELECT {values} 
                WHERE {column} = %s)
            RETURNING {response_fields}
        """
        query = sql.SQL(update_query).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            values=sql.SQL(',').join(map(sql.Literal, values)),
            column=sql.Identifier(column_name),
            response_fields=sql.SQL(',').join(map(sql.Identifier, response_fields))
        )
        self.cursor.execute(query, (file_id,))
        self.conn.commit()
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"File with id {file_id} not found")
        
    def delete_file(self, file_id):
        if not file_id:
            raise ValueError('File id is required')
        if not isinstance(file_id, int):
            raise ValueError('File id must be an integer')
        
        table_name = "file"
        column_name = "id"
        query = sql.SQL('DELETE FROM {table} WHERE {column} = %s').format(
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (file_id,))
        self.conn.commit()
        
        if self.cursor.rowcount == 0:
            raise RecordNotFound(f"File with id {file_id} not found")
        else:
            return True
        
    # documents
    def list_file_documents(self, file_id):
        table_name = "document"
        column_name = "file_id"
        fields = ['id', 'file_id', 'name', 'description', 'contents', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (file_id,))

        response =  self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            return response_dict
        else:
            # return RecordNotFound("No documents found")
            return None
        
    def list_documents(self):
        table_name = "document"
        fields = ['id', 'file_id', 'name', 'description', 'contents', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table}').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        )
        self.cursor.execute(query)

        response =  self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            for document in response_dict:
                del document['contents']
            return response_dict
        else:
            raise RecordNotFound("No documents found")
        
    def get_file_document(self, document_id):
        table_name = "document"
        column_name = "id"
        fields = ['id', 'file_id', 'name', 'description', 'contents', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (document_id,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            return None
        
    def get_file_document_name_by_id(self, id: int):
        table_name = "document"
        column_name = "id"
        fields = ['name']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        try:
            self.cursor.execute(query, (id,))
            response = self.cursor.fetchone()
        except Exception as e:
            raise e
        if response: 
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound
        
    def get_file_document_by_name(self, file_id, name):
        table_name = "document"
        fields = ['id', 'file_id', 'name', 'description', 'url', 'created_at', 'updated_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE file_id = %s AND name = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
        )
        try:
            self.cursor.execute(query, (file_id, name,))

            response = self.cursor.fetchone()
        except Exception as e:
            raise e
        if response: 
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound
        
    def create_file_document(self, file_id, name, description, contents, url):
        if not file_id or not name or not description or not contents or not url:
            raise ValueError('File id, name, description, contents, and url are required')
        if not isinstance(file_id, int):
            raise ValueError('File id must be an integer')
        if not isinstance(name, str):
            raise ValueError('Name must be a string')
        if not isinstance(description, str):
            raise ValueError('Description must be a string')
        if not isinstance(contents, str):
            raise ValueError('Contents must be a string')
        if not isinstance(url, str):
            raise ValueError('File url must be a string')
          
        table_name = "document"
        response_fields = ['id', 'file_id', 'name', 'description', 'contents', 'url', 'created_at', 'updated_at']
        fields = ['file_id', 'name', 'description', 'contents', 'url']
        values = [file_id, name, description, contents, url]
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
            raise Exception(f"Failed to create document with name {name} not created")
        
    def update_file_document(self, document_id, name=None, description=None, contents=None, url=None):
        if not document_id:
            raise ValueError('Document id is required')
        if not isinstance(document_id, int):
            raise ValueError('Document id must be an integer')
        if name and not isinstance(name, str):
            raise ValueError('Name must be a string')
        if description and not isinstance(description, str):
            raise ValueError('Description must be a string')
        if contents and not isinstance(contents, str):
            raise ValueError('Contents must be a string')
        if url and not isinstance(url, str):
            raise ValueError('File url must be a string')
        
        table_name = "document"
        column_name = "id"
        response_fields = ['id', 'file_id', 'name', 'description', 'contents', 'url', 'created_at', 'updated_at']
        fields = ['updated_at']
        values = [datetime.now()]
        if name:
            fields.append('name')
            values.append(name)
        if description:
            fields.append('description')
            values.append(description)
        if contents:
            fields.append('contents')
            values.append(contents)
        if url:
            fields.append('url')
            values.append(url)
        query = sql.SQL('UPDATE {table} SET ({fields}) = ({values}) WHERE {column} = %s RETURNING {response_fields}').format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            values=sql.SQL(',').join(map(sql.Literal, values)),
            column=sql.Identifier(column_name),
            response_fields=sql.SQL(',').join(map(sql.Identifier, response_fields))
        )
        self.cursor.execute(query, (document_id,))
        self.conn.commit()
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Document with id {document_id} not found")
        
    def delete_file_document(self, document_id):
        if not document_id:
            raise ValueError('Document id is required')
        if not isinstance(document_id, int):
            raise ValueError('Document id must be an integer')
        
        table_name = "document"
        column_name = "id"
        query = sql.SQL('DELETE FROM {table} WHERE {column} = %s').format(
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (document_id,))
        
        if self.cursor.rowcount == 0:
            raise RecordNotFound(f"Document with id {document_id} not found")
        else:
            return True
        
    # segments

    def list_document_segments(self, document_id):
        table_name = "segment"
        column_name = "document_id"
        fields = ['id', 'document_id', 'embedding', 'potential_questions', 'start_line', 'end_line', 'content', 'created_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (document_id,))

        response =  self.cursor.fetchall()
        if response:
            response_dict = [dict(zip(fields, row)) for row in response]
            return response_dict
        else:
            raise RecordNotFound("No segments found")
        
    def get_document_segment(self, segment_id):
        table_name = "segment"
        column_name = "id"
        fields = ['id', 'document_id', 'embedding', 'potential_questions', 'start_line', 'end_line', 'content', 'created_at']
        query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s').format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (segment_id,))

        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Segment with id {segment_id} not found")
        
    def create_document_segment(self, document_id,  content, embedding=None, potential_questions=None, start_line=None, end_line=None):
        if not document_id or not content:
            raise ValueError('Document id, potential questions, and content are required')
        if not isinstance(document_id, int):
            raise ValueError('Document id must be an integer')
        if embedding and not isinstance(embedding, list):
            raise ValueError('Embedding must be a list')
        if potential_questions and not isinstance(potential_questions, list):
            raise ValueError('Potential questions must be a list')
        if start_line and not isinstance(start_line, int):
            raise ValueError('Start line must be an integer')
        if end_line and not isinstance(end_line, int):
            raise ValueError('End line must be an integer')
        if not isinstance(content, str):
            raise ValueError('Content must be a string')
          
        table_name = "segment"
        response_fields = ['id', 'embedding', 'potential_questions', 'start_line', 'end_line', 'content', 'created_at']
        fields = ['document_id', 'embedding', 'potential_questions', 'start_line', 'end_line', 'content']
        values = [document_id, embedding, potential_questions, start_line, end_line, content]
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
            raise RecordNotFound(f"Segment with content {content} not created")
        
    def update_document_segment(self, 
        segment_id, 
        embedding=None, 
        potential_questions=None, 
        source_document_id=None, 
        start_line=None, 
        end_line=None, 
        content=None
        ):
        if not segment_id:
            raise ValueError('Segment id is required')
        if not isinstance(segment_id, int):
            raise ValueError('Segment id must be an integer')
        if embedding and not isinstance(embedding, list):
            raise ValueError('Embedding must be a list')
        if potential_questions and not isinstance(potential_questions, list):
            raise ValueError('Potential questions must be a list')
        if source_document_id and not isinstance(source_document_id, int):
            raise ValueError('Source document id must be an integer')
        if start_line and not isinstance(start_line, int):
            raise ValueError('Start line must be an integer')
        if end_line and not isinstance(end_line, int):
            raise ValueError('End line must be an integer')
        if content and not isinstance(content, str):
            raise ValueError('Content must be a string')
        
        table_name = "segment"
        column_name = "id"
        response_fields = ['id', 'embedding', 'potential_questions', 'source_document_id', 'start_line', 'end_line', 'content', 'created_at']
        fields = ['updated_at']
        values = [datetime.now()]
        if embedding:
            fields.append('embedding')
            values.append(embedding)
        if potential_questions:
            fields.append('potential_questions')
            values.append(potential_questions)
        if source_document_id:
            fields.append('source_document_id')
            values.append(source_document_id)
        if start_line:
            fields.append('start_line')
            values.append(start_line)
        if end_line:
            fields.append('end_line')
            values.append(end_line)
        if content:
            fields.append('content')
            values.append(content)
        query = sql.SQL('UPDATE {table} SET ({fields}) = ({values}) WHERE {column} = %s RETURNING {response_fields}').format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            values=sql.SQL(',').join(map(sql.Literal, values)),
            column=sql.Identifier(column_name),
            response_fields=sql.SQL(',').join(map(sql.Identifier, response_fields))
        )
        self.cursor.execute(query, (segment_id,))
        self.conn.commit()
        
        response = self.cursor.fetchone()
        if response:
            response_dict = dict(zip(response_fields, response))
            return response_dict
        else:
            raise RecordNotFound(f"Segment with id {segment_id} not found")
        
    def delete_document_segment(self, segment_id):
        if not segment_id:
            raise ValueError('Segment id is required')
        if not isinstance(segment_id, int):
            raise ValueError('Segment id must be an integer')
        
        table_name = "segment"
        column_name = "id"
        query = sql.SQL('DELETE FROM {table} WHERE {column} = %s').format(
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        self.cursor.execute(query, (segment_id,))
        
        if self.cursor.rowcount == 0:
            raise RecordNotFound(f"Segment with id {segment_id} not found")
        else:
            return True
        