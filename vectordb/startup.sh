#!/bin/bash
set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

echo "creating vectodb database"
# Create the vectordb database
"${psql[@]}" --dbname="$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE vectordb;
EOSQL

echo "running sql init files"
# run sql init files
echo "loading extensions..."
"${psql[@]}" --dbname="vectordb" -f /sqlscripts/load_extensions.sql
echo "creating tables..."
"${psql[@]}" --dbname="vectordb" -f /sqlscripts/create_tables.sql

echo "tables in vectordb -->"
"${psql[@]}" --dbname="vectordb" <<-EOSQL 
    \dt; 
EOSQL

echo "seeding data..."
"${psql[@]}" --dbname="vectordb" -f /sqlscripts/seed.sql

# Run the original entrypoint script
# /usr/local/bin/docker-entrypoint.sh "$@"