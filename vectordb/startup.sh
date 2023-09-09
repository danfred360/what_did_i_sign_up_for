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
"${psql[@]}" --dbname="vectordb" -f /sqlscripts/load_extensions.sql
"${psql[@]}" --dbname="vectordb" -f /sqlscripts/init_schema.sql

echo "print tables in vectordb"
"${psql[@]}" --dbname="vectordb" <<-EOSQL 
    \dt; 
EOSQL

# echo "seeding data"
# "${psql[@]}" --dbname="vectordb" -f /sqlscripts/seed.sql

# Run the original entrypoint script
# /usr/local/bin/docker-entrypoint.sh "$@"