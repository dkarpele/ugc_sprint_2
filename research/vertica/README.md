# Upload data to Vertica

1. `cd vertica`
2. `docker-compose up`
3. `python upload.py`

Here we use `COPY` method to upload data to Vertica from data.csv file created before. Thanks to multiprocessing upload is going for seconds not for minutes.

```commandline
Upload chunk_size=100.000 rows to file in 1.82918119430542 seconds
Insert 10.000.000 (num_chunks=100, chunk_size=100000) rows in 2.7222237586975098 seconds
Insert speed: 3673467.3143785414 rows/sec
Total time: 4.55140495300293
```

```commandline
Upload chunk_size=10.000 rows to file in 0.17650842666625977 seconds
Insert 10.000.000 (num_chunks=1000, chunk_size=10000) rows in 7.906338453292847 seconds
Insert speed: 1264807.9840087267 rows/sec
Total time: 8.082846879959106 sec
```

```commandline
Upload chunk_size=1000 rows to file in 0.018946170806884766 seconds
Insert 10.000.000 (num_chunks=10.000, chunk_size=1000) rows in 62.586204051971436 seconds
Insert speed: 159779.62158714762 rows/sec
Total time: 62.60515022277832 sec
```

___

## Review
It's obvious that smaller amount of chunks will speed up upload data to Vertica.


# Read data from Vertica

1. `cd vertica`
2. `docker-compose up`
3. `python upload.py` - It will create data.csv. It's mandatory for `read.py`
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

I) Select all rows in 4.089077472686768 seconds
II) Select all rows in 1.338136911392212 seconds 
 I guess vertica creates index after first request.
III) Select all rows in 0.4279141426086426 seconds
```

```commandline
Select all rows in 34.323320150375366 seconds
for query
        """
        SELECT
            user_id
        FROM user_viewed_frame
        WHERE ts > '2022-12-01 00:00:00'
        """
```
