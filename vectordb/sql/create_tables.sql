CREATE TABLE  collection (
    id SERIAL PRIMARY KEY,
    parent_collection_id INTEGER REFERENCES collection(id) NULL,
    name TEXT,
    description TEXT,
    image_url TEXT
);

CREATE TABLE class (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    image_url TEXT
);

CREATE TABLE file (
    id SERIAL PRIMARY KEY,
    url TEXT,
    title TEXT,
    description TEXT NULL,
    class_id INTEGER REFERENCES class(id),
    collection_id INTEGER REFERENCES collection(id)
);

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    source_file_id INTEGER REFERENCES file(id),
    title TEXT
);

CREATE TABLE segment (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(1536),
    potential_questions VECTOR(1536),
    source_document_id INTEGER REFERENCES document(id),
    start_line INTEGER,
    end_line INTEGER,
    content TEXT
);
