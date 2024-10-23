cd $(dirname "$0")
./stop.sh

docker compose build
docker compose up -d git_data_db rabbitmq
sleep 30
docker compose up -d szz_runner szz_webserver