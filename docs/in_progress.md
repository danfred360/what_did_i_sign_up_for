# in progress

## up next
- app
  - question answering
    - return citations with answer
    - generate questions that are relevant to a segment and create an embedding for each question to store with the segment
  - support filtering results by collection, class_id, file, or document
    - support filtering by a combination of these?
  - return confidence score with each result
    - how close it was to the query
    - if the question was answered
  - improve exception handling in vectordb provider
  - improve logging
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