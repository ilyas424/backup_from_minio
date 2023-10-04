from minio import Minio
from minio.error import S3Error

import os

ENDPOINT_MINIO = "YOUR URL MINIO"
ACCES_KEY = "access_key"
SECRET_KEY= "secret_key"

ENDPOINT_MINIO_GITLAB = "YOUR URL MINIO"
ACCES_KEY_GITLAB = "access_key"
SECRET_KEY_GITLAB = "secret_key"

GITLAB_BUCKET = "my_bucket"
MINIO_BACKET = "minio_bucket"

client_minio = Minio(
    ENDPOINT_MINIO,
    access_key=ACCES_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

client_git = Minio(
    ENDPOINT_MINIO_GITLAB,
    access_key=ACCES_KEY_GITLAB,
    secret_key=SECRET_KEY_GITLAB,
    region="us-east-1",
    secure=False
)


def show_bucket_objects(bucket_name):
    try:
        # Получение списка объектов в бакете
        objects = client_git.list_objects(bucket_name, recursive=True)
        new_lst = []


        print(f"Содержимое бакета '{bucket_name}':")
        for obj in objects:
            new_lst.append(obj.object_name)

    except S3Error as err:
        print(f"Ошибка при получении списка объектов: {err}")
    
    return  new_lst[-1]


def upload_file(FILE_NAME):
    try:
        client_git.fget_object(GITLAB_BUCKET, FILE_NAME, FILE_NAME)
        print(f'Файл  успешно скачан из бакета  с помощью Minio.')

    except S3Error as e:
            print(f'Ошибка при скачивании файла: {e}')
        
    return True


def download_file(FILE_NAME):
    try:
        file_path = f'/your_url/{FILE_NAME}'

        object_name = FILE_NAME

        client_minio.fput_object(MINIO_BACKET, object_name, file_path)
        
        print(f'Файл успешно отправлен в бакет {MINIO_BACKET}  под именем {FILE_NAME}')

    except S3Error as err:
        print(f'Произошла ошибка при отправке файла: {err}')
    
    return True


def remove_object(bucket_name, object_name):
    try:

        # Удаление объекта
        client_git.remove_object(bucket_name, object_name)
        print(f'Объект {object_name} успешно удален из бакета {bucket_name}')
    except S3Error as err:
        print(f'Ошибка при удалении объекта: {err}')


def remove_file_tar(FILENAME):
    try:
        os.remove(f'/your_url/{FILENAME}')
        print(f"Файл {FILENAME} успешно удален.")
    except OSError as e:
        print(f"Ошибка при удалении файла {FILENAME}: {e}")


if __name__ == "__main__":
    FILE_NAME = show_bucket_objects(GITLAB_BUCKET)
    if upload_file(FILE_NAME):
        if download_file(FILE_NAME):
            remove_file_tar(FILE_NAME)
            remove_object(GITLAB_BUCKET, FILE_NAME)

