CREATE TABLE person (
    username TEXT PRIMARY KEY,
    hashed_password TEXT,
    salt TEXT,
    first_name TEXT NULL,
    last_name TEXT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    image_url TEXT NULL
);

CREATE TABLE collection (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES person(username),
    parent_collection_id INTEGER REFERENCES collection(id) NULL,
    name TEXT,
    description TEXT,
    image_url TEXT NULL
);

CREATE TABLE file_class (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    image_url TEXT NULL
);

CREATE TABLE file (
    id SERIAL PRIMARY KEY,
    url TEXT,
    name TEXT,
    description TEXT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    file_class_id INTEGER REFERENCES file_class(id),
    collection_id INTEGER REFERENCES collection(id)
);

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    file_id INTEGER REFERENCES file(id),
    name TEXT,
    description TEXT NULL,
    url TEXT NULL,
    contents TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE segment (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(1536),
    potential_questions VECTOR(1536) NULL,
    document_id INTEGER REFERENCES document(id),
    start_line INTEGER NULL,
    end_line INTEGER NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
