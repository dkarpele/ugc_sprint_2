import os
import time
import multiprocessing as mp

from pymongo import MongoClient

from research.mongoDB.upload_from_file import insert_data

conn_info = f'mongodb://'\
            f'{os.environ.get("ROOT_USERNAME")}:'\
            f'{os.environ.get("ROOT_PASSWORD")}@'\
            f'{os.environ.get("HOST")}:{os.environ.get("PORT")}'
client = MongoClient(conn_info)
db = client[os.environ.get('MONGO_INITDB_DATABASE')]

user_id = 'eb20837b-a15a-4859-a340-e4b243ff522d'
movie_id = '284b6fe4-7cd6-4137-9096-100158e79ed7'


def count_user_likes(like=10):
    try:
        filter_ = {'user_id': user_id,
                   'point': like}
        return db['likes'].count_documents(filter_)

    except Exception as err:
        print(err)


def count_liked_movies(like=10):
    try:
        filter_ = {'movie_id': movie_id,
                   'point': like}
        return db['likes'].count_documents(filter_)

    except Exception as err:
        print(err)


def average_movie_rating():
    try:
        filter_ = [
            {
                '$match': {
                    'movie_id': movie_id
                }
            },
            {
                '$group': {
                    '_id': "$movie_id",
                    'avg_rating': {
                        '$avg': "$point"
                    }
                }
            }
        ]
        return db['likes'].aggregate(filter_)

    except Exception as err:
        print(err)


def show_user_likes(like=10):
    try:
        filter_ = {'user_id': user_id,
                   'point': like}
        res = db['likes'].find(filter_, {"movie_id": 1})
        return res
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

    print(f"Average movie rating {[x for x in avg_rating][0]['avg_rating']} "
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
