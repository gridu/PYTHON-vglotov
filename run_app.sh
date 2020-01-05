
export PORT=${1:-5000} LOG_METHOD=${2:-"console"} LOG_LVL=${3:-"INFO"} DB_PATH=${4:-"///"} DB_NAME=${5:-"book_db.db"}

python3 -m pip install --user virtualenv
python3 -m venv env
python3 setup.py install
python3 -m pytest models/BookModel_test.py app_test.py
python3 configuration.py --port ${PORT} --log_method "${LOG_METHOD}" --log_lvl "${LOG_LVL}" --db_path "${DB_PATH}" --db_name "${DB_NAME}"
python3 app.py