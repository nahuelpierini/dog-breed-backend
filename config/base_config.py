from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    CONTAINER_NAME = config('CONTAINER_NAME')
    AZURE_STORAGE_CONNECTION_STRING = config('AZURE_STORAGE_CONNECTION_STRING')
    DB_HOST = config('DB_HOST')
    DB_NAME = config('DB_NAME')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_ENGINE = config('DB_ENGINE')