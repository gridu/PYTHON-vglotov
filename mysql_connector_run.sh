export USER=${1} PASS=${2}

python3 mysql-connector/get_csv_from_db.py --user "${USER}" --passw "${PASS}"