import os
import tarfile
import time
import uuid
import multiprocessing as mp

import docker
from dotenv import load_dotenv
from pymongo import MongoClient
from faker import Faker

load_dotenv()


docker_client = docker.from_env()
container = docker_client.containers.get(os.environ.get('CONTAINER_NAME'))


conn_info = f'mongodb://'\
            f'{os.environ.get("ROOT_USERNAME")}:'\
            f'{os.environ.get("ROOT_PASSWORD")}@'\
            f'{os.environ.get("HOST")}:{os.environ.get("PORT")}'
client = MongoClient(conn_info)
db = client[os.environ.get('MONGO_INITDB_DATABASE')]

fake: Faker = Faker()

num_chunks = 100
chunk_size = 100_000


def load_data_to_file(collection_name, collection_data):
    db.drop_collection(collection_name)
    filename = f'{collection_name}.csv'

    start = time.time()

    with open(filename, 'w') as file:
        file.write(''.join(str(x) for x in collection_data))
    end = time.time()

    with tarfile.open(f'{filename}' + '.tar', mode='w') as tar:
        tar.add(f'{filename}')

    container.put_archive('/data/db/', open(
        f'{os.getcwd()}/{collection_name}.csv.tar',
        'rb').read())

    return end - start


def insert_data_likes(chunks_amount=None) -> None:
    if not os.path.isfile(f'{os.getcwd()}/likes.csv'):
        raise Exception('Create likes.csv first!')
    try:
        container.exec_run(
                  f'mongoimport {conn_info} '
                  f'-d {os.environ.get("MONGO_INITDB_DATABASE")} '
                  f'-c likes '
                  f'--type=csv '
                  f'--fields="user_id,movie_id,point" '
                  f'--file=/data/db/likes.csv')

    except Exception as err:
        print(err)


if __name__ == "__main__":
    total_records = num_chunks * chunk_size

    # Likes
    collection = 'likes'
    data = ((f"'{uuid.uuid4()}',"
             f"'{uuid.uuid4()}',"
             f"{fake.random_int(min=0, max=1) * 10}"
             f"\n")
            for _ in range(chunk_size))
    elapsed_time_upload_to_file_likes = load_data_to_file(collection,
                                                    data)
    if elapsed_time_upload_to_file_likes:
        print(f"Upload chunk_size={chunk_size} rows to file in "
              f"{elapsed_time_upload_to_file_likes} seconds for `{collection}`.")

    # Bookmarks
    collection = 'bookmarks'
    data = ((f"'{uuid.uuid4()}',"
             f"'{uuid.uuid4()}'"
             f"\n")
            for _ in range(chunk_size))
    elapsed_time_upload_to_file = load_data_to_file(collection,
                                                    data)
    if elapsed_time_upload_to_file:
        print(f"Upload chunk_size={chunk_size} rows to file in "
              f"{elapsed_time_upload_to_file} seconds for `{collection}`.")

    # Insert to likes collection
    start_time = time.time()
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(insert_data_likes, range(num_chunks))
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for `likes` collection")
    print(f"Total time: {elapsed_time + elapsed_time_upload_to_file_likes}"
          f" sec")

    #
    #
    # # Insert to bookmarks collection
    # start_time = time.time()
    # with mp.Pool(mp.cpu_count()) as pool:
    #     pool.map(insert_data_bookmarks, range(num_chunks))
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Insert {total_records} (num_chunks={num_chunks}, "
    #       f"chunk_size={chunk_size}) rows in "
    #       f"{elapsed_time} seconds for `bookmarks` collection")
    # print(f"Total time: "
    #       f"{elapsed_time + elapsed_time_create_lines_bookmarks}"
    #       f" sec")
