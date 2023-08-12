# Upload data to MongoDB

1. `cd mongoDB`
2. `docker-compose up`
3. `chmod 744 mongo-cluster-config.sh`
4. `./mongo-cluster-config.sh`
5. `python upload_from_file.py`

Here we use `SELECT * FROM file` method to upload data to MongoDB from data.csv file created before. Thanks to multiprocessing upload is going for seconds not for minutes.

```commandline
Upload chunk_size=100.000 rows to file in 1.9522244930267334 seconds
Insert 10.000.000 (num_chunks=100, chunk_size=100.000) rows in 1.4755141735076904 seconds
Insert speed: 6777298.503495453 rows/sec
Total time: 3.427738666534424 sec
```

```commandline
Upload chunk_size=10.000 rows to file in 0.18043851852416992 seconds
Insert 10.000.000 (num_chunks=1000, chunk_size=10.000) rows in 1.8392279148101807 seconds
Insert speed: 5437064.063391002 rows/sec
Total time: 2.0196664333343506 sec
```

```commandline
Upload chunk_size=1000 rows to file in 0.019498348236083984 seconds
Insert 10.000.000 (num_chunks=10.000, chunk_size=1000) rows in 8.14340353012085 seconds
Insert speed: 1227987.7772250834 rows/sec
Total time: 8.162901878356934 sec
```

___

## Review
MongoDB works faster with 100-1000 amount of chunks. The best result for upload for MongoDB is two times faster than the best result for Vertica. Also, MongoDB often fails during upload with the error below. As a result I see only 9970000 rows instead of 1M.
```Code: 1000.
DB::Exception: I/O error: Too many open files. Stack trace:
```
or just
```commandline
Code: 100. Unknown packet 4 from server localhost:9000
[Errno 32] Broken pipe
[Errno 32] Broken pipe
[Errno 32] Broken pipe
[Errno 32] Broken pipe
[Errno 104] Connection reset by peer
Error on localhost:9000 ping: Unexpected EOF while reading bytes
Error on localhost:9000 ping: Unexpected EOF while reading bytes
Connection was closed, reconnecting.
Connection was closed, reconnecting.
Error on socket shutdown: [Errno 107] Transport endpoint is not connected
```

# Read data from MongoDB

1. `cd mongoDB`
2. `docker-compose up`
3. `python upload_from_file.py` - It will create data.csv. It's mandatory before `read.py`
4. `python read.py` - Some load (insert 10000 rows) to the database will be emulated during reading.

```commandline
query = 
            """
        SELECT
            user_id,
            max(viewed_frame)
        FROM user_viewed_frame
        WHERE ts > '2022-12-01 00:00:00'
        GROUP by user_id
        """

I) Select all rows in 1.7852933406829834 seconds
II) Select all rows in 1.8951201438903809 seconds 
III) Select all rows in 1.8790724277496338 seconds
```

Results are the same during sequential calls. 

```commandline
Select all rows in 9.48959493637085 seconds
for query
        """
        SELECT
            user_id
        FROM user_viewed_frame
        WHERE ts > '2022-12-01 00:00:00'
        """
```

___

## Review
Reading not aggregated data from MongoDB is 4 times faster than from Vertica. Reading of aggregated data is 2 times faster but if you make the same request few times than Vertica becomes faster (Probably vertica creates index behind the scenes).