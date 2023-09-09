# goals

- ingest terms of service document or privacy policy document
- maintain vectordb of embeddings and metadata
- provide search api for querying vectordb
- provide question and answer api for querying gpt4 using vectordb for context

## systems

### vectordb
use postgres with the pgvector extension. this will allow us to store embeddings and metadata in the same database. we can use the metadata to filter the embeddings and return the most relevant results.

```mermaid
erDiagram
    ENTITY segment {
        id int
        embedding vector
        potential_questions vector
        source_document_id int
        start_line int
        end_line int
        content string
    }

    ENTITY document {
        id int
        source_file_id int
        title string
    }

    ENTITY file {
        id int
        url uri
        title string
        description string
        class_id int
    }

    ENTITY class {
        id int
        name string
        description string
    }

    ENTITY collection {
        id int
        parent_collection_id int
        name string
        description string
        image uri
    }

    segment ||--o{ document : "source_document_id"
    document ||--o{ file : "source_file_id"
    file ||--o{ class : "class_id"
    file ||--o{ collection : "collection_id"
    collection ||--o{ collection : "parent_collection_id"
```

### vectordb provider
python module for interacting with vectordb. this will be used by the web app and the cli app. semantic search by creating an embedding of the search query and comparing it to the embeddings in vectordb. also takes parameters for filtering by metadata.

filters:
- knowledge source
    - terms of service documents or privacy policy documents, broken into groups by country or however the user chooses.
- preperation method
    - embeddings stored in database will have been prepared. break down source document into chunks and append additional metadata to each chunk. 
        - use gpt4 to create a list of possible questions related to that segment. this will make the search more effective when searching for matches with a user's query from the question and answer system.

both the web app and the cli will need to be able to interact with this module

### gpt4 provider
lean on langchain here.

### search api
web api with functions built towards searching the vectordb for relevant segments. web app will have a section that is dedicated to seartching and displaying the results in a useful manner. user will select filters (collections, files, documents, segments)


### question and answer api
python module for interacting with gpt4 provider and vectordb. this will be used by the web app and the cli app.



    - use search api to build context?
### web app
use swagger to build out functionality. split into two key features: search and question and answer.

build a frontend that is as light as possible. html css and light js.
### cli app
python cli for interacting with the search and quest and answer python components from the terminal or when scripting.