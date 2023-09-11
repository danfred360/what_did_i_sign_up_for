# vectordb

## local development
```bash
# start container
cd vectordb
docker compose up -d

# force rebuild container if making changes to Dockerfile or seed scripts
docker compose up -d --build --force-recreate --remove-orphans

# connect to running container
docker exec -it vectordb bash

# start psql utility
psql -h localhost -U postgres -d vectordb
```

useful psql commands:
```sql
-- list tables in database
\dt;

-- list columns in table
\d+ table_name;

-- select * from table
select * from table_name;

-- list indexes in table
\di+ table_name;

-- list functions in database
\df;

-- list triggers in database
\dft;
```

## schema
```mermaid
erDiagram vectordb
    ENTITY segment {
        id int
        embedding vector
        potential_questions vector
        source_document_id int
        start_line int
        end_line int
        content text
        created_at datetime
    }

    ENTITY document {
        id int
        file_id int
        name text
        description text
        url text
        contents text
        created_at datetime
        updated_at datetime
    }

    ENTITY file {
        id int
        url text
        name text
        description text
        created_at datetime
        updated_at datetime
        file_class_id int
        collection_id int
    }

    ENTITY file_class {
        id int
        name text
        description text
        image_url text
    }

    ENTITY collection {
        id int
        parent_collection_id int
        name text
        description text
        image_url text
    }

    segment ||--o{ document : "source_document_id"
    document ||--o{ file : "source_file_id"
    file ||--o{ file_class : "file_class_id"
    file ||--o{ collection : "collection_id"
    collection ||--o{ collection : "parent_collection_id"
```
## resources
- [pgvector](https://github.com/pgvector/pgvector)
- https://neon.tech/docs/extensions/pgvector