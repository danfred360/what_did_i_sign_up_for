# app
Python api (made with fastapi) to provide a web interface for the vectordb and question answering with langchain.
## local development
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

## resources
- https://wiki.postgresql.org/wiki/Psycopg2_Tutorial