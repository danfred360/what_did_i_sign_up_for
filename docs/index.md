# what_did_i_sign_up_for

## run locally
```bash
# initialize virtual environment
python -m venv venv
. venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run
cd app
uvicorn main:app --reload
```

See swagger page [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## run tests
```bash
# run pytests
pytest app
```