## Review after sprint 8 (ClickHouse VS Vertica)
Writing to ClickHouse is always faster than to Vertica. The best result for CH is for  100-1000 chunks. The best result for upload to clickhouse is two times faster than the best result for Vertica. The worst result for CH is about 8 times faster than for Verica.

Reading not aggregated data from Clickhouse is 4 times faster than from Vertica. Reading of aggregated data is 2 times faster but if you make the same request few times than Vertica becomes faster (Probably vertica creates index behind the scenes).

So, we will use ClickHouse as a storage for analytical data.