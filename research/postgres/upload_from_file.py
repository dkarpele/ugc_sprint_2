import os
import tarfile
import time
import uuid

import docker
import psycopg2

from dotenv import load_dotenv
from faker import Faker

fake: Faker = Faker()

load_dotenv()

conn_info = {'dbname': os.environ.get('DB_NAME'),
             'user': os.environ.get('DB_USER'),
             'password': os.environ.get('DB_PASSWORD'),
             'host': os.environ.get('DB_HOST', '127.0.0.1'),
             'port': os.environ.get('DB_PORT', 5432)}
pg_connection = psycopg2.connect(**conn_info)

num_chunks = 20
chunk_size = 500_000


def load_data_to_file(table_name, table_data):
    filename = f'{table_name}.csv'

    start = time.time()

    with open(filename, 'w') as file:
        file.write(''.join(str(x) for x in table_data))
    end = time.time()

    with tarfile.open(f'{filename}' + '.tar', mode='w') as tar:
        tar.add(f'{filename}')

    client = docker.from_env()
    container = client.containers.get('postgres')
    container.put_archive('/data/postgres/', open(
        f'{os.getcwd()}/{table_name}.csv.tar',
        'rb').read())

    print(f"Upload chunk_size={chunk_size} rows to file {filename} in "
          f"{end - start} seconds for `{table_name}`.")
    return end - start


def insert_data(table_name='likes',
                file_name='likes.csv',
                fields='user_id,movie_id,rating') -> None:
    if not os.path.isfile(f'{os.getcwd()}/{file_name}'):
        raise Exception(f'Create {file_name} first!')
    try:
        with pg_connection:
            with pg_connection.cursor() as cursor:
                cursor.execute(
                    f"COPY {table_name}({fields}) "
                    f"FROM '/data/postgres/{file_name}' DELIMITER ',';"
                )
    except Exception as err:
        print(err)


def prepare_db():
    with pg_connection:
        with pg_connection.cursor() as cursor:
            cursor.execute(
                """
                DROP TABLE IF EXISTS likes;
                """
            )
            cursor.execute(
                """
                DROP TABLE IF EXISTS bookmarks;
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS likes
                (
                    user_id VARCHAR,
                    movie_id VARCHAR,
                    rating INTEGER
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bookmarks
                (
                    user_id VARCHAR,
                    movie_id VARCHAR
                );
            """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_user_movie
                ON likes(user_id, movie_id);
            """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_user_movie_b
                ON bookmarks(user_id, movie_id);
            """
            )


if __name__ == "__main__":

    total_records = num_chunks * chunk_size

    prepare_db()

    # Likes file
    table = 'likes'
    data = ((f"{uuid.uuid4()},"
             f"{uuid.uuid4()},"
             f"{fake.random_int(min=0, max=1) * 10}"
             f"\n")
            for _ in range(chunk_size))
    elapsed_time_upload_to_file = load_data_to_file(table,
                                                    data)

    # Insert to likes table
    start_time = time.time()

    for i in range(num_chunks):
        insert_data(table, 'likes.csv', 'user_id,movie_id,rating')
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for {table} table")
    print(f"Total time: {elapsed_time + elapsed_time_upload_to_file}"
          f" sec")

    # Bookmarks file
    table = 'bookmarks'
    data = ((f"{uuid.uuid4()},"
             f"{uuid.uuid4()}"
             f"\n")
            for _ in range(chunk_size))
    elapsed_time_upload_to_file = load_data_to_file(table,
                                                    data)

    # Insert to bookmarks table
    start_time = time.time()

    for i in range(num_chunks):
        insert_data(table, 'bookmarks.csv', 'user_id,movie_id')
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for {table} tabl")
    print(f"Total time: {elapsed_time + elapsed_time_upload_to_file}"
          f" sec")
