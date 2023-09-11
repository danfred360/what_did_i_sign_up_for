import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .provider import VectorDBProvider, RecordNotFound

class LLMProvider:
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

    def get_embedding(self, text: str):
        embedding = self.embeddings_model.embed_query(text)
        return embedding
    
    def get_embeddings(self, texts: list[str]):
        embeddings = self.embeddings_model.embed_documents(texts)
        return embeddings
    
    def generate_embeddings_for_segment(self, segment_id: int):
        vectordb = VectorDBProvider()
        try:
            vectordb.connect()
            segment = vectordb.get_segment(segment_id)
        except RecordNotFound:
            vectordb.disconnect()
            return False
        vectordb.disconnect()

        text = segment['contents']
        embedding = self.get_embedding(text)

        try:
            vectordb.connect()
            vectordb.update_segment_embedding(segment_id, embedding)
        except RecordNotFound:
            vectordb.disconnect()
            return False
        vectordb.disconnect()
        return True
    
    def generate_segments_for_document(self, document_id: int, generate_embeddings: bool = True):
        vectordb = VectorDBProvider()
        try:
            vectordb.connect()
            document = vectordb.get_file_document(document_id)
        except RecordNotFound:
            vectordb.disconnect()
            return False
        vectordb.disconnect()
        
        text = document['contents']

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 100,
            length_function = len,
            add_start_index = True
        )

        texts = text_splitter.create_documents([text])
        if generate_embeddings:
            embeddings = self.get_embeddings(list(map(lambda x: x.page_content, texts)))
            for i in range(len(texts)):
                try:
                    vectordb.connect()
                    vectordb.create_document_segment(
                        document_id, 
                        embedding = embeddings[i], 
                        content = texts[i].page_content
                    )
                except RecordNotFound:
                    vectordb.disconnect()
                    return False
                vectordb.disconnect()
        else:
            for i in range(len(texts)):
                try:
                    vectordb.connect()
                    vectordb.create_document_segment(
                        document_id,  
                        content = texts[i].page_content
                    )
                except RecordNotFound:
                    vectordb.disconnect()
                    return False
                vectordb.disconnect()

        return True
