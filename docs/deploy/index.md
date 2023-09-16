# deploy
**These are not up to date, but note:**
to mount log files, you need to create the directory first, and then mount it. Otherwise docker will create a directory with root permissions and the app will not be able to write to it.

The `deploy` directory contains the files needed to deploy the application using docker compose. `vectordb.env` and `app.env` must be created using the `env.example` files as a template.

```bash
cd deploy
docker compose up
```

The site should be accessible at [localhost](http://localhost)

See [the readme](../../README.md) for the quickstart guide.

The docker compose file is configured to use the `latest` tag for the `vectordb` and `app` images. 

The app image creates a volume to the input files directory. This allows the user to add files to the `input_files` directory and have them available to the app.

The vectordb image creates a volume to the data directory to persist the database. Database migrations are not currently supported so if you don't want to lose data maybe pin the image to a sha.
```yml
services:
  app:
    container_name: testing-app
    image: ghcr.io/danfred360/what_did_i_sign_up_for-app:latest
    environment:
      VECTORDB_HOST: testing-vectordb
      VECTORDB_PORT: 5432
      INPUT_FILES_DIRECTORY: /code/input_files
    env_file:
      - app.env
    ports:
      - 80:80
    volumes:
      - ./input_files:/code/input_files

  vectordb:
    container_name: testing-vectordb
    image: ghcr.io/danfred360/what_did_i_sign_up_for-vectordb:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
    env_file:
      - vectordb.env
    volumes:
      - ./data:/var/lib/postgresql/data
```