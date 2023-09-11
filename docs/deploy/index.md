# deploy
The `deploy` directory contains the files needed to deploy the application using docker compose. `vectordb.env` and `app.env` must be created using the `env.example` files as a template.

```bash
cd deploy
docker compose up
```

The site should be accessible at [localhost](http://localhost)