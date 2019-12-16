python3 -m pip install --user virtualenv
python3 -m testenv env
pip install -r install/requirements.txt
python -m pytest models/BookModel_test.py app_test.py
python3 app.py
