
export PORT=${1:-5000} LOG_METHOD=${2:-"console"} LOG_LVL=${3:-"INFO"}

python3 -m pip install --user virtualenv
python3 -m testenv env
pip install -r install/requirements.txt
python3 -m pytest models/BookModel_test.py app_test.py
python3 app.py --port ${PORT} --log_method "${LOG_METHOD}" --log_lvl "${LOG_LVL}"