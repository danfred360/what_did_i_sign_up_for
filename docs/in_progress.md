# in progress

- app
  - split documents into segments
  - semantic search using vectordb provider
  - improve test coverage
  - harden production deployment
- vectordb
  - harden production deployment
- local experience
    - traefik reverse proxy
        - https?
        - /docs path?
        - need access to cloudflare to add dns records for letsencrypt
- deploy
  - kubernetes?
  - build docker containers for multiple chip architectures (may only currently support arm64 becuase I'm developing on a Mac M2)