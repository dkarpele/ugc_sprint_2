# Upload data to Postgres

1. `cd postgres`
2. `docker-compose up`
3. `python upload_from_file.py`

Here we use `COPY` method to upload data to Postgres from data.csv file created before.

```commandline
Upload chunk_size=500000 rows to file likes.csv in 3.9165849685668945 seconds for `likes`.
Insert 10000000 (num_chunks=20, chunk_size=500000) rows in 56.479774475097656 seconds for likes table
Total time: 60.39635944366455 sec
Upload chunk_size=500000 rows to file bookmarks.csv in 4.408282995223999 seconds for `bookmarks`.
Insert 10000000 (num_chunks=20, chunk_size=500000) rows in 74.07430100440979 seconds for bookmarks tabl
Total time: 78.48258399963379 sec
```

___

## Review
The uploading results to postgres are about two times slower for `likes` table and 1.5 times slower for `bookmarks` table than to MongoDB. But it could be because I was unable to use multiprocessing with postgres. The scripts just don't stop even after uploading all batch of chunks.



# Read data from Postgres

1. `cd postgres`
2. `docker-compose up`
3. `python upload_from_file.py` - It will create likes.csv. It's mandatory before `read.py`
4. `python read.py` - Some load (insert 10000 rows) to the database will be emulated during reading.

```commandline
Found (0,) user dislikes in 0.0012710094451904297 seconds
Found (20,) user likes in 0.0001270771026611328 seconds
Found (20,) likes for movie in 0.0967247486114502 seconds
Found (0,) dislikes for movie in 0.059488534927368164 seconds
Average movie rating (Decimal('10.0000000000000000'),) found in 0.06133317947387695 seconds
Found user likes in 3.2410776615142822 seconds during uploading some data to the same collection
```

There were about 10M documents in `likes` collection during reading. It's also interesting that the same method `count_user_likes` works 25000 times slower if at the same time data was being uploaded to the collection. Compare lines 2 and 6 (0.00012 vs 3.241). 
