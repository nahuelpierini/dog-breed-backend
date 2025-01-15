from config.base_config import Config
from decouple import config

class ProductionConfig(Config):
    DEBUG = False
    AZURE_ML_URL = config('AZURE_ML_URL')
    AZURE_ML_TOKEN = config('AZURE_ML_TOKEN')
