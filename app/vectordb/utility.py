import os
from provider import VectorDBProvider
from llm import LLMProvider

class DocumentLoader():
    def __init__(self):
        self.vectordb = VectorDBProvider()
        self.llm = LLMProvider()

    def load_document(self, file_path: str, file_id: int, name: str, description: str, url: str, generate_embeddings: bool = True):
        if not os.path.exists(file_path):
            raise Exception(f'File {file_path} not found')

        with open(file_path, 'r') as f:
            contents = f.read()

        try:
            self.vectordb.connect()
            document = self.vectordb.create_file_document(
                file_id, 
                name, 
                description, 
                contents, 
                url
            )
        except Exception as e:
            self.vectordb.disconnect()
            raise e
        self.vectordb.disconnect()

        try:
            self.llm.generate_segments_for_document(document['id'], generate_embeddings)
        except Exception as e:
            raise e
        return document

        

        