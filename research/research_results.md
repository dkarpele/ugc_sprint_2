## Review after sprint 9 (MongoDB VS Postgres)
All numbers are in the relevant directories.
Writing to Postgres was slower than to MongoDb but not significantly considering that for postgres I didn't use multiprocessing. We use very similar approach (upload from file to DB), the same amount of data (10M rows).

Time execution for simple reading requests were almost the same for postgres and Mongo. Reading aggregated data with simultaneous load to the same collection was 16 times faster from MongoDB than from Postgres. Reading aggregated data without load was 20 times faster.

We will use MongoDB. Moreover, python client for MongoDB is much more convenient.


## Review after sprint 9 (MongoDB VS ClickHouse)
All numbers are in the relevant directories.
Writing to MongoDB is much slower than to ClickHouse. We use very similar approach (upload from file to DB), the same amount of data (10M rows). Also, everywhere we used multiprocessing to speed process up.

But when we talk about reading - MongoDB wins. At least according to our research. It's very important to use index in MongoDB. Reading aggregated data with simultaneous load to the same collection was 9 times faster from MongoDB than from ClickHouse.

So our choice for UGC is MongoDB.  


## Review after sprint 8 (ClickHouse VS Vertica)
Writing to ClickHouse is always faster than to Vertica. The best result for CH is for 100-1000 chunks. The best result for upload to clickhouse is two times faster than the best result for Vertica. The worst result for CH is about 8 times faster than for Verica.

Reading not aggregated data from Clickhouse is 4 times faster than from Vertica. Reading of aggregated data is 2 times faster but if you make the same request few times than Vertica becomes faster (Probably vertica creates index behind the scenes).

So, we will use ClickHouse as a storage for analytical data.