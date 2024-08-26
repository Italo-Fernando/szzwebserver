docker compose up -d git_data_db rabbitmq
sleep 10
docker compose up -d szz_runner szz_webserver