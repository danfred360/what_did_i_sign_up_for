from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg2 import sql, Error as psycopg2Error
import logging
from .provider import VectorDBProvider
from .llm import LLMProvider

class SearchProvider:
    def __init__(self):
        self.vectordb = VectorDBProvider()
        self.llm = LLMProvider()

    def get_relevant_segments(self, query: str, num_requests: int = 5):
        query_embedding = self.llm.get_embedding(query)

        table_name = "segment"
        embedding_column_name = "embedding"
        fields = ['id', 'document_id', 'content', 'embedding', 'created_at']
        select_query = "SELECT {fields} from {table}"

        search_query = """
            SELECT {fields}
            FROM ({base_query}) AS relevant_segments
            ORDER BY {embedding_column_name} <-> CAST(%s AS vector)
            LIMIT %s
        """

        query = sql.SQL(search_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            base_query=sql.SQL(select_query).format(
                fields=sql.SQL(',').join(map(sql.Identifier, fields)),
                table=sql.Identifier(table_name)
            ),
            embedding_column_name=sql.Identifier(embedding_column_name)
        )

        try:
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (query_embedding, num_requests,))
            query_result = self.vectordb.cursor.fetchall()
            results = [dict(zip(fields, row)) for row in query_result]
            for result in results:
                del result['embedding']
            return {'count': len(results), 'results': results}
        except psycopg2Error as e:
            logging.error(f"Error executing query: {e}")
            logging.info(f"Query: {query.as_string(self.vectordb.cursor)}")
            raise e
        except Exception as e:
            raise e
        finally:
            self.vectordb.disconnect()

    def get_relevant_segments_by_document_id(self, input_query: str, document_id: int, num_segments: int = 5, embedding_column: str = 'embedding'):
        embedding_column_name = embedding_column
        fields = ['id', 'document_id', 'content', 'created_at']
        segments_query = """
            SELECT id, document_id, content, {embedding_column}, created_at
            FROM segment
            WHERE document_id = %s
        """
        search_query = """
            SELECT *
            FROM ({segments_query}) AS relevant_segments
            ORDER BY {embedding_column} <-> CAST(%s AS vector)
            LIMIT %s
        """
        select_query = """
            SELECT {fields}
            FROM ({search_query}) AS relevant_segments_to_return
        """

        query = sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            search_query=sql.SQL(search_query).format(
                fields=sql.SQL(',').join(map(sql.Identifier, fields)),
                segments_query=sql.SQL(segments_query).format(
                        embedding_column=sql.Identifier(embedding_column_name)
                ),
                embedding_column=sql.Identifier(embedding_column_name)
            )
        )

        try:
            input_query_embedding = self.llm.get_embedding(input_query)
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (document_id, input_query_embedding, num_segments,))
            query_result = self.vectordb.cursor.fetchall()
            results = [dict(zip(fields, row)) for row in query_result]
            return {'count': len(results), 'results': results}
        except psycopg2Error as e:
            logging.error(f"Error executing query: {e}")
            logging.info(f"Query: {query.as_string(self.vectordb.cursor)}")
            raise e
        except Exception as e:
            raise e
        finally:
            self.vectordb.disconnect()

    def get_relevant_segments_by_file_id(self, input_query: str, file_id: int, num_segments: int = 5, embedding_column: str = 'embedding'):
        fields = ['id', 'document_id', 'content', 'created_at']
        segments_query = """
            SELECT segment.id, document_id, segment.content, segment.created_at, {embedding_column}
            FROM segment
            JOIN document ON segment.document_id = document.id
            WHERE document.file_id = %s
        """
        search_query = """
            SELECT *
            FROM ({segments_query}) AS relevant_segments
            ORDER BY {embedding_column} <-> CAST(%s AS vector)
            LIMIT %s
        """
        select_query = """
            SELECT {fields}
            FROM ({search_query}) AS relevant_segments_to_return
        """
        query = sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            search_query=sql.SQL(search_query).format(
                segments_query=sql.SQL(segments_query).format(
                    embedding_column=sql.Identifier(embedding_column)
                ),
                embedding_column=sql.Identifier(embedding_column)
            )
        )

        try:
            input_query_embedding = self.llm.get_embedding(input_query)
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (file_id, input_query_embedding, num_segments,))
            query_result = self.vectordb.cursor.fetchall()
            results = [dict(zip(fields, row)) for row in query_result]
            return {'count': len(results), 'results': results}
        except psycopg2Error as e:
            logging.error(f"Error executing query: {e}")
            logging.error(f"Query: {query.as_string(self.vectordb.cursor)}")
            raise e
        except Exception as e:
            raise e
        finally:
            self.vectordb.disconnect()

    def get_relevant_segments_by_collection_id(self, input_query: str, collection_id: int, num_segments: int = 5, embedding_column: str = 'embedding'):
        fields = ['id', 'document_id', 'content', 'created_at']
        segments_query = """
            SELECT segment.id, document_id, segment.content, segment.created_at, {embedding_column}
            FROM segment
            JOIN document ON segment.document_id = document.id
            JOIN file ON document.file_id = file.id
            WHERE file.collection_id = %s
        """
        search_query = """
            SELECT *
            FROM ({segments_query}) AS relevant_segments
            ORDER BY {embedding_column} <-> CAST(%s AS vector)
            LIMIT %s
        """
        select_query = """
            SELECT {fields}
            FROM ({search_query}) AS relevant_segments_to_return
        """
        query = sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            search_query=sql.SQL(search_query).format(
                segments_query=sql.SQL(segments_query).format(
                    embedding_column=sql.Identifier(embedding_column)
                ),
                embedding_column=sql.Identifier(embedding_column)
            )
        )

        try:
            input_query_embedding = self.llm.get_embedding(input_query)
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (collection_id, input_query_embedding, num_segments,))
            query_result = self.vectordb.cursor.fetchall()
            results = [dict(zip(fields, row)) for row in query_result]
            return {'count': len(results), 'results': results}
        except psycopg2Error as e:
            logging.error(f"Error executing query: {e}")
            logging.error(f"Query: {query.as_string(self.vectordb.cursor)}")
            raise e
        except Exception as e:
            raise e
        finally:
            self.vectordb.disconnect()

    def get_relevant_segments_by_file_class_id(self, input_query: str, file_class_id: int, num_segments: int = 5, embedding_column: str = 'embedding'):
        fields = ['id', 'document_id', 'content', 'created_at']
        segments_query = """
            SELECT segment.id, document_id, segment.content, segment.created_at, {embedding_column}
            FROM segment
            JOIN document ON segment.document_id = document.id
            JOIN file ON document.file_id = file.id
            WHERE file.file_class_id = %s
        """
        search_query = """
            SELECT *
            FROM ({segments_query}) AS relevant_segments
            ORDER BY {embedding_column} <-> CAST(%s AS vector)
            LIMIT %s
        """
        select_query = """
            SELECT {fields}
            FROM ({search_query}) AS relevant_segments_to_return
        """
        query = sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            search_query=sql.SQL(search_query).format(
                segments_query=sql.SQL(segments_query).format(
                    embedding_column=sql.Identifier(embedding_column)
                ),
                embedding_column=sql.Identifier(embedding_column)
            )
        )

        try:
            input_query_embedding = self.llm.get_embedding(input_query)
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (file_class_id, input_query_embedding, num_segments,))
            query_result = self.vectordb.cursor.fetchall()
            results = [dict(zip(fields, row)) for row in query_result]
            return {'count': len(results), 'results': results}
        except psycopg2Error as e:
            logging.error(f"Error executing query: {e}")
            logging.error(f"Query: {query.as_string(self.vectordb.cursor)}")
            raise e
        except Exception as e:
            raise e
        finally:
            self.vectordb.disconnect()
