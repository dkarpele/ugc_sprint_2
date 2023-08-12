# Sprint 9, UGC - 2 

### Installation

1. Clone [repo](https://github.com/dkarpele/ugc_sprint_2).
2. Create ```.env``` file according to ```.env.example```.
3. Launch the project ```docker-compose up --build```.


#### [cluster_clickhouse](cluster_clickhouse)

Cluster settings for ClickHouse (runs from `docker-compose.yaml`)

#### [etl](etl)

ETL process to transfer from Kafka (running in Yandex Cloud) to ClickHouse (docker)

#### [research](research)

Research which storage to use: Vertica (docker), ClickHouse (docker) or MongoDB (docker) - **NEW**

#### [users_interact_api](users_interact_api)

API endpoint (docker) sends data to Kafka.
- POST http://127.0.0.1/api/v1/views/send-movie-time - create user's viewed timeframe for movie

Send User Generated Content to MongoDB

**Bookmarks**
- POST http://127.0.0.1/api/v1/bookmarks/bookmarks - add movie bookmark for current user
- GET http://127.0.0.1/api/v1/bookmarks/bookmarks - get list of user's bookmarks
- DELETE http://127.0.0.1/api/v1/bookmarks/bookmarks - delete bookmark for current user

**Likes**
- POST http://127.0.0.1/api/v1/likes/like - add like to movie for current user
- POST http://127.0.0.1/api/v1/likes/dislike - add dislike to movie for current user
- DELETE http://127.0.0.1/api/v1/likes/like - delete like or dislike from current user
- GET http://127.0.0.1/api/v1/likes/avg-movie-rating?movie_id=<movie_id> - average rating for movie
- GET http://127.0.0.1/api/v1/likes/likes-dislikes-count-movie?movie_id=<movie_id> - amount of likes and dislikes for current movie