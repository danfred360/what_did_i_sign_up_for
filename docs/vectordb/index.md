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

## resources
- [pgvector](https://github.com/pgvector/pgvector)