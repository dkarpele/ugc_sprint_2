# Upload data to MongoDB

1. `cd mongoDB`
2. `docker-compose up`
3. `chmod 744 mongo-cluster-config.sh`
4. `./mongo-cluster-config.sh`
5. `python upload_from_file.py`

Here we use `mongoimport` method to upload data to MongoDB from data.csv file created before. Thanks to multiprocessing upload is going for seconds not for minutes.

```commandline
Upload chunk_size=500000 rows to file likes.csv in 3.5695748329162598 seconds for `likes`.
Insert 10000000 (num_chunks=20, chunk_size=500000) rows in 30.569183826446533 seconds for likes collection
Total time: 34.13875865936279 sec
Upload chunk_size=500000 rows to file bookmarks.csv in 2.9929966926574707 seconds for `bookmarks`.
Insert 10000000 (num_chunks=20, chunk_size=500000) rows in 51.38963198661804 seconds for bookmarks collection
Total time: 54.38262867927551 sec
```

___

## Review
MongoDB works **much slower** than ClickHouse for upload data. The best result for the similar data that I found (`num_chunks=20, chunk_size=500000`) is only about 30 seconds for 10M rows while to CH it was 1.5 seconds. So uploading to Mongo is unimpressive.



# Read data from MongoDB

1. `cd mongoDB`
2. `docker-compose up`
3. `chmod 744 mongo-cluster-config.sh`
4. `./mongo-cluster-config.sh`
5. `python upload_from_file.py` - It will create likes.csv. It's mandatory before `read.py`
6. `python read.py` - Some load (insert 10000 rows) to the database will be emulated during reading.

```commandline
Found 1001 user dislikes in 0.008716344833374023 seconds
Found 0 user likes in 0.0029973983764648438 seconds
Found 1001 likes for movie in 0.003248453140258789 seconds
Found 0 dislikes for movie in 0.0030100345611572266 seconds
Average movie rating 10.0 found in 0.0034134387969970703 seconds
Found user likes in 0.20038866996765137 seconds during uploading some data to the same collection
```

Results are the same during sequential calls. There were about 10M documents in `likes` collection during reading. It's clear that for MongoDB does not matter how many results were returned (0 or 1001). The most important thing here was to create index for `user_id` and `movie_id`. Index speeds up reading data for about 1000 times! It's also interesting that the same method `count_user_likes` works 100 times slower if at the same time data was being uploaded to the collection. Compare lines 2 and 6 (0.0029 vs 0.2003). Although it is still very fast.
