from provider import VectorDBProvider
from utility import DocumentLoader
from dotenv import load_dotenv

load_dotenv()

def init_file():
    vectordb = VectorDBProvider()
    vectordb.connect()
    collection = vectordb.create_collection('Rental House', 'foobar')
    file = vectordb.create_file(
        collection['id'],
        1,
        'Rental Wifi Terms of Use',
        'Terms of use for rental wifi',
        'https://www.rentalwifi.com/terms_of_use'
    )
    vectordb.disconnect()
    print(file)

def get_segments(document_id: int):
    document_id = document_id

    vectordb = VectorDBProvider()
    vectordb.connect()
    segments = vectordb.list_document_segments(document_id)
    vectordb.disconnect()
    print(segments)

def load_doc():
    loader = DocumentLoader()

    path = '/Users/dpfrederick/code/ai-consortium/what_did_i_sign_up_for/input_files/rental_wifi/terms_of_use.txt'
    file_id = 5
    name = 'Rental Wifi Terms of Use'
    description = 'Terms of use for rental wifi'
    url = 'https://www.rentalwifi.com/terms_of_use'

    document = loader.load_document(
        path, 
        file_id, 
        name, 
        description, 
        url, 
        generate_embeddings = True
    )

    get_segments(document['id'])

#init_file()

load_doc()