export DB=${1:-"test_db"} TABLE=${2:-"test_table"}

docker run --env="MYSQL_ROOT_PASSWORD=passw0rd" -p 3306:3306 -d mysql:latest
sleep 5
python3 ./mysql-connector/get_csv_from_db.py --db ${DB} --table ${TABLE}
mysql -h 127.0.0.1 -P 3306 -u root -ppassw0rd -e "SELECT * FROM ${DB}.${TABLE};"