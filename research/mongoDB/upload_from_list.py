import os
import time
import uuid
import multiprocessing as mp

from dotenv import load_dotenv
from pymongo import MongoClient
from faker import Faker

load_dotenv()

client = MongoClient(f'mongodb://'
                     f'{os.environ.get("ROOT_USERNAME")}:'
                     f'{os.environ.get("ROOT_PASSWORD")}@'
                     f'{os.environ.get("HOST")}:{os.environ.get("PORT")}')
db = client['ugc']

fake: Faker = Faker()

num_chunks = 10
chunk_size = 1_000_000


def load_data_to_list_likes(size):
    db.drop_collection('likes')
    start = time.time()
    lines_ = [{"user_id": str(uuid.uuid4()),
               "movie_id": str(uuid.uuid4()),
               "rating": fake.random_int(min=0, max=1) * 10}
              for _ in range(size)]

    end = time.time()

    return lines_, end - start


def load_data_to_list_bookmarks(size):
    db.drop_collection('bookmarks')
    start = time.time()
    lines_ = [{"user_id": str(uuid.uuid4()),
               "movie_id": str(uuid.uuid4())}
              for _ in range(size)]

    end = time.time()

    return lines_, end - start


(lines_likes, elapsed_time_create_lines_likes) \
    = (load_data_to_list_likes(chunk_size))
print(f"Upload chunk_size={chunk_size} rows to list in\n"
      f"{elapsed_time_create_lines_likes} seconds for `likes` collection.")


def insert_data_likes(chunks_amount=None) -> None:
    collection = db['likes']
    try:
        collection.insert_many(lines_likes)
    except Exception as err:
        print(err)


(lines_bookmarks, elapsed_time_create_lines_bookmarks) = \
        (load_data_to_list_bookmarks(chunk_size))
print(f"Upload chunk_size={chunk_size} rows to list in\n"
      f"{elapsed_time_create_lines_bookmarks} seconds for `bookmarks` "
      f"collection.")


def insert_data_bookmarks(chunks_amount=None) -> None:
    collection = db['bookmarks']
    try:
        collection.insert_many(lines_bookmarks)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    total_records = num_chunks * chunk_size

    # Insert to likes collection
    start_time = time.time()
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(insert_data_likes, range(num_chunks))
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for `likes` collection")
    print(f"Total time: {elapsed_time + elapsed_time_create_lines_likes}"
          f" sec")

    # Insert to bookmarks collection
    start_time = time.time()
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(insert_data_bookmarks, range(num_chunks))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for `bookmarks` collection")
    print(f"Total time: "
          f"{elapsed_time + elapsed_time_create_lines_bookmarks}"
          f" sec")
