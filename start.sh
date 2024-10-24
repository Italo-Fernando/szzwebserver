cd $(dirname "$0")
./stop.sh

docker compose build
docker compose up -d git_data_db rabbitmq
sleep 10
docker compose run -e PGPASSWORD=example db_populator psql -U example -h git_data_db -p 5432 -d git_repository -f /app/insert_variants.sql
sleep 10
docker compose up -d szz_runner szz_webserver