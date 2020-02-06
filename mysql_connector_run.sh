docker run --name=docker_sql --env="MYSQL_ROOT_PASSWORD=passw0rd" -p 3306:3306 -d mysql:latest
docker ps
sleep 1
python ./mysql-connector/get_csv_from_db.py
mysql -h 127.0.0.1 -P 3306 -u root -ppassw0rd -e "SELECT * FROM csvToGetDBdocker.test_data;"
echo Total rows in table:
mysql -h 127.0.0.1 -P 3306 -u root -ppassw0rd -e "SELECT COUNT(date) FROM csvToGetDBdocker.test_data;"