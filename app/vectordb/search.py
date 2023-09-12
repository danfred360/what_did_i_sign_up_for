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
        table_name = "segment"
        embedding_column_name = embedding_column
        fields = ['id', 'document_id', 'content', embedding_column_name, 'created_at']
        select_query = "SELECT {fields} from {table} WHERE document_id = %s"

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
            input_query_embedding = self.llm.get_embedding(input_query)
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (document_id, input_query_embedding, num_segments,))
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

    def get_relevant_segments_by_file_id(self, input_query: str, file_id: int, num_segments: int = 5, embedding_column: str = 'embedding'):
        table_name = "segment"
        fields = ['id', 'document_id', 'content', embedding_column, 'created_at']
        documents_query = """
            SELECT id
            FROM document
            WHERE file_id = %s
        """
        segments_query = """
            SELECT {fields}
            FROM {table}
            WHERE document_id IN ({documents_query})
        """
        search_query = """
            SELECT {fields}
            FROM ({segments_query}) AS relevant_segments
            ORDER BY {embedding_column_name} <-> CAST(%s AS vector)
            LIMIT %s
        """
        query = sql.SQL(search_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            segments_query=sql.SQL(segments_query).format(
                fields=sql.SQL(',').join(map(sql.Identifier, fields)),
                table=sql.Identifier(table_name),
                documents_query=sql.SQL(documents_query)
            ),
            embedding_column_name=sql.Identifier(embedding_column)
        )

        try:
            input_query_embedding = self.llm.get_embedding(input_query)
            self.vectordb.connect()
            self.vectordb.cursor.execute(query, (file_id, input_query_embedding, num_segments,))
            query_result = self.vectordb.cursor.fetchall()
            results = [dict(zip(fields, row)) for row in query_result]
            for result in results:
                del result[embedding_column]
            return {'count': len(results), 'results': results}
        except psycopg2Error as e:
            logging.error(f"Error executing query: {e}")
            logging.info(f"Query: {query.as_string(self.vectordb.cursor)}")
            raise e
        except Exception as e:
            raise e
        finally:
            self.vectordb.disconnect()
