from dotenv import dotenv_values

env_vars = dotenv_values('.config.env')

DB_CONNECTION = env_vars.get('DB_CONNECTION')
SECRET_KEY = env_vars.get('SECRET_KEY')