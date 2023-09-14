import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
from openai.error import RateLimitError
from .provider import VectorDBProvider, RecordNotFound
import logging

class LLMProvider:
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))
        self.llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

    def get_embedding(self, text: str):
        try:
            embedding = self.embeddings_model.embed_query(text)
        except Exception as e:
            logging.error(f'llm provider error: {e}')
            raise e
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
    
    def generate_possible_question_embeddings_for_segment(self, segment_id: int):
        raise NotImplementedError
    
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
    
    def extract_document_metadata(self, content: str, schema: dict):
        try:
            metadata = create_extraction_chain(schema=schema, llm=self.llm).run(content)
        except RateLimitError as e:
            raise e
        except Exception as e:
            raise e
        return metadata
