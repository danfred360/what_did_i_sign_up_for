# what_did_i_sign_up_for

See what's [in progress](./in_progress.md).

## quickstart
```bash
cd deploy
docker compose up
```

Access site at [localhost](http://localhost).

## local developement

### app
```bash
# initialize virtual environment
python -m venv venv
. venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run
uvicorn app.main:app --reload
```

See swagger page [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

local checks
```bash
# run tests
pytest app

# run linter
ruff check app
```

See [the app docs](./app/index.md) for more information.

### vectordb
```
cd vectordb
docker compose up
```

See [the vectordb docs](./vectordb/index.md) for more information.

## run with Docker
```bash
# build image
docker build -t app .

# run container
docker run -d --name app -p 80:80 app
```

![site-screenshot](./assets/site-screenshot.png)

## resources
- https://fastapi.tiangolo.com/tutorial/testing/
- https://www.codewithfaraz.com/content/61/how-to-create-neobrutalism-sign-up-form-using-html-and-css-only
- https://betterstack.com/community/guides/logging/how-to-start-logging-with-python/