import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from .provider import VectorDBProvider, RecordNotFound
import logging

class LLMProvider:
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

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
    
    def answer_question(self, input_query: str):
        system_template = """
            You are a helpful assistant that answers questions based on 
            the context that is provided. Please only answer the question
            if the answer is in the context. If the answer is not in the
            context, please response with "I don't have enough information
            to answer the question."
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_template = """
            Context: {context}

            Question: {question}
        """
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(
            llm = ChatOpenAI(),
            prompt = chat_prompt
        )

        try:
            answer = chain.run({'context': 'foo', 'question': input_query})
        except Exception as e:
            logging.error(f'llm provider error: {e}')
            raise e
        return {'answer': answer}
