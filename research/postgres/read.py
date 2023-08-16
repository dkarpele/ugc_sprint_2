import os
import time
import multiprocessing as mp

import psycopg2

from dotenv import load_dotenv

from research.postgres.upload_from_file import insert_data

load_dotenv()

conn_info = {'dbname': os.environ.get('DB_NAME'),
             'user': os.environ.get('DB_USER'),
             'password': os.environ.get('DB_PASSWORD'),
             'host': os.environ.get('DB_HOST', '127.0.0.1'),
             'port': os.environ.get('DB_PORT', 5432)}
pg_connection = psycopg2.connect(**conn_info)

user_id = '0ccd3069-d485-45d4-9523-f37acd442593'
movie_id = 'e853940e-0227-477f-b777-ccd8e5e13a06'


def count_user_likes(like=10):
    try:
        with pg_connection:
            with pg_connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    select count(*) from likes
                     where rating='{like}' AND user_id='{user_id}';
                    """
                )
                return cursor.fetchone()

    except Exception as err:
        print(err)


def count_liked_movies(like=10):
    try:
        with pg_connection:
            with pg_connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    select count(*) from likes
                     where rating='{like}' AND movie_id='{movie_id}';
                    """
                )
                return cursor.fetchone()

    except Exception as err:
        print(err)


def average_movie_rating():
    try:
        with pg_connection:
            with pg_connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    select avg(rating) from likes
                    where movie_id='{movie_id}' group by movie_id;
                    """
                )
                return cursor.fetchone()

    except Exception as err:
        print(err)


def read_uploaded_data():
    start_time = time.time()
    user_dislikes = count_user_likes(0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Found {user_dislikes} user dislikes in {elapsed_time} seconds")

    start_time = time.time()
    user_likes = count_user_likes(10)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Found {user_likes} user likes in {elapsed_time} seconds")

    start_time = time.time()
    movie_likes = count_liked_movies(10)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Found {movie_likes} likes for movie in {elapsed_time} seconds")

    start_time = time.time()
    movie_dislikes = count_liked_movies(0)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Found {movie_dislikes} dislikes for movie in {elapsed_time} "
          f"seconds")

    start_time = time.time()
    avg_rating = average_movie_rating()
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Average movie rating {avg_rating} "
          f"found in {elapsed_time} seconds")


def read_live_data():
    start_time = time.time()
    p1_upload = mp.Process(target=insert_data)
    p1_upload.start()

    p2_read = mp.Process(target=count_user_likes)
    p2_read.start()

    p1_upload.join()
    p2_read.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Found user likes in {elapsed_time} seconds during uploading"
          f" some data to the same collection")


if __name__ == "__main__":
    read_uploaded_data()
    read_live_data()
