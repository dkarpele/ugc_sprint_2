# Проектная работа 8 спринта

### Installation

1. Clone [repo](https://github.com/dkarpele/ugc_sprint_1).
2. Create ```.env``` file according to ```.env.example```.
3. Launch the project ```docker-compose up --build```.

#### [architecture](architecture)

Component diagram for the whole project and sequence diagram for UGC.

#### [cluster_clickhouse](cluster_clickhouse)

Cluster settings for ClickHouse (runs from `docker-compose.yaml`)

#### [etl](etl)

ETL process to transfer from Kafka (running in Yandex Cloud) to ClickHouse (docker)

#### [research](research)

Research which storage to use: Vertica (docker) or ClickHouse (docker)

#### [users_analyze_api](users_analyze_api)

API endpoint (docker) sends data to Kafka.
- POST http://127.0.0.1/api/v1/views/send-movie-time - create user's viewed timeframe for movie