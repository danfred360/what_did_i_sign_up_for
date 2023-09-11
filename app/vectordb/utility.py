import os
from provider import VectorDBProvider
from llm import LLMProvider

class DocumentLoader():
    def __init__(self):
        self.vectordb = VectorDBProvider()
        self.llm = LLMProvider()
        self.file_path = os.environ.get('INPUT_FILES_DIRECTORY')
        if not os.path.exists(self.file_path):
            raise Exception(f'Input directory at {self.file_path} does not exist.')

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
    
    def load_documents_from_input_files_dir(self, generate_embeddings=False):
        collection_directories = os.listdir(self.file_path)
        for collection_name in collection_directories:
            if collection_name == 'README.md':
                continue
            self.vectordb.connect()
            collection = self.vectordb.create_collection(
                collection_name,
                'Generated by Document Loader',
            )
            self.vectordb.disconnect()
            file_class_directories = os.listdir(os.path.join(self.file_path, collection_name))
            for file_class_name in file_class_directories:
                if file_class_name == 'terms_of_service':
                    file_class_id = 1
                elif file_class_name == 'privacy_policy':
                    file_class_id = 2
                else:
                    file_class_id = 3
                file_names = os.listdir(os.path.join(self.file_path, collection_name, file_class_name))
                for file_name in file_names:
                    self.vectordb.connect()
                    file = self.vectordb.create_file(
                        collection['id'],
                        file_class_id,
                        file_name,
                        'Generated by Document Loader',
                        'foo.com'
                    )
                    self.vectordb.disconnect()
                    
                    document_names = os.listdir(os.path.join(self.file_path, collection_name, file_class_name, file_name))
                    for document_name in document_names:
                        document_path = os.path.join(self.file_path, collection_name, file_class_name, file_name, document_name)
                        self.load_document(
                            document_path, 
                            file['id'], 
                            document_name,
                            'Generated by Document Loader', 
                            'foo.com', 
                            generate_embeddings
                        )
        return True


        

        