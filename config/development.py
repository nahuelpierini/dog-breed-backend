from config.base_config import Config
from decouple import config

class DevelopmentConfig(Config):
    DEBUG = True
    MODEL_PATH = config('MODEL_PATH')
    LABEL_MAPPING_PATH = config('LABEL_MAPPING_PATH')
