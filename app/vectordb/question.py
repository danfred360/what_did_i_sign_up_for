from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate)
from langchain.chains import LLMChain
from .provider import VectorDBProvider
from .search import SearchProvider
import logging

class QuestionAnswerer():
    def __init__(self):
        self.search = SearchProvider()
        self.vectordb = VectorDBProvider()

        system_template = """
            You are a helpful assistant that answers questions based on 
            the context that is provided. Please only answer the question
            if the answer is in the context. If the answer is not in the
            context, please response with "I don't have enough information
            to answer the question." When you refer to the context, use the 
            relevant document name for the content that you are referring to,
            and don't refer to the context as "the context".
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_template = """
            Context: {context}

            Question: {question}
        """
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        self.chain = LLMChain(
            llm = ChatOpenAI(),
            prompt = chat_prompt
        )
    
    def format_context_from_search_results(self, search_results: dict):
        context = ''
        try:
            self.vectordb.connect()
            for segment in search_results['results']:
                del segment['id']
                del segment['created_at']
                document_name = self.vectordb.get_file_document_name_by_id(segment['document_id'])
                del segment['document_id']
                segment['document_name'] = document_name['name']
                context += f'\tdocument name:\n{segment["document_name"]}\n\trelevant segment:\n{segment["content"]}\n\n'
        except Exception as e:
            logging.error(f'ran into an error formatting context from search results: {e}')
            raise e
        finally:
            self.vectordb.disconnect()
        return context

    def answer_question(self, input_query: str):
            try:
                self.vectordb.connect()
                search_results = self.search.get_relevant_segments(input_query)
            except Exception as e:
                logging.error(f'ran into an error getting relevant segments: {e}')
                raise e
            finally:
                 self.vectordb.disconnect()

            try:
                context = self.format_context_from_search_results(search_results)
                answer = self.chain.run({'context': context, 'question': input_query})
            except Exception as e:
                logging.error(f'ran into an error running question answer chain: {e}')
                raise e
            return {'answer': answer}
    
    def answer_question_by_document_id(self, input_query: str, document_id: int):
            try:
                self.vectordb.connect()
                search_results = self.search.get_relevant_segments_by_document_id(input_query, document_id)
            except Exception as e:
                logging.error(f'ran into an error getting relevant segments: {e}')
                raise e
            finally:
                 self.vectordb.disconnect()

            try:
                context = self.format_context_from_search_results(search_results)
                answer = self.chain.run({'context': context, 'question': input_query})
            except Exception as e:
                logging.error(f'ran into an error running question answer chain: {e}')
                raise e
            return {'answer': answer}
    
    def answer_question_by_file_id(self, input_query: str, file_id: int):
            try:
                self.vectordb.connect()
                search_results = self.search.get_relevant_segments_by_file_id(input_query, file_id)
            except Exception as e:
                logging.error(f'ran into an error getting relevant segments: {e}')
                raise e
            finally:
                 self.vectordb.disconnect()

            try:
                context = self.format_context_from_search_results(search_results)
                answer = self.chain.run({'context': context, 'question': input_query})
            except Exception as e:
                logging.error(f'ran into an error running question answer chain: {e}')
                raise e
            return {'answer': answer}
    
    def answer_question_by_collection_id(self, input_query: str, collection_id: int):
            try:
                self.vectordb.connect()
                search_results = self.search.get_relevant_segments_by_collection_id(input_query, collection_id)
            except Exception as e:
                logging.error(f'ran into an error getting relevant segments: {e}')
                raise e
            finally:
                 self.vectordb.disconnect()

            try:
                context = self.format_context_from_search_results(search_results)
                answer = self.chain.run({'context': context, 'question': input_query})
            except Exception as e:
                logging.error(f'ran into an error running question answer chain: {e}')
                raise e
            return {'answer': answer}
    
    def answer_question_by_file_class_id(self, input_query: str, file_class_id: int):
            try:
                self.vectordb.connect()
                search_results = self.search.get_relevant_segments_by_file_class_id(input_query, file_class_id)
            except Exception as e:
                logging.error(f'ran into an error getting relevant segments: {e}')
                raise e
            finally:
                 self.vectordb.disconnect()

            try:
                context = self.format_context_from_search_results(search_results)
                answer = self.chain.run({'context': context, 'question': input_query})
            except Exception as e:
                logging.error(f'ran into an error running question answer chain: {e}')
                raise e
            return {'answer': answer}