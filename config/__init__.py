from config.development import DevelopmentConfig
from config.production import ProductionConfig
from decouple import config

environment = config('FLASK_ENV')

config_env = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

selected_env = config_env.get(environment, DevelopmentConfig)