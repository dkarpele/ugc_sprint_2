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

num_chunks = 1000
chunk_size = 10_000


def load_data_to_file(collection_name, collection_data):
    db.drop_collection(collection_name)
    db[collection_name].create_index([("user_id", 1)])
    db[collection_name].create_index([("movie_id", 1)])
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

    print(f"Upload chunk_size={chunk_size} rows to file {filename} in "
          f"{end - start} seconds for `{collection}`.")
    return end - start


def insert_data(collection_name='likes',
                file_name='likes.csv',
                fields='user_id,movie_id,rating') -> None:
    if not os.path.isfile(f'{os.getcwd()}/{file_name}'):
        raise Exception(f'Create {file_name} first!')
    try:
        container.exec_run(
                  f'mongoimport {conn_info} '
                  f'-d {os.environ.get("MONGO_INITDB_DATABASE")} '
                  f'-c {collection_name} '
                  f'--type=csv '
                  f'--fields="{fields}" '
                  f'--file=/data/db/{file_name}')

    except Exception as err:
        print(err)


if __name__ == "__main__":
    total_records = num_chunks * chunk_size

    # Likes file
    collection = 'likes'
    data = ((f"{uuid.uuid4()},"
             f"{uuid.uuid4()},"
             f"{fake.random_int(min=0, max=1) * 10}"
             f"\n")
            for _ in range(chunk_size))
    elapsed_time_upload_to_file = load_data_to_file(collection,
                                                    data)

    # Insert to likes collection
    start_time = time.time()
    items = [('likes', 'likes.csv', 'user_id,movie_id,rating')
             for i in range(num_chunks)]
    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(insert_data, items)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for {collection} collection")
    print(f"Total time: {elapsed_time + elapsed_time_upload_to_file}"
          f" sec")

    # Bookmarks file
    collection = 'bookmarks'
    data = ((f"{uuid.uuid4()},"
             f"{uuid.uuid4()}"
             f"\n")
            for _ in range(chunk_size))
    elapsed_time_upload_to_file = load_data_to_file(collection,
                                                    data)

    # Insert to bookmarks collection
    start_time = time.time()
    items = [('bookmarks', 'bookmarks.csv', 'user_id,movie_id')
             for i in range(num_chunks)]
    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(insert_data, items)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Insert {total_records} (num_chunks={num_chunks}, "
          f"chunk_size={chunk_size}) rows in "
          f"{elapsed_time} seconds for {collection} collection")
    print(f"Total time: {elapsed_time + elapsed_time_upload_to_file}"
          f" sec")
